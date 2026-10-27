"""Observable money and recovery contracts, using real SQLite files/processes."""
import multiprocessing
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from lab import ledger


def concurrent_settlement(db, request_id, barrier):
    barrier.wait(timeout=15)
    ledger.settle(db, request_id)


class SettlementTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.db = str(Path(self.temp.name) / "ledger.sqlite")
        ledger.initialize(self.db)

    def run_workers(self, requests):
        ctx = multiprocessing.get_context("spawn")
        barrier = ctx.Barrier(len(requests) + 1)
        workers = [ctx.Process(target=concurrent_settlement, args=(self.db, r, barrier))
                   for r in requests]
        for worker in workers:
            worker.start()
        try:
            barrier.wait(timeout=15)
            for worker in workers:
                worker.join(timeout=15)
                self.assertEqual(worker.exitcode, 0)
        finally:
            for worker in workers:
                if worker.is_alive():
                    worker.terminate()
                    worker.join(timeout=5)

    def test_two_processes_charge_same_account_without_lost_update(self):
        ledger.enqueue(self.db, "A", 3_000_000)
        ledger.enqueue(self.db, "B", 4_000_000)
        self.run_workers(["A", "B"])
        result = ledger.inspect(self.db)
        self.assertEqual(result["balance_micro_usd"], 3_000_000)
        self.assertEqual(result["settlement_count"], 2)
        self.assertEqual(len(result["pending_events"]), 2)

    def test_duplicate_delivery_across_processes_charges_once(self):
        ledger.enqueue(self.db, "A", 1_500_000)
        self.run_workers(["A", "A"])
        result = ledger.inspect(self.db)
        self.assertEqual(result["balance_micro_usd"], 8_500_000)
        self.assertEqual(result["settlement_count"], 1)
        self.assertEqual(len(result["pending_events"]), 1)

    def test_conflicting_command_cannot_replace_original_amount(self):
        ledger.enqueue(self.db, "A", 1_500_000)
        ledger.enqueue(self.db, "A", 1_500_000)
        with self.assertRaisesRegex(ValueError, "conflicting"):
            ledger.enqueue(self.db, "A", 2_000_000)
        ledger.settle(self.db, "A")
        self.assertEqual(ledger.inspect(self.db)["balance_micro_usd"], 8_500_000)

    def test_crash_before_commit_rolls_back_and_command_survives(self):
        ledger.enqueue(self.db, "A", 1_500_000)
        run = subprocess.run([sys.executable, "-m", "lab.ledger", "settle", "--db", self.db,
                              "--request", "A", "--crash", "before_commit"], timeout=15)
        self.assertEqual(run.returncode, 71)
        result = ledger.inspect(self.db)
        self.assertEqual(result["balance_micro_usd"], 10_000_000)
        self.assertEqual(result["settlement_count"], 0)
        self.assertEqual(len(result["pending_commands"]), 1)
        self.assertEqual(result["pending_events"], [])
        ledger.settle(self.db, "A")
        self.assertEqual(ledger.inspect(self.db)["balance_micro_usd"], 8_500_000)

    def test_crash_after_commit_leaves_outbox_and_retry_does_not_charge(self):
        ledger.enqueue(self.db, "A", 1_500_000)
        run = subprocess.run([sys.executable, "-m", "lab.ledger", "settle", "--db", self.db,
                              "--request", "A", "--crash", "after_commit"], timeout=15)
        self.assertEqual(run.returncode, 72)
        ledger.initialize(self.db)
        self.assertFalse(ledger.settle(self.db, "A"))
        result = ledger.inspect(self.db)
        self.assertEqual(result["balance_micro_usd"], 8_500_000)
        self.assertEqual(result["pending_commands"], [])
        self.assertEqual(len(result["pending_events"]), 1)
        self.assertEqual(result["pending_events"][0]["delta"], -1_500_000)

    def test_negative_cost_is_rejected_but_actual_overdraft_is_recorded(self):
        with self.assertRaises(ValueError):
            ledger.enqueue(self.db, "bad", -1)
        ledger.enqueue(self.db, "A", 10_500_000)
        ledger.settle(self.db, "A")
        self.assertEqual(ledger.inspect(self.db)["balance_micro_usd"], -500_000)


if __name__ == "__main__":
    unittest.main()
