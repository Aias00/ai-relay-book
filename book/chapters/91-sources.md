# 附录 B：固定源码与结论边界

三个项目均于 2026-10-27 从本地干净工作区读取，提交已通过各自上游 GitHub API 确认存在。下列链接固定到提交，不跟随 main。`book/sources.json` 保存逐文件 SHA-256，供后续复核。源码阅读未运行三个网关、真实供应商或其完整测试套件。

## N：new-api

固定提交：`34003e9c2eed2c20e617f583fdfe54bf1bf42237`。

支持第 2、3、7、8 章：预扣入口、计价与请求快照、钱包原子扣减、会话内状态、订阅初始记录和差额结算。普通聊天结论不覆盖全部 WebSocket 与任务入口；订阅退款的独立事务调用只是源码观察，未通过三数据库故障注入验证。

- [controller/relay.go](https://github.com/QuantumNous/new-api/blob/34003e9c2eed2c20e617f583fdfe54bf1bf42237/controller/relay.go)
- [relay/request_billing.go](https://github.com/QuantumNous/new-api/blob/34003e9c2eed2c20e617f583fdfe54bf1bf42237/relay/request_billing.go)
- [relay/helper/price.go](https://github.com/QuantumNous/new-api/blob/34003e9c2eed2c20e617f583fdfe54bf1bf42237/relay/helper/price.go)
- [relay/compatible_handler.go](https://github.com/QuantumNous/new-api/blob/34003e9c2eed2c20e617f583fdfe54bf1bf42237/relay/compatible_handler.go)
- [service/token_counter.go](https://github.com/QuantumNous/new-api/blob/34003e9c2eed2c20e617f583fdfe54bf1bf42237/service/token_counter.go)
- [service/billing_session.go](https://github.com/QuantumNous/new-api/blob/34003e9c2eed2c20e617f583fdfe54bf1bf42237/service/billing_session.go)
- [service/funding_source.go](https://github.com/QuantumNous/new-api/blob/34003e9c2eed2c20e617f583fdfe54bf1bf42237/service/funding_source.go)
- [service/text_quota.go](https://github.com/QuantumNous/new-api/blob/34003e9c2eed2c20e617f583fdfe54bf1bf42237/service/text_quota.go)
- [service/tiered_settle.go](https://github.com/QuantumNous/new-api/blob/34003e9c2eed2c20e617f583fdfe54bf1bf42237/service/tiered_settle.go)
- [service/task_billing.go](https://github.com/QuantumNous/new-api/blob/34003e9c2eed2c20e617f583fdfe54bf1bf42237/service/task_billing.go)
- [model/quota_reserve.go](https://github.com/QuantumNous/new-api/blob/34003e9c2eed2c20e617f583fdfe54bf1bf42237/model/quota_reserve.go)
- [model/user.go](https://github.com/QuantumNous/new-api/blob/34003e9c2eed2c20e617f583fdfe54bf1bf42237/model/user.go)
- [model/subscription.go](https://github.com/QuantumNous/new-api/blob/34003e9c2eed2c20e617f583fdfe54bf1bf42237/model/subscription.go)
- [model/utils.go](https://github.com/QuantumNous/new-api/blob/34003e9c2eed2c20e617f583fdfe54bf1bf42237/model/utils.go)
- [pkg/billingexpr/expr.md](https://github.com/QuantumNous/new-api/blob/34003e9c2eed2c20e617f583fdfe54bf1bf42237/pkg/billingexpr/expr.md)
- [setting/operation_setting/quota_setting.go](https://github.com/QuantumNous/new-api/blob/34003e9c2eed2c20e617f583fdfe54bf1bf42237/setting/operation_setting/quota_setting.go)

## S：sub2api

固定提交：`7da09cab4e875463baa79fc150adde700c5438df`。

支持第 2、4、9 章：用户/账户并发、普通钱包与固定金额 scope 预留、UUID、TTL、引用交接、worker 与数据库去重。普通聊天结论不覆盖独立批量图片 hold/recovery；未对 Redis 故障转移和数据库峰值吞吐实测。

- [backend/internal/handler/gateway_handler.go](https://github.com/Wei-Shaw/sub2api/blob/7da09cab4e875463baa79fc150adde700c5438df/backend/internal/handler/gateway_handler.go)
- [backend/internal/handler/failover_loop.go](https://github.com/Wei-Shaw/sub2api/blob/7da09cab4e875463baa79fc150adde700c5438df/backend/internal/handler/failover_loop.go)
- [backend/internal/service/concurrency_service.go](https://github.com/Wei-Shaw/sub2api/blob/7da09cab4e875463baa79fc150adde700c5438df/backend/internal/service/concurrency_service.go)
- [backend/internal/service/billing_inflight_reservation.go](https://github.com/Wei-Shaw/sub2api/blob/7da09cab4e875463baa79fc150adde700c5438df/backend/internal/service/billing_inflight_reservation.go)
- [backend/internal/repository/billing_inflight_cache.go](https://github.com/Wei-Shaw/sub2api/blob/7da09cab4e875463baa79fc150adde700c5438df/backend/internal/repository/billing_inflight_cache.go)
- [backend/internal/service/billing_cache_service.go](https://github.com/Wei-Shaw/sub2api/blob/7da09cab4e875463baa79fc150adde700c5438df/backend/internal/service/billing_cache_service.go)
- [backend/internal/service/gateway_usage_billing.go](https://github.com/Wei-Shaw/sub2api/blob/7da09cab4e875463baa79fc150adde700c5438df/backend/internal/service/gateway_usage_billing.go)
- [backend/internal/service/usage_record_worker_pool.go](https://github.com/Wei-Shaw/sub2api/blob/7da09cab4e875463baa79fc150adde700c5438df/backend/internal/service/usage_record_worker_pool.go)
- [backend/internal/repository/usage_billing_repo.go](https://github.com/Wei-Shaw/sub2api/blob/7da09cab4e875463baa79fc150adde700c5438df/backend/internal/repository/usage_billing_repo.go)
- [backend/internal/config/config.go](https://github.com/Wei-Shaw/sub2api/blob/7da09cab4e875463baa79fc150adde700c5438df/backend/internal/config/config.go)

## R：9router

固定提交：`87a74e1bda3677193c6f71a7e2100c90311f0689`。

支持第 2—5、10 章：宿主入口、转换器、连接与组合回退、SSE 错误处理、SQLite usage 历史与统计。对用户钱包链路的判断限定于列出的聊天、Key 和 usage 路径；不把 README 的节省比例或文档界面示例作为计费能力和性能证明。

- [src/app/api/v1/chat/completions/route.js](https://github.com/decolua/9router/blob/87a74e1bda3677193c6f71a7e2100c90311f0689/src/app/api/v1/chat/completions/route.js)
- [src/sse/handlers/chat.js](https://github.com/decolua/9router/blob/87a74e1bda3677193c6f71a7e2100c90311f0689/src/sse/handlers/chat.js)
- [src/sse/services/auth.js](https://github.com/decolua/9router/blob/87a74e1bda3677193c6f71a7e2100c90311f0689/src/sse/services/auth.js)
- [open-sse/handlers/chatCore.js](https://github.com/decolua/9router/blob/87a74e1bda3677193c6f71a7e2100c90311f0689/open-sse/handlers/chatCore.js)
- [open-sse/handlers/chatCore/streamingHandler.js](https://github.com/decolua/9router/blob/87a74e1bda3677193c6f71a7e2100c90311f0689/open-sse/handlers/chatCore/streamingHandler.js)
- [open-sse/utils/streamHandler.js](https://github.com/decolua/9router/blob/87a74e1bda3677193c6f71a7e2100c90311f0689/open-sse/utils/streamHandler.js)
- [open-sse/translator/index.js](https://github.com/decolua/9router/blob/87a74e1bda3677193c6f71a7e2100c90311f0689/open-sse/translator/index.js)
- [open-sse/services/combo.js](https://github.com/decolua/9router/blob/87a74e1bda3677193c6f71a7e2100c90311f0689/open-sse/services/combo.js)
- [open-sse/services/accountFallback.js](https://github.com/decolua/9router/blob/87a74e1bda3677193c6f71a7e2100c90311f0689/open-sse/services/accountFallback.js)
- [open-sse/services/usage.js](https://github.com/decolua/9router/blob/87a74e1bda3677193c6f71a7e2100c90311f0689/open-sse/services/usage.js)
- [open-sse/providers/pricing.js](https://github.com/decolua/9router/blob/87a74e1bda3677193c6f71a7e2100c90311f0689/open-sse/providers/pricing.js)
- [src/lib/db/repos/usageRepo.js](https://github.com/decolua/9router/blob/87a74e1bda3677193c6f71a7e2100c90311f0689/src/lib/db/repos/usageRepo.js)
- [src/lib/db/repos/apiKeysRepo.js](https://github.com/decolua/9router/blob/87a74e1bda3677193c6f71a7e2100c90311f0689/src/lib/db/repos/apiKeysRepo.js)
- [src/lib/db/schema.js](https://github.com/decolua/9router/blob/87a74e1bda3677193c6f71a7e2100c90311f0689/src/lib/db/schema.js)
- [src/lib/db/driver.js](https://github.com/decolua/9router/blob/87a74e1bda3677193c6f71a7e2100c90311f0689/src/lib/db/driver.js)

## 本书设计与实验

第 11—13 章是针对有限透支、低延迟与恢复要求提出的设计，不是以上源码的功能宣称。第 14 章的 Python/SQLite 实验代码由本书提供，运行命令和结果范围见实验章与仓库 validation.json。它没有 Redis 消费者、SSE 网络服务、真实价格和供应商取消测试。

随书构建器和阅读样式复用作者自己的 ai-gateway-book；新书书稿、实验和来源清单独立维护。三个第三方项目的名称、署名和代码权利保留给各自作者；本书提供链接与分析，不打包它们的源码或凭据。
