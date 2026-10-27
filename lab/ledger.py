"""SQLite settlement/outbox lab. Amounts are integer microdollars.

No Redis, network gateway, credentials or provider requests are involved.
Crash hooks use os._exit solely in disposable subprocess experiments.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sqlite3


def connect(path):
    conn = sqlite3.connect(path, timeout=10, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA synchronous=FULL")
    return conn


def initialize(path, balance=10_000_000):
    if type(balance) is not int or not 0 <= balance <= 10**12:
        raise ValueError("invalid starting balance")
    conn = connect(path)
    try:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS accounts (
          user_id INTEGER PRIMARY KEY, balance INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS commands (
          user_id INTEGER NOT NULL REFERENCES accounts(user_id),
          request_id TEXT NOT NULL, actual INTEGER NOT NULL CHECK(actual >= 0),
          PRIMARY KEY(user_id, request_id));
        CREATE TABLE IF NOT EXISTS settlements (
          user_id INTEGER NOT NULL, request_id TEXT NOT NULL,
          actual INTEGER NOT NULL, PRIMARY KEY(user_id, request_id),
          FOREIGN KEY(user_id, request_id) REFERENCES commands(user_id, request_id));
        CREATE TABLE IF NOT EXISTS outbox (
          event_id INTEGER PRIMARY KEY AUTOINCREMENT,
          user_id INTEGER NOT NULL, request_id TEXT NOT NULL,
          delta INTEGER NOT NULL, delivered INTEGER NOT NULL DEFAULT 0,
          UNIQUE(user_id, request_id),
          FOREIGN KEY(user_id, request_id) REFERENCES settlements(user_id, request_id));
        """)
        # Reopening never resets a previously consumed balance.
        conn.execute("INSERT OR IGNORE INTO accounts VALUES (1, ?)", (balance,))
    finally:
        conn.close()


def enqueue(path, request_id, actual, user_id=1):
    """Durably accept an immutable command; duplicate content is a no-op."""
    if not isinstance(request_id, str) or not request_id or len(request_id) > 128:
        raise ValueError("invalid request ID")
    if type(actual) is not int or not 0 <= actual <= 10**12:
        raise ValueError("actual must be bounded integer microdollars")
    conn = connect(path)
    try:
        conn.execute("BEGIN IMMEDIATE")
        row = conn.execute(
            "SELECT actual FROM commands WHERE user_id=? AND request_id=?",
            (user_id, request_id),
        ).fetchone()
        if row is not None and row["actual"] != actual:
            raise ValueError("same request ID has conflicting amount")
        conn.execute("INSERT OR IGNORE INTO commands VALUES (?, ?, ?)",
                     (user_id, request_id, actual))
        conn.commit()
    except BaseException:
        conn.rollback()
        raise
    finally:
        conn.close()


def settle(path, request_id, user_id=1, crash=None):
    """Claim + balance delta + settlement + outbox in one SQL transaction.

    Negative balance is allowed intentionally. Admission/reservation is outside
    this experiment. A real command would additionally freeze pricing and usage.
    """
    conn = connect(path)
    try:
        conn.execute("BEGIN IMMEDIATE")
        row = conn.execute(
            "SELECT actual FROM commands WHERE user_id=? AND request_id=?",
            (user_id, request_id),
        ).fetchone()
        if row is None:
            raise ValueError("no durable command")
        inserted = conn.execute(
            "INSERT OR IGNORE INTO settlements VALUES (?, ?, ?)",
            (user_id, request_id, row["actual"]),
        ).rowcount
        if not inserted:
            conn.commit()
            return False
        conn.execute("UPDATE accounts SET balance=balance-? WHERE user_id=?",
                     (row["actual"], user_id))
        if crash == "before_commit":
            os._exit(71)
        conn.execute(
            "INSERT INTO outbox(user_id, request_id, delta) VALUES (?, ?, ?)",
            (user_id, request_id, -row["actual"]),
        )
        conn.commit()
        if crash == "after_commit":
            os._exit(72)
        return True
    except BaseException:
        conn.rollback()
        raise
    finally:
        conn.close()


def inspect(path):
    conn = connect(path)
    try:
        return {
            "balance_micro_usd": conn.execute(
                "SELECT balance FROM accounts WHERE user_id=1").fetchone()[0],
            "command_count": conn.execute("SELECT COUNT(*) FROM commands").fetchone()[0],
            "settlement_count": conn.execute("SELECT COUNT(*) FROM settlements").fetchone()[0],
            "pending_commands": [dict(row) for row in conn.execute("""
                SELECT c.* FROM commands c LEFT JOIN settlements s
                ON c.user_id=s.user_id AND c.request_id=s.request_id
                WHERE s.request_id IS NULL ORDER BY c.user_id, c.request_id""")],
            "pending_events": [dict(row) for row in conn.execute(
                "SELECT * FROM outbox WHERE delivered=0 ORDER BY event_id")],
        }
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["demo", "inspect", "settle"])
    parser.add_argument("--db", required=True)
    parser.add_argument("--request", default="demo-A")
    parser.add_argument("--crash", choices=["before_commit", "after_commit"])
    args = parser.parse_args()
    if args.action == "demo":
        if Path(args.db).exists():
            parser.error("demo requires a new database path; existing files are never reset")
        initialize(args.db)
        enqueue(args.db, "demo-A", 1_500_000)
        settle(args.db, "demo-A")
        settle(args.db, "demo-A")
    elif args.action == "settle":
        settle(args.db, args.request, crash=args.crash)
    print(json.dumps(inspect(args.db), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
