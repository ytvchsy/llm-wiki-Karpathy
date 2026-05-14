# Operating Model

这套知识库的核心目标：让项目代码、飞书协作、LLM 开发过程和 Obsidian 知识图谱保持一致。

## 角色分工

| 角色 | 职责 |
| --- | --- |
| 人类维护者 | 决定目标、提供资料、审核关键判断 |
| 飞书 | 承载团队协作、会议、需求、讨论和外部输入 |
| Hermes/OpenClaw | 执行开发任务、整理工程上下文、更新项目知识 |
| Obsidian | 浏览、链接、图谱化和复盘知识 |
| GitHub | 同步、版本历史、备份和审计 |

## 信息生命周期

1. 资料进入飞书、代码仓库或 `raw/`。
2. LLM 将资料脱水成结构化 Markdown。
3. 项目事实进入 `wiki/project/`。
4. 通用知识进入 `wiki/concepts/`、`wiki/entities/` 和 `wiki/synthesis/`。
5. 索引和日志记录本次知识变更。
6. GitHub 保存完整历史。

## 项目文档约定

| 文件 | 用途 |
| --- | --- |
| `wiki/project/project-progress.md` | 当前阶段、已完成、进行中、阻塞、下一步 |
| `wiki/project/project-features.md` | 功能清单、状态、入口、依赖、验收标准 |
| `wiki/project/project-architecture.md` | 系统边界、组件、数据流、集成点 |
| `wiki/project/project-usage.md` | 安装、配置、常用命令、故障处理 |
| `wiki/project/project-decisions.md` | ADR 风格关键决策 |

## 更新节奏

- 每次开发后：更新 `wiki/project/`。
- 每次飞书同步后：更新 `wiki/sources/` 和相关项目页。
- 每周或阶段性复盘：更新 `wiki/overview.md` 和 `wiki/questions.md`。
- 每次结构变化：更新 `docs/architecture.md` 和本文件。
