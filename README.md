# Hermes + Obsidian + LLM Wiki

一套面向 Hermes/OpenClaw 开发流程的 AI 知识库方案：飞书负责协作输入，LLM 负责脱水整理，Obsidian 负责本地浏览和图谱，GitHub 负责版本历史和同步。

它采用 Karpathy 提到的三层结构：

- `raw/`: 原始资料，只读保存，不由 LLM 修改。
- `wiki/`: LLM 维护的 Markdown 知识层，用于摘要、概念、实体、综合分析和查询沉淀。
- `AGENTS.md`: 给 Codex/其他代理的操作规则，确保每次摄入、查询、维护都有一致流程。

架构图、图例和目录职责见 [docs/architecture.md](docs/architecture.md)。
飞书接入见 [docs/feishu-integration.md](docs/feishu-integration.md)。
Hermes/OpenClaw 开发文档流见 [docs/hermes-openclaw-workflow.md](docs/hermes-openclaw-workflow.md)。
云服务器部署见 [docs/cloud-deployment.md](docs/cloud-deployment.md)。

## 架构速览

```text
Feishu / Code / Notes -> raw/ -> LLM/Hermes/OpenClaw -> wiki/ -> Obsidian
                                      GitHub <---- git sync ---->
```

## 快速开始

1. 把文章、PDF 转写、会议纪要、网页剪藏或其他资料放到 `raw/`。
2. 让 LLM 执行：`摄入 raw/<filename>`。
3. LLM 会创建或更新 `wiki/sources/`、相关概念页、实体页、`wiki/index.md` 和 `wiki/log.md`。
4. 用 Obsidian 打开本目录，浏览 `wiki/index.md` 和图谱视图。
5. Hermes/OpenClaw 每次开发后更新 `wiki/project/` 的进度、功能、架构、使用和决策文档。

## CLI

项目内置一个零依赖 Python CLI，帮助代理和人类维护 wiki。

```bash
python3 tools/wiki.py index
python3 tools/wiki.py search "关键词"
python3 tools/wiki.py lint
python3 tools/wiki.py backlinks wiki/concepts/example.md
python3 tools/wiki.py log ingest "Article Title" --body "Processed raw/article.md"
python3 tools/wiki.py new-source raw/article.md --title "Article Title" --kind article
python3 tools/feishu_sync.py extract-id "https://example.feishu.cn/docx/xxxx"
python3 tools/feishu_sync.py fetch "https://example.feishu.cn/docx/xxxx" --title "项目会议"
```

## 目录约定

- `wiki/index.md`: 内容索引，按类型列出所有页面。
- `wiki/log.md`: 追加式时间线，记录摄入、查询、维护和决策。
- `wiki/overview.md`: 当前知识库的高层综述。
- `wiki/sources/`: 单个来源的摘要页。
- `wiki/concepts/`: 可复用概念、主题、框架。
- `wiki/entities/`: 人、组织、产品、地点、项目等实体。
- `wiki/synthesis/`: 跨来源综合、论文式分析、长期判断。
- `wiki/queries/`: 值得沉淀的问答和一次性研究结果。
- `wiki/questions.md`: 开放问题、待验证假设、需要补充资料的空白。
- `wiki/project/`: 项目进度、功能、架构、使用说明和技术决策。
- `docs/architecture.md`: 架构图、图例、流程说明和目录职责。
- `docs/feishu-integration.md`: 飞书自建应用接入、同步和摄入流程。
- `docs/hermes-openclaw-workflow.md`: Hermes/OpenClaw 开发后如何更新 wiki。
- `docs/cloud-deployment.md`: 云服务器部署、Hermes/OpenClaw 部署和本地 Obsidian 同步方案。
- `scripts/wiki_commit_push.sh`: 云端更新 wiki 后的一键 index、lint、commit、push 脚本。

## 推荐工作流

### 摄入

```text
请摄入 raw/<file>，更新 wiki，并记录来源、关键结论、相关页面、矛盾和开放问题。
```

### 查询

```text
请基于 wiki 回答：<问题>。先读 index，再读取相关页面；如果答案值得复用，请沉淀到 wiki/queries/ 或 wiki/synthesis/。
```

### 飞书同步

```text
请同步飞书文档到 raw/feishu/，再摄入 wiki，并更新项目进度、功能、架构、使用说明和决策。
```

### 开发后文档更新

```text
本次 Hermes/OpenClaw 开发完成后，请更新 wiki/project/project-progress.md、project-features.md、project-architecture.md、project-usage.md、project-decisions.md，并运行 index/lint。
```

### 云端提交同步

```bash
scripts/wiki_commit_push.sh "Update project wiki"
```

### 健康检查

```text
请运行 wiki lint，检查孤儿页、断链、缺少来源、重复概念和可能矛盾，然后修复高价值问题。
```

## 原则

- 原始资料是事实源，保持不可变。
- wiki 是编译层，允许被 LLM 持续重写和改进。
- 所有重要断言尽量带来源链接。
- 对不确定、冲突、过期的信息要显式标注。
- 重要查询结果不应该只留在聊天记录里，要沉淀回 wiki。
