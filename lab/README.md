# 持久结算实验

仅使用 Python 3.10+ 标准库和真实 SQLite 文件，不安装三个上游项目，不请求模型、不需要 API Key。

```sh
python3 -m unittest discover -s tests -v
python3 -m lab.ledger demo --db /tmp/relay-ledger-demo.sqlite
python3 -m lab.ledger inspect --db /tmp/relay-ledger-demo.sqlite
```

demo 要求路径不存在；若已经运行过，请换一个文件名，不会自动删除旧数据库。初始余额 10 美元，重复处理同一笔 1.5 美元消费，最终为 8.5 美元，一个结算记录和一个待投递 outbox 事件。所有金额单位为微美元。

测试覆盖两个独立进程更新同账户、重复投递、请求金额冲突、提交前 `os._exit`、提交后 `os._exit` 与重复处理、负费用拒绝和实际透支。crash 选项仅用于一次性实验进程，不应在生产进程使用。

实验不实现 Redis、预留、流式估算、价格引擎、缓存消费者或自动对账。outbox 保持 pending 是为了让读者观察恢复证据；未实现消费者确认，不代表事件已到达真实缓存。SQLite 单写者行为不能推导 PostgreSQL/MySQL、Redis Cluster 或跨机器文件系统的正确性。第 14 章说明每条断言及其范围。
