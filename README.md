# AI 中转站工程

**new-api、sub2api 与 9router 源码对照：路由、流式响应与低延迟计费。** 作者 Aias00。

[在线阅读](https://aias00.github.io/ai-relay-book/) · [下载 EPUB](https://aias00.github.io/ai-relay-book/downloads/ai-relay-book.epub) · [完整书稿](https://aias00.github.io/ai-relay-book/downloads/book.md) · [离线 HTML](https://aias00.github.io/ai-relay-book/downloads/ai-relay-book.html)

一本面向后端开发者的独立中文工程书。围绕真实中转站请求，解释协议转换、账户与模型路由、SSE 生命周期、预扣和预留、多进程结算、有限透支下的分段预算以及故障恢复。包括 16 章正文、前言、练习参考、固定源码来源、术语表，以及自动生成的实验代码附录。

## 目录

1. AI 中转站到底管理什么
2. 沿三个工程追踪一次请求
3. 协议兼容不能只看文本是否出来
4. 路由选择的是能力与资源
5. SSE 输出开始以后，错误处理就变了
6. 失败切换不等于安全重放
7. 先统一计量，再计算价格
8. new-api 的预扣、订阅记录与差额结算
9. sub2api 的在途预留与事务后扣
10. 9router 的配额追踪不是用户钱包
11. 允许少量欠费时，怎样缩短准入路径
12. 长请求按段追加预算
13. 多进程扣费与跨存储恢复
14. 运行一个可崩溃的结算实验
15. 用指标和故障窗口控制上线
16. 选择基础工程与实施顺序

## 来源与结论范围

本书固定读取以下版本，读取日期为 2026-10-27。来源清单包含 41 个文件的固定提交链接与 SHA-256，见 [book/sources.json](book/sources.json) 和[来源附录](book/chapters/91-sources.md)。

| 工程 | 提交 |
| --- | --- |
| [QuantumNous/new-api](https://github.com/QuantumNous/new-api) | `34003e9c2eed2c20e617f583fdfe54bf1bf42237` |
| [Wei-Shaw/sub2api](https://github.com/Wei-Shaw/sub2api) | `7da09cab4e875463baa79fc150adde700c5438df` |
| [decolua/9router](https://github.com/decolua/9router) | `87a74e1bda3677193c6f71a7e2100c90311f0689` |

源码观察、建议设计和本书实验分开陈述：没有运行三个工程的完整测试套件、真实模型请求或性能压测。不会把成本统计当作钱包、把 Redis 原子操作当作跨存储事务、把 TTL 到期当作供应商未收费的证明。所有金额示例与预算阈值都是教学假设。

## 运行实验

Python 3.10+，仅标准库；使用真实 SQLite 文件与独立进程，不需要模型凭据或 Redis。

```sh
python3 -m unittest discover -s tests -v
python3 -m lab.ledger demo --db /tmp/relay-ledger-demo.sqlite
python3 -m lab.ledger inspect --db /tmp/relay-ledger-demo.sqlite
```

demo 使用新文件，已有路径不会被覆盖。六项测试验证同账户多进程扣款、重复投递、金额冲突、提交前崩溃、提交后崩溃与恢复、负费用拒绝和实际透支。详见 [lab/README.md](lab/README.md) 与[实验章节](book/chapters/14-ledger-lab.md)。实验不实现 Redis 消费者、分段预留或真实 SSE；这些仍属于设计和待验收项。

## 在线阅读与构建

在线页面、EPUB、离线 HTML 和完整 Markdown 都从 `book/chapters/` 构建。阅读器支持全文搜索、章节目录、前后翻页、字号、浅深色主题、阅读位置和移动端；禁用 JavaScript 仍可阅读正文。

需要 Pandoc 3.12.1、Python 3.10+。EPUBCheck 需要 Java 17+。

```sh
python3 scripts/build.py
python3 scripts/verify.py
sh scripts/epubcheck.sh
python3 -m http.server 8767 --bind 127.0.0.1 --directory site
```

GitHub Actions 在每次推送 main 时运行实验、构建、逐章一致性检查、EPUBCheck 和浏览器验收，通过后发布 GitHub Pages。构建产物不提交仓库。浏览器验收与发布细节见 [scripts/README.md](scripts/README.md)。

## 作者与权利

© 2026 Aias00。原创书稿与实验保留所有权利。本书使用 AI 辅助源码阅读、写作与验证；结论范围和可运行证据随书提供。第三方项目及其署名归原作者所有，本仓库不打包其源码、凭据或商标素材。

阅读器和出版脚本复用作者自己的 [ai-gateway-book](https://github.com/Aias00/ai-gateway-book)，本书正文、实验、来源和发布仓库独立维护。
