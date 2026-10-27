# 源码核对记录

## N new-api

支持第 2、3、7、8 章：预扣入口、计价与请求快照、钱包原子扣减、会话内状态、订阅初始记录和差额结算。普通聊天结论不覆盖全部 WebSocket 与任务入口；订阅退款的独立事务调用只是源码观察，未通过三数据库故障注入验证。

提交：`34003e9c2eed2c20e617f583fdfe54bf1bf42237`；入口和 SHA-256 见 `book/sources.json`。

## S sub2api

支持第 2、4、9 章：用户/账户并发、普通钱包与固定金额 scope 预留、UUID、TTL、引用交接、worker 与数据库去重。普通聊天结论不覆盖独立批量图片 hold/recovery；未对 Redis 故障转移和数据库峰值吞吐实测。

提交：`7da09cab4e875463baa79fc150adde700c5438df`；入口和 SHA-256 见 `book/sources.json`。

## R 9router

支持第 2—5、10 章：宿主入口、转换器、连接与组合回退、SSE 错误处理、SQLite usage 历史与统计。对用户钱包链路的判断限定于列出的聊天、Key 和 usage 路径；不把 README 的节省比例或文档界面示例作为计费能力和性能证明。

提交：`87a74e1bda3677193c6f71a7e2100c90311f0689`；入口和 SHA-256 见 `book/sources.json`。

未作性能排名，未把业务推断计为实测。所有建议费率和阈值为教学假设。
