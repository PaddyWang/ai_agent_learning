# 60天 AI Agent 转岗打卡文档（杭州 / Python）

开始方式：
- 如果你从 `2026-04-03` 才开始，建议把 `第1天` 和 `第2天` 合并到本周末补掉。
- 每天按 6 个固定栏目执行：`今天要学会的知识`、`今天不用深挖的内容`、`今天学完后你应该能回答的问题`、`今天的完成标准`、`今天的学习顺序`、`实操版清单`。

每日固定动作：
- [ ] 看完当天指定链接
- [ ] 完成当天编码目标
- [ ] 至少 1 次 commit
- [ ] 写 5 条学习笔记
- [ ] 写 1 条可放进简历的项目 bullet

---

## 第1天：FastAPI First Steps + Pydantic Models
- 今天要学会的知识：`FastAPI()` 应用实例、`@app.get()` 路由注册、JSON 响应、`/docs`、`BaseModel`、字段类型、默认值、`model_dump()`
- 今天不用深挖的内容：`validators`、嵌套模型、严格模式、复杂依赖注入
- 今天学完后你应该能回答的问题：为什么 FastAPI 返回 `dict` 会变成 JSON？`BaseModel` 和普通 `dict` 的区别是什么？为什么健康检查也值得定义 `response_model`？
- 今天的完成标准：`uv + ruff + pytest + pre-commit` 初始化完成；`/health` 可访问；`/docs` 可访问
- 今天的学习顺序：[FastAPI First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/) -> [Pydantic Models](https://docs.pydantic.dev/latest/concepts/models/)
- 实操版清单：初始化项目；创建 `main.py`；定义 `HealthResponse`；实现 `/health`；配置 `ruff`、`pytest`、`pre-commit`

## 第2天：Request Body + Validators
- 今天要学会的知识：请求体解析、`BaseModel` 作为入参、字段校验、常见类型转换、接口入参与出参拆分
- 今天不用深挖的内容：复杂联合类型、自定义 validator 高级写法、泛型模型
- 今天学完后你应该能回答的问题：为什么请求体要单独定义 schema？Pydantic 为什么会发生类型转换？什么时候需要把创建请求和返回响应拆成两个模型？
- 今天的完成标准：完成 `UserCreate`、`ChatRequest`、`ChatResponse` 三组 schema；新增 `POST /chat` 的最小实现
- 今天的学习顺序：[FastAPI Request Body](https://fastapi.tiangolo.com/tutorial/body/) -> [Pydantic Validators](https://docs.pydantic.dev/latest/concepts/validators/)
- 实操版清单：补 `schemas.py`；为 `/chat` 增加入参校验；补 2 个错误请求测试；记录 3 个常见校验错误

## 第3天：Dependencies + Serialization
- 今天要学会的知识：依赖注入的基本用法、公共逻辑抽取、`model_dump()`、响应序列化、接口层与业务层分离
- 今天不用深挖的内容：带 yield 的依赖、复杂依赖树、自定义序列化器
- 今天学完后你应该能回答的问题：什么逻辑适合放在 `Depends` 里？为什么说 Pydantic 模型比裸字典更适合接口边界？
- 今天的完成标准：抽出一个公共依赖；完成 `/users/me` 或 `/messages` 示例接口；能稳定返回 schema 化 JSON
- 今天的学习顺序：[FastAPI Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/) -> [Pydantic Serialization](https://docs.pydantic.dev/latest/concepts/serialization/)
- 实操版清单：创建 `deps.py`；把公共 header 或 mock user 提取为依赖；把响应统一改为 `response_model`

## 第4天：Testing 基础
- 今天要学会的知识：`pytest` 基础、FastAPI `TestClient`、接口级测试、测试命名和最小断言集
- 今天不用深挖的内容：复杂 fixture、端到端测试、覆盖率平台集成
- 今天学完后你应该能回答的问题：为什么接口项目必须尽早补测试？一个健康检查接口最少应该断言什么？
- 今天的完成标准：至少新增 5 个测试；覆盖健康检查、创建请求、异常分支
- 今天的学习顺序：[FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/) -> [fastapi/fastapi](https://github.com/fastapi/fastapi)
- 实操版清单：创建 `tests/`；写 `test_health.py`；给 `/chat` 补成功和失败测试；让 `pytest` 能本地跑通

## 第5天：Security 入门
- 今天要学会的知识：鉴权基本概念、Bearer Token、最小登录流程、项目目录拆分
- 今天不用深挖的内容：OAuth2 全套细节、刷新令牌、RBAC 复杂模型
- 今天学完后你应该能回答的问题：JWT 在项目里的作用是什么？哪些接口应该从一开始就要求鉴权？
- 今天的完成标准：完成一个最小登录接口；完成一个需要鉴权的受保护接口
- 今天的学习顺序：[FastAPI Simple OAuth2](https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/) -> [Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- 实操版清单：拆 `routers/`、`schemas/`、`services/`；新增 `/login`；新增 `get_current_user` 依赖；保护 `/users/me`

## 第6天：StreamingResponse + SSE
- 今天要学会的知识：流式响应、SSE 基本格式、AI 对话为什么适合流式输出、同步响应和流式响应的区别
- 今天不用深挖的内容：WebSocket、浏览器重连机制、复杂事件协议
- 今天学完后你应该能回答的问题：为什么 AI 聊天常用 SSE 而不是普通 JSON 响应？什么时候应该优先做流式接口？
- 今天的完成标准：做出 `/chat/stream`；前端或 curl 可以看到逐段返回
- 今天的学习顺序：[Custom Response / StreamingResponse](https://fastapi.tiangolo.com/advanced/custom-response/) -> [Server-Sent Events](https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse)
- 实操版清单：写生成器函数；返回 `StreamingResponse`；模拟逐 token 输出；记录响应耗时

## 第7天：Background Tasks + CORS
- 今天要学会的知识：后台任务、日志异步写入、跨域配置、开发态前后端联调要点
- 今天不用深挖的内容：任务队列系统、复杂跨域白名单、消息中间件
- 今天学完后你应该能回答的问题：什么场景适合 `BackgroundTasks`？为什么前后端分离开发一定会遇到 CORS？
- 今天的完成标准：完成一次异步日志落盘；本地前端能调用接口不报跨域错误；Week1 README 完成
- 今天的学习顺序：[Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/) -> [CORS](https://fastapi.tiangolo.com/tutorial/cors/)
- 实操版清单：接一个日志后台任务；配置允许本地前端域名；整理 Week1 功能清单与目录结构

## 第8天：SQLAlchemy Unified Tutorial 入门
- 今天要学会的知识：Engine、Session、ORM 模型、数据库连接、事务的最小概念
- 今天不用深挖的内容：复杂 join、事件系统、分布式事务
- 今天学完后你应该能回答的问题：ORM 模型和 Pydantic 模型分别解决什么问题？为什么数据库访问需要 Session？
- 今天的完成标准：建 `Session`、`Message`、`Task` 三张 ORM 表
- 今天的学习顺序：[SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/20/tutorial/index.html) -> [Working with Transactions and the DBAPI](https://docs.sqlalchemy.org/20/tutorial/dbapi_transactions.html)
- 实操版清单：创建 `db.py`；定义 Base；写 3 个 ORM 模型；连上本地数据库

## 第9天：CRUD + Relationship
- 今天要学会的知识：增删改查、模型关系、一对多、基础查询抽象
- 今天不用深挖的内容：复杂多对多、延迟加载策略、ORM 高级优化
- 今天学完后你应该能回答的问题：为什么要抽 repository 层？`Session` 和 `Message` 为什么天然是一对多？
- 今天的完成标准：写出 `create_session`、`create_message`、`list_messages`
- 今天的学习顺序：[SQLAlchemy Working with Data](https://docs.sqlalchemy.org/20/tutorial/data.html) -> [Relationship Configuration](https://docs.sqlalchemy.org/en/20/orm/relationships.html)
- 实操版清单：新增 `repositories/`；补 3 个 CRUD；让接口读写真库而不是 mock 数据

## 第10天：AsyncSession
- 今天要学会的知识：异步数据库访问、`AsyncSession`、依赖注入数据库会话、接口层如何安全使用 db session
- 今天不用深挖的内容：连接池细节、同步/异步混用陷阱深挖
- 今天学完后你应该能回答的问题：FastAPI 项目里为什么很多人会选择异步数据库驱动？数据库 Session 为什么适合通过依赖注入管理？
- 今天的完成标准：完成 `AsyncSession` 版本数据访问层；接口切换到异步数据库访问
- 今天的学习顺序：[SQLAlchemy asyncio](https://docs.sqlalchemy.org/20/orm/extensions/asyncio.html) -> [FastAPI SQL Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- 实操版清单：把 db 连接改成 async；实现 `get_db`；让 `/chat`、`/sessions` 走异步读写

## 第11天：Alembic 迁移
- 今天要学会的知识：数据库迁移的意义、初始化迁移、自动生成 migration、升级/回滚的最小流程
- 今天不用深挖的内容：分支迁移冲突、复杂数据迁移、线上灰度迁移
- 今天学完后你应该能回答的问题：为什么真实项目不能只靠 `create_all()`？迁移文件为什么也属于代码资产？
- 今天的完成标准：初始化 Alembic；生成并执行第一版迁移；数据库 schema 可复现
- 今天的学习顺序：[Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html) -> [Alembic Autogenerate](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)
- 实操版清单：执行 `alembic init`；配置数据库 URL；生成初始 migration；运行 upgrade

## 第12天：PostgreSQL 基础
- 今天要学会的知识：PostgreSQL 基础语法、索引、分页、`jsonb` 的用途
- 今天不用深挖的内容：复杂查询优化、分区表、存储过程
- 今天学完后你应该能回答的问题：为什么 AI 应用很适合用 `jsonb` 存 metadata？什么时候要给消息表加索引？
- 今天的完成标准：为消息或任务表增加索引；加入一个 `jsonb` 字段保存扩展元数据
- 今天的学习顺序：[PostgreSQL Tutorial](https://www.postgresql.org/docs/current/tutorial.html) -> [PostgreSQL JSON Types](https://www.postgresql.org/docs/current/datatype-json.html)
- 实操版清单：补 migration；加 `created_at`、`metadata`；验证分页和排序

## 第13天：Redis 基础
- 今天要学会的知识：Redis 用途、缓存、会话存储、限流思路、过期时间
- 今天不用深挖的内容：Redis Stream、集群、Lua 脚本
- 今天学完后你应该能回答的问题：为什么 AI 应用离不开缓存？哪些数据适合放 Redis，哪些不适合？
- 今天的完成标准：做出 1 个缓存点和 1 个简单限流点
- 今天的学习顺序：[redis-py Guide](https://redis.io/docs/latest/develop/clients/redis-py/) -> [Pipelines and Transactions](https://redis.io/docs/latest/develop/clients/redis-py/transpipe/)
- 实操版清单：接入 Redis 客户端；缓存健康检查或会话列表；给 `/chat` 增加简单限流

## 第14天：Docker + Compose
- 今天要学会的知识：镜像、容器、Dockerfile、Compose、服务编排
- 今天不用深挖的内容：镜像优化高级技巧、Kubernetes、生产级安全
- 今天学完后你应该能回答的问题：为什么后端项目要尽早容器化？Compose 相比手工启动服务的价值是什么？
- 今天的完成标准：`FastAPI + PostgreSQL + Redis` 一键启动
- 今天的学习顺序：[Docker Introduction](https://docs.docker.com/get-started/introduction/) -> [Containerize a Python Application](https://docs.docker.com/guides/python/containerize/) -> [Docker Compose Quickstart](https://docs.docker.com/compose/gettingstarted/)
- 实操版清单：写 `Dockerfile`；写 `docker-compose.yml`；容器内跑服务；更新 README 启动方式

## 第15天：Responses API / 统一模型网关
- 今天要学会的知识：模型调用抽象、统一 provider 层、`Responses API` 的定位、请求与响应边界
- 今天不用深挖的内容：多模态、高级会话管理、复杂工具链
- 今天学完后你应该能回答的问题：为什么项目里最好不要把模型 SDK 调用散落在业务代码里？统一网关层解决了什么问题？
- 今天的完成标准：封装一个 `LLM Gateway`，至少支持 1 个模型提供商
- 今天的学习顺序：[Migrate to Responses API](https://platform.openai.com/docs/guides/migrate-to-responses) -> [Function Calling](https://platform.openai.com/docs/guides/function-calling?api-mode=responses)
- 实操版清单：创建 `llm/` 目录；定义 provider 接口；抽出统一请求参数；记录 token/耗时

## 第16天：Structured Outputs
- 今天要学会的知识：结构化输出、JSON Schema、Pydantic schema 对接 LLM 输出、为什么前端喜欢稳定 JSON
- 今天不用深挖的内容：复杂嵌套 schema、深层容错策略
- 今天学完后你应该能回答的问题：为什么智能体结果最好不是纯文本？结构化输出如何减少前端解析成本？
- 今天的完成标准：完成一个结构化抽取接口，稳定返回符合 schema 的 JSON
- 今天的学习顺序：[Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs?api-mode=chat) -> [Pydantic JSON Schema](https://docs.pydantic.dev/latest/concepts/json_schema/)
- 实操版清单：定义 `ExtractionResult`；让模型返回结构化 JSON；为非法 JSON 增加兜底

## 第17天：Tools / File Search 认知
- 今天要学会的知识：Tools 的概念、托管检索和自建 RAG 的区别、工具调用场景边界
- 今天不用深挖的内容：托管工具的细节限制、企业级权限集成
- 今天学完后你应该能回答的问题：什么时候应该直接用托管 File Search？什么时候一定要自己做 RAG？
- 今天的完成标准：写一篇 500 字对比笔记，说明“托管检索 vs 自建 RAG”的取舍
- 今天的学习顺序：[Using Tools](https://platform.openai.com/docs/guides/tools?api-mode=responses) -> [File Search](https://platform.openai.com/docs/guides/tools-file-search)
- 实操版清单：整理优缺点表；补 1 张架构草图；明确你后面 45 天主线坚持“自建 RAG + 可控工程”

## 第18天：文档解析与向量写入
- 今天要学会的知识：文档 ingestion、chunk 的意义、embedding 的位置、向量写入流程
- 今天不用深挖的内容：embedding 模型评测、复杂分块算法
- 今天学完后你应该能回答的问题：为什么 RAG 不是“传文件给模型就完了”？为什么 chunk 质量会直接影响召回效果？
- 今天的完成标准：支持 `PDF/Markdown/CSV` 文档切块与向量写入
- 今天的学习顺序：[Qdrant Essentials](https://qdrant.tech/course/essentials/) -> [qdrant-client](https://github.com/qdrant/qdrant-client)
- 实操版清单：写 `ingest.py`；抽取文档文本；按段落或标题切块；写入向量库

## 第19天：Hybrid Search
- 今天要学会的知识：dense retrieval、sparse retrieval、混合检索、召回率提升思路
- 今天不用深挖的内容：复杂 reranker、训练自定义 sparse encoder
- 今天学完后你应该能回答的问题：纯向量检索为什么会漏召回？混合检索在中文业务场景里为什么很常见？
- 今天的完成标准：做出 dense + sparse 的混合检索实验
- 今天的学习顺序：[Hybrid Search](https://qdrant.tech/course/essentials/day-3/hybrid-search/) -> [Hybrid Search Demo](https://qdrant.tech/course/essentials/day-3/hybrid-search-demo/)
- 实操版清单：新增检索策略枚举；对比 3 个问题的召回差异；记录命中情况

## 第20天：Rerank
- 今天要学会的知识：重排的作用、召回与排序的区别、为什么“先多找再重排”常见
- 今天不用深挖的内容：训练 rerank 模型、复杂在线评测体系
- 今天学完后你应该能回答的问题：为什么 topK 召回后还要 rerank？RAG 系统里最常见的两个错误是什么？
- 今天的完成标准：给 RAG 链路加一个 rerank 步骤
- 今天的学习顺序：[Hybrid Queries](https://qdrant.tech/documentation/concepts/hybrid-queries/) -> [Hybrid Search with Reranking](https://qdrant.tech/documentation/advanced-tutorials/reranking-hybrid-search/)
- 实操版清单：实现召回结果排序；输出分数；对比开启/关闭 rerank 的差异

## 第21天：RAG v1 收口
- 今天要学会的知识：引用来源、metadata、RAG 基础评测、最小可演示产品思维
- 今天不用深挖的内容：自动评测平台、复杂观测平台
- 今天学完后你应该能回答的问题：为什么 RAG 回答一定要带引用？怎么判断一个 RAG demo 已经达到了“可展示”的水平？
- 今天的完成标准：完成 `rag-lab v1`，支持上传文档、提问、展示引用来源
- 今天的学习顺序：[Manage Knowledge Content](https://docs.dify.ai/en/use-dify/knowledge/manage-knowledge/maintain-knowledge-documents) -> [Qdrant Essentials](https://qdrant.tech/course/essentials/)
- 实操版清单：做上传页；做引用来源卡片；补 10 条测试问题；录 2 分钟演示

## 第22天：LangGraph 概念入门
- 今天要学会的知识：graph orchestration、state、node、edge、为什么 Agent 系统适合图编排
- 今天不用深挖的内容：持久化执行、高级 checkpoint、复杂子图
- 今天学完后你应该能回答的问题：LangGraph 相比“一个大函数串起来”解决了什么问题？什么叫状态驱动的工作流？
- 今天的完成标准：画出最小 graph 结构并跑通 demo
- 今天的学习顺序：[LangGraph Overview](https://docs.langchain.com/oss/python/langgraph/overview) -> [Introduction to LangGraph](https://academy.langchain.com/courses/intro-to-langgraph)
- 实操版清单：建立 `project-a/`；写最小 graph；让节点按顺序执行并打印结果

## 第23天：State / Node / Edge
- 今天要学会的知识：状态 schema、节点输入输出、条件路由、memory 的最小概念
- 今天不用深挖的内容：复杂循环控制、多分支恢复
- 今天学完后你应该能回答的问题：节点为什么不应该互相“偷改”数据？为什么 state schema 对多人协作很重要？
- 今天的完成标准：实现 `state / node / edge / router / memory` 基础版本
- 今天的学习顺序：[Introduction to LangGraph](https://academy.langchain.com/courses/intro-to-langgraph) -> [LangGraph Essentials Python](https://academy.langchain.com/courses/langgraph-essentials-python)
- 实操版清单：定义 `AgentState`；做条件分支；写 1 个 summary memory

## 第24天：Tool Calling 节点
- 今天要学会的知识：工具节点设计、tool schema、agent loop 的最小形态
- 今天不用深挖的内容：复杂 planning 算法、多工具冲突调度
- 今天学完后你应该能回答的问题：为什么工具调用要显式 schema？普通函数和 agent tool 的差异是什么？
- 今天的完成标准：实现一个带工具调用的 graph
- 今天的学习顺序：[Introduction to LangChain - Python](https://academy.langchain.com/courses/foundation-introduction-to-langchain-python) -> [LangGraph Overview](https://docs.langchain.com/oss/python/langgraph/overview)
- 实操版清单：写 2 个工具；把工具接到 graph；输出工具调用日志

## 第25天：项目A 骨架
- 今天要学会的知识：项目拆分、前后端目录、路由组织、可维护工程结构
- 今天不用深挖的内容：完整设计系统、微前端
- 今天学完后你应该能回答的问题：一个可投递项目的“骨架”至少需要包含哪些目录和文档？
- 今天的完成标准：项目A骨架完成，前后端结构定型
- 今天的学习顺序：[full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template) -> [Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- 实操版清单：创建前后端目录；拆 routers/services/schemas；写 README 草稿和 `.env.example`

## 第26天：业务工具 1
- 今天要学会的知识：业务工具抽象、商品知识检索、规则检索、工具与 graph 的耦合边界
- 今天不用深挖的内容：复杂商品推荐算法
- 今天学完后你应该能回答的问题：为什么“商品知识检索”和“活动规则检索”应该拆成两个工具？
- 今天的完成标准：完成两个核心工具
- 今天的学习顺序：[Project: Ambient Agents](https://academy.langchain.com/courses/ambient-agents) -> [LangGraph Overview](https://docs.langchain.com/oss/python/langgraph/overview)
- 实操版清单：实现 `search_products`、`search_campaign_rules`；写 tool schema；输出调用日志

## 第27天：结构化营销建议
- 今天要学会的知识：结构化业务输出、前端卡片渲染所需字段、审查节点基础
- 今天不用深挖的内容：内容安全复杂策略、富文本编辑器
- 今天学完后你应该能回答的问题：为什么“直接吐一段营销文案”不如“返回结构化活动建议 + 文案”？
- 今天的完成标准：结构化营销建议 JSON 可在前端渲染
- 今天的学习顺序：[Function Calling](https://platform.openai.com/docs/guides/function-calling?api-mode=responses) -> [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs?api-mode=chat)
- 实操版清单：定义 `CampaignSuggestion` schema；前端渲染卡片；补 3 个异常分支

## 第28天：项目A 收口
- 今天要学会的知识：demo 思维、README 结构、架构图最小集合、录屏脚本
- 今天不用深挖的内容：品牌包装、复杂视觉设计
- 今天学完后你应该能回答的问题：为什么项目必须有 README、架构图和 demo？面试官最关心你项目里的哪三件事？
- 今天的完成标准：项目A 完成 demo、README、架构图、录屏
- 今天的学习顺序：[LangSmith Essentials](https://academy.langchain.com/courses/quickstart-langsmith-essentials) -> [LangGraph Overview](https://docs.langchain.com/oss/python/langgraph/overview)
- 实操版清单：补 README；画架构图；录 3 分钟 demo；写 3 条简历 bullet

## 第29天：Dify 基础认知
- 今天要学会的知识：Dify 的 workflow、knowledge、agent、低代码平台定位
- 今天不用深挖的内容：插件市场、自部署集群
- 今天学完后你应该能回答的问题：Dify 适合解决什么问题？为什么很多企业会同时用“代码方案 + 低代码方案”？
- 今天的完成标准：理解 Dify 基础能力并能口述核心模块
- 今天的学习顺序：[Dify Introduction](https://docs.dify.ai/en/use-dify/getting-started/introduction) -> [langgenius/dify](https://github.com/langgenius/dify)
- 实操版清单：浏览 Dify 核心概念；记录 5 个与你项目相关的能力点；写 1 段技术定位总结

## 第30天：知识库配置策略
- 今天要学会的知识：chunk 设置、TopK、召回策略、知识库维护思路
- 今天不用深挖的内容：大规模知识库治理、复杂版本控制
- 今天学完后你应该能回答的问题：为什么知识库不是“传上去就行”？不同 chunk 策略会如何影响召回？
- 今天的完成标准：写出 chunk 规则、TopK、召回策略对比笔记
- 今天的学习顺序：[Manage Knowledge Settings](https://docs.dify.ai/en/use-dify/knowledge/manage-knowledge/introduction) -> [Manage Knowledge Content](https://docs.dify.ai/en/use-dify/knowledge/manage-knowledge/maintain-knowledge-documents)
- 实操版清单：整理 3 套 chunk 方案；记录优缺点；给项目B 选定默认知识库策略

## 第31天：项目B 立项
- 今天要学会的知识：垂直行业知识库项目如何定义场景、PRD 最小写法、文档 ingestion 方案设计
- 今天不用深挖的内容：全文档工作流编排复杂度
- 今天学完后你应该能回答的问题：为什么项目B 不能只是“另一个 RAG demo”？标书/行业知识助手的关键业务价值是什么？
- 今天的完成标准：项目B PRD 完成，明确 3 个核心场景
- 今天的学习顺序：[Dify Introduction](https://docs.dify.ai/en/use-dify/getting-started/introduction) -> [Qdrant Hybrid Search](https://qdrant.tech/course/essentials/day-3/hybrid-search/)
- 实操版清单：写需求背景；列 3 个核心问题；定义输入输出和引用要求

## 第32天：长文档解析
- 今天要学会的知识：目录切块、表格抽取、长文档结构保留、文档 metadata 设计
- 今天不用深挖的内容：OCR 复杂场景、扫描件精修
- 今天学完后你应该能回答的问题：为什么长文档不能简单按固定长度切？标题层级和页码信息为什么重要？
- 今天的完成标准：完成长文档解析、目录切块、表格抽取
- 今天的学习顺序：[Manage Knowledge Content](https://docs.dify.ai/en/use-dify/knowledge/manage-knowledge/maintain-knowledge-documents) -> [Custom Response](https://fastapi.tiangolo.com/advanced/custom-response/)
- 实操版清单：保留标题路径；提取表格文本；记录页码；补导入日志

## 第33天：项目B RAG 问答
- 今天要学会的知识：引用回溯、答案生成、证据链最小闭环
- 今天不用深挖的内容：复杂证据聚合、自动 fact-check
- 今天学完后你应该能回答的问题：行业知识助手为什么必须强调“依据来自哪里”？什么样的回答算“可交付”？
- 今天的完成标准：完成标书/知识问答、引用回溯、答案生成
- 今天的学习顺序：[Manage Knowledge Content](https://docs.dify.ai/en/use-dify/knowledge/manage-knowledge/maintain-knowledge-documents) -> [LangGraph Overview](https://docs.langchain.com/oss/python/langgraph/overview)
- 实操版清单：实现问答接口；返回引用片段；展示文档页码和标题

## 第34天：技术选型文档
- 今天要学会的知识：技术选型表达、LangGraph vs Dify 的 tradeoff、面试表达思路
- 今天不用深挖的内容：组织级治理和预算决策
- 今天学完后你应该能回答的问题：什么场景优先选 Dify？什么场景优先自己写 LangGraph？
- 今天的完成标准：写完 `LangGraph vs Dify` 技术选型文档
- 今天的学习顺序：[LangGraph Overview](https://docs.langchain.com/oss/python/langgraph/overview) -> [Dify Introduction](https://docs.dify.ai/en/use-dify/getting-started/introduction)
- 实操版清单：至少从开发速度、灵活性、治理、集成、成本 5 个维度对比

## 第35天：项目B 收口
- 今天要学会的知识：权限、审计日志、上传记录、可演示项目的产品补全
- 今天不用深挖的内容：复杂组织权限、多租户平台
- 今天学完后你应该能回答的问题：为什么企业知识库项目离不开权限和审计？哪些日志要留？
- 今天的完成标准：项目B 可演示版完成
- 今天的学习顺序：[FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/) -> [Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/)
- 实操版清单：补上传记录表；补审计日志；补 5 个 smoke test；录 demo

## 第36天：多智能体模式入门
- 今天要学会的知识：`planner / executor / reviewer` 模式、为什么单 Agent 不够、任务拆解最小原则
- 今天不用深挖的内容：复杂 agent 社会学、自动自我纠错高级论文
- 今天学完后你应该能回答的问题：为什么复杂任务适合拆成多角色？每个角色的边界应该怎么定？
- 今天的完成标准：能口述三角色协作模式并画出流程图
- 今天的学习顺序：[Introduction to LangChain - Python](https://academy.langchain.com/courses/foundation-introduction-to-langchain-python) -> [LangGraph Overview](https://docs.langchain.com/oss/python/langgraph/overview)
- 实操版清单：画流程图；定义 3 个角色的输入输出；写项目C PRD 草稿

## 第37天：Deep Agents 认知
- 今天要学会的知识：多步骤任务执行、研究型 Agent 的基本构成、任务分解与回顾
- 今天不用深挖的内容：自动代码修改、复杂子代理编排
- 今天学完后你应该能回答的问题：研究型 Agent 和问答型 Agent 的核心差异是什么？
- 今天的完成标准：做出多步骤任务拆解原型
- 今天的学习顺序：[Project: Deep Agents](https://academy.langchain.com/courses/deep-agents-with-langgraph) -> [Project: Ambient Agents](https://academy.langchain.com/courses/ambient-agents)
- 实操版清单：定义任务列表；写 planner 原型；把任务拆成 3 个步骤并可打印

## 第38天：多任务与子步骤设计
- 今天要学会的知识：子任务、工具选择、失败回退、简单 review 流程
- 今天不用深挖的内容：复杂并行调度、真实子代理基础设施
- 今天学完后你应该能回答的问题：为什么多智能体不等于“越多越好”？失败重试应该放在哪一层？
- 今天的完成标准：完成多步骤任务与 review 思路笔记
- 今天的学习顺序：[Project: Deep Agents](https://academy.langchain.com/courses/deep-agents-with-langgraph) -> [MCP Architecture](https://modelcontextprotocol.io/docs/learn/architecture)
- 实操版清单：列失败场景；设计 review 节点输入输出；补一页 tradeoff 笔记

## 第39天：AkShare 入门
- 今天要学会的知识：金融数据接口、行情/财务/新闻三类数据源、数据 provider 抽象
- 今天不用深挖的内容：量化策略、回测系统
- 今天学完后你应该能回答的问题：为什么金融研究助手不能直接把原始接口暴露给 Agent？provider 层存在的意义是什么？
- 今天的完成标准：接入行情、财务、新闻 3 类数据
- 今天的学习顺序：[AKShare Docs](https://akshare.akfamily.xyz/) -> [akfamily/akshare](https://github.com/akfamily/akshare)
- 实操版清单：试 3 个接口；统一输出 schema；补异常处理和数据为空兜底

## 第40天：金融数据 Provider
- 今天要学会的知识：provider 封装、统一数据格式、字段清洗、时间范围控制
- 今天不用深挖的内容：复杂金融指标计算
- 今天学完后你应该能回答的问题：为什么要把第三方数据先“洗一遍”再给 Agent 用？
- 今天的完成标准：完成金融数据 provider 层
- 今天的学习顺序：[AKShare Docs](https://akshare.akfamily.xyz/) -> [Project: Deep Agents](https://academy.langchain.com/courses/deep-agents-with-langgraph)
- 实操版清单：实现 `get_quotes`、`get_financials`、`get_news`；统一 DTO；写 3 个测试

## 第41天：Planner / Executor / Reviewer 落地
- 今天要学会的知识：多角色落地、角色边界、review 的价值、失败回补
- 今天不用深挖的内容：复杂共识机制、长期记忆系统
- 今天学完后你应该能回答的问题：为什么 reviewer 不是可有可无？它最适合检查什么？
- 今天的完成标准：实现三角色流程
- 今天的学习顺序：[LangGraph Overview](https://docs.langchain.com/oss/python/langgraph/overview) -> [Project: Ambient Agents](https://academy.langchain.com/courses/ambient-agents)
- 实操版清单：把项目C 接成 graph；输出每个角色日志；展示最终摘要

## 第42天：项目C 页面完成
- 今天要学会的知识：研究摘要页面、结构化信息展示、项目 demo 组织
- 今天不用深挖的内容：复杂图表系统
- 今天学完后你应该能回答的问题：一个“金融研究助手” demo，最重要的展示信息是什么？
- 今天的完成标准：完成“每日研究摘要”页面
- 今天的学习顺序：[LangSmith Essentials](https://academy.langchain.com/courses/quickstart-langsmith-essentials) -> [Introduction to LangChain - Python](https://academy.langchain.com/courses/foundation-introduction-to-langchain-python)
- 实操版清单：展示摘要、引用、数据来源、任务日志；录 demo

## 第43天：MCP 架构入门
- 今天要学会的知识：MCP 的 `host / client / server / tools / resources / prompts` 概念
- 今天不用深挖的内容：复杂 transport 细节、协议实现细节
- 今天学完后你应该能回答的问题：MCP 解决的是“模型怎么接外部能力”的哪个问题？它和普通 HTTP API 有什么差异？
- 今天的完成标准：能口述 MCP 基本架构
- 今天的学习顺序：[MCP Architecture](https://modelcontextprotocol.io/docs/learn/architecture) -> [Quickstart](https://modelcontextprotocol.io/quickstart)
- 实操版清单：整理术语表；画一张 host-client-server 图；列你要做的 3 个工具

## 第44天：最小 MCP Server
- 今天要学会的知识：MCP Python SDK 用法、最小 server、工具注册
- 今天不用深挖的内容：复杂鉴权、自定义 transport
- 今天学完后你应该能回答的问题：一个最小 MCP Server 至少要提供什么？它是怎么暴露工具的？
- 今天的完成标准：跑通一个最小 MCP Server
- 今天的学习顺序：[MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) -> [MCP Servers](https://github.com/modelcontextprotocol/servers)
- 实操版清单：创建 `mcp_server.py`；注册一个 `time` 工具；本地调试成功

## 第45天：MCP 工具扩展
- 今天要学会的知识：工具 schema、`filesystem / time / db` 三类工具设计
- 今天不用深挖的内容：复杂权限和沙箱隔离
- 今天学完后你应该能回答的问题：为什么 MCP 工具必须强调输入输出 schema？文件系统工具为什么风险更高？
- 今天的完成标准：增加 3 个工具
- 今天的学习顺序：[MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) -> [Function Calling](https://platform.openai.com/docs/guides/function-calling?api-mode=responses)
- 实操版清单：实现 `read_file`、`get_time`、`query_db`；补参数校验；记录错误日志

## 第46天：Agent 接入 MCP
- 今天要学会的知识：Agent 调 MCP 工具、工具发现、工具日志、错误处理
- 今天不用深挖的内容：多 server 编排、复杂协商机制
- 今天学完后你应该能回答的问题：为什么 MCP 能让 Agent 工具接入更标准化？真实项目里接入 MCP 的收益是什么？
- 今天的完成标准：Agent 可调用 MCP 工具完成至少 1 个任务
- 今天的学习顺序：[MCP Servers](https://github.com/modelcontextprotocol/servers) -> [Using Tools](https://platform.openai.com/docs/guides/tools?api-mode=responses)
- 实操版清单：把工具接入项目B 或 C；输出工具调用步骤；补失败重试

## 第47天：Tracing
- 今天要学会的知识：调用链追踪、节点日志、Agent observability 最小方案
- 今天不用深挖的内容：完整可观测平台、自定义 trace 协议
- 今天学完后你应该能回答的问题：为什么 Agent 系统比普通 CRUD 更需要 tracing？出了错应该先看哪几类日志？
- 今天的完成标准：能看到一次完整调用链
- 今天的学习顺序：[LangSmith Essentials](https://academy.langchain.com/courses/quickstart-langsmith-essentials) -> [Agent Observability & Evaluation](https://academy.langchain.com/courses/building-reliable-agents)
- 实操版清单：接 tracing；记录节点开始结束时间；输出 tool call 详情

## 第48天：评测
- 今天要学会的知识：离线评测、结构化打分、成功率/引用率/延迟三项核心指标
- 今天不用深挖的内容：线上 A/B 平台、复杂评测数据集
- 今天学完后你应该能回答的问题：Agent 项目评测时最少应该看哪些指标？为什么“感觉不错”不算评测？
- 今天的完成标准：补离线评测集和结构化打分
- 今天的学习顺序：[Agent Observability & Evaluation](https://academy.langchain.com/courses/building-reliable-agents) -> [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs?api-mode=chat)
- 实操版清单：整理 20 条评测问题；写打分 schema；输出评测结果表

## 第49天：稳定性与成本
- 今天要学会的知识：超时、重试、fallback、成本日志、provider 切换
- 今天不用深挖的内容：复杂配额系统、财务对账
- 今天学完后你应该能回答的问题：Agent 系统最常见的三类稳定性问题是什么？什么时候要做 provider fallback？
- 今天的完成标准：补齐超时、重试、fallback、成本日志
- 今天的学习顺序：[redis-py Production Usage](https://redis.io/docs/latest/develop/clients/redis-py/produsage/) -> [FastAPI in Containers - Docker](https://fastapi.tiangolo.com/deployment/docker/)
- 实操版清单：给外部调用增加 timeout；加简单 retry；记录 token 和费用估算；支持 provider 切换

## 第50天：生产版 Dockerfile
- 今天要学会的知识：多阶段构建、生产镜像和开发镜像差异、容器启动命令
- 今天不用深挖的内容：镜像安全扫描、K8s 编排
- 今天学完后你应该能回答的问题：为什么开发态 Dockerfile 不能直接当生产版用？
- 今天的完成标准：完成生产版 `Dockerfile` 和 `docker-compose.yml`
- 今天的学习顺序：[Docker Compose Quickstart](https://docs.docker.com/compose/gettingstarted/) -> [FastAPI in Containers - Docker](https://fastapi.tiangolo.com/deployment/docker/)
- 实操版清单：优化 Dockerfile；设置环境变量；容器内跑迁移和应用

## 第51天：Python 容器化补强
- 今天要学会的知识：容器化 Python 项目的依赖安装、启动脚本、环境变量管理
- 今天不用深挖的内容：镜像分发、复杂缓存层
- 今天学完后你应该能回答的问题：为什么 `.env.example` 和容器启动说明对项目交付很重要？
- 今天的完成标准：补 lint、typing、容器化运行说明
- 今天的学习顺序：[Docker Python Guide](https://docs.docker.com/guides/python/) -> [Containerize a Python Application](https://docs.docker.com/guides/python/containerize/)
- 实操版清单：整理 `.env.example`；写启动命令；验证全新环境可启动

## 第52天：平台化目录统一
- 今天要学会的知识：把多个项目收束为统一平台壳、目录规范、公共模块抽取
- 今天不用深挖的内容：插件系统、复杂微服务拆分
- 今天学完后你应该能回答的问题：为什么 3 个项目不能完全割裂？哪些能力适合沉淀成公共模块？
- 今天的完成标准：A/B/C 项目统一为平台化目录结构
- 今天的学习顺序：[full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template) -> [Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- 实操版清单：抽公共 auth、db、llm、rag、agent 模块；统一配置和日志

## 第53天：存储与缓存优化
- 今天要学会的知识：metadata 存储、缓存键设计、TTL、索引补强
- 今天不用深挖的内容：复杂数据库调优、分库分表
- 今天学完后你应该能回答的问题：为什么缓存设计也会影响 Agent 产品体验？哪些字段适合做 metadata？
- 今天的完成标准：优化 metadata 存储、缓存和超时配置
- 今天的学习顺序：[PostgreSQL JSON Types](https://www.postgresql.org/docs/current/datatype-json.html) -> [redis-py Production Usage](https://redis.io/docs/latest/develop/clients/redis-py/produsage/)
- 实操版清单：梳理缓存键；补 TTL；检查索引；记录压测前后差异

## 第54天：Smoke Test + Lifespan
- 今天要学会的知识：服务启动钩子、健康检查、smoke test、最小交付测试体系
- 今天不用深挖的内容：复杂测试矩阵、全链路压测
- 今天学完后你应该能回答的问题：为什么“服务能启动”不等于“服务可用”？上线前最少要跑哪些 smoke test？
- 今天的完成标准：补 smoke test、启动钩子、健康检查
- 今天的学习顺序：[FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/) -> [Lifespan Events](https://fastapi.tiangolo.com/advanced/events/)
- 实操版清单：实现启动检查；补 `/health` 的数据库和缓存子检查；写 smoke test 脚本

## 第55天：统一架构图与作品集素材
- 今天要学会的知识：作品集组织、架构图表达、项目亮点总结
- 今天不用深挖的内容：花哨设计、复杂官网搭建
- 今天学完后你应该能回答的问题：你的 3 个项目分别证明了什么能力？架构图应该重点标哪几层？
- 今天的完成标准：整理统一架构图和作品集截图
- 今天的学习顺序：[LangGraph Overview](https://docs.langchain.com/oss/python/langgraph/overview) -> [MCP Architecture](https://modelcontextprotocol.io/docs/learn/architecture) -> [langgenius/dify](https://github.com/langgenius/dify)
- 实操版清单：画平台架构图；截图 3 个项目页面；写 6 条亮点 bullet

## 第56天：杭州版简历
- 今天要学会的知识：岗位关键词对齐、AI 岗简历改写、突出前端转 AI 的差异化优势
- 今天不用深挖的内容：英文简历、跨国岗位包装
- 今天学完后你应该能回答的问题：你相比纯后端或纯算法候选人的差异化卖点是什么？
- 今天的完成标准：完成 `AI应用工程师` 和 `AI Agent工程师` 两版简历
- 今天的学习顺序：[Boss 杭州 AI工程师列表](https://www.zhipin.com/zhaopin/7b6a86b85e006e5f1HVz2dy8EQ~~/) -> [智联 杭州 Python开发工程师（AI Agent方向）](https://www.zhaopin.com/jobdetail/CC635029720J40847536205.htm) -> [智联 杭州 AI应用工程师](https://www.zhaopin.com/jobdetail/CC502842530J40843146110.htm)
- 实操版清单：提炼 JD 高频词；重写自我介绍；每个项目写 3 条结果型 bullet

## 第57天：杭州 JD 匹配表
- 今天要学会的知识：岗位筛选、关键词匹配、投递优先级排序
- 今天不用深挖的内容：猎头沟通策略、薪资谈判细节
- 今天学完后你应该能回答的问题：哪类杭州岗位最适合你现在投？哪些岗位暂时应该放弃？
- 今天的完成标准：整理 30 个杭州 JD 匹配表
- 今天的学习顺序：[Boss 杭州 AI工程师列表](https://www.zhipin.com/zhaopin/7b6a86b85e006e5f1HVz2dy8EQ~~/) -> [Boss 杭州 AI技术应用工程师列表](https://www.zhipin.com/zhaopin/fad7e3f0a10bdeee1nJz2Nm-/) -> [智联 杭州 AI应用工程师](https://www.zhaopin.com/jobdetail/CC502842530J40843146110.htm)
- 实操版清单：建表字段：公司、岗位、薪资、关键词、匹配度、是否投递；先筛 30 家

## 第58天：模拟面试 1
- 今天要学会的知识：项目深挖表达、RAG 讲法、LangGraph 讲法、MCP 讲法
- 今天不用深挖的内容：算法岗问题、模型训练细节
- 今天学完后你应该能回答的问题：如果面试官让你 3 分钟介绍项目A/B/C，你能否讲清楚场景、架构、难点、结果？
- 今天的完成标准：完成 1 轮项目深挖模拟面试
- 今天的学习顺序：[LangGraph Overview](https://docs.langchain.com/oss/python/langgraph/overview) -> [Function Calling](https://platform.openai.com/docs/guides/function-calling?api-mode=responses) -> [MCP Architecture](https://modelcontextprotocol.io/docs/learn/architecture)
- 实操版清单：准备 10 个高频问题；录音复盘；改 3 个表达不顺的回答

## 第59天：模拟面试 2
- 今天要学会的知识：系统设计、稳定性、权限、成本控制、部署讲法
- 今天不用深挖的内容：极致性能调优、超大规模集群
- 今天学完后你应该能回答的问题：如果面试官问“系统怎么做稳定性/成本控制/权限隔离”，你能否给出工程化答案？
- 今天的完成标准：完成 1 轮系统设计 / 稳定性模拟面试
- 今天的学习顺序：[Docker Compose Quickstart](https://docs.docker.com/compose/gettingstarted/) -> [redis-py Production Usage](https://redis.io/docs/latest/develop/clients/redis-py/produsage/) -> [Agent Observability & Evaluation](https://academy.langchain.com/courses/building-reliable-agents)
- 实操版清单：准备 8 个系统设计题；输出标准答题模板；整理部署、缓存、重试、日志、评测话术

## 第60天：首批投递
- 今天要学会的知识：投递节奏、岗位优先级、面试跟进表、复盘机制
- 今天不用深挖的内容：所有城市全量海投
- 今天学完后你应该能回答的问题：你当前最应该投哪些岗位？投出去之后如何追踪和补短板？
- 今天的完成标准：首批投递 20-30 家；建立面试跟进表
- 今天的学习顺序：[Boss 杭州 AI工程师列表](https://www.zhipin.com/zhaopin/7b6a86b85e006e5f1HVz2dy8EQ~~/) -> [智联 杭州 Python开发工程师（AI Agent方向）](https://www.zhaopin.com/jobdetail/CC635029720J40847536205.htm) -> [智联 杭州 AI应用工程师](https://www.zhaopin.com/jobdetail/CC502842530J40843146110.htm)
- 实操版清单：投递 20-30 家；建跟进表；标记待准备问题；写未来 2 周补短板计划

---

## 每周复盘模板
- [ ] 本周完成了什么
- [ ] 本周新掌握的 3 个核心知识点
- [ ] 本周踩过的 3 个坑
- [ ] 本周新增的简历 bullet
- [ ] 下周最需要补的短板

## 飞书表格建议列
- 日期
- 天数
- 学习主题
- 学习链接
- 完成目标
- 是否完成
- 输出物
- 今日问题
- 明日计划
