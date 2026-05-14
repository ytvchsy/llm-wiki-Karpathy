# LLM Wiki

一个面向 LLM 代理维护的本地知识库骨架。它采用 Karpathy 提到的三层结构：

- `raw/`: 原始资料，只读保存，不由 LLM 修改。
- `wiki/`: LLM 维护的 Markdown 知识层，用于摘要、概念、实体、综合分析和查询沉淀。
- `AGENTS.md`: 给 Codex/其他代理的操作规则，确保每次摄入、查询、维护都有一致流程。

## 快速开始

1. 把文章、PDF 转写、会议纪要、网页剪藏或其他资料放到 `raw/`。
2. 让 LLM 执行：`摄入 raw/<filename>`。
3. LLM 会创建或更新 `wiki/sources/`、相关概念页、实体页、`wiki/index.md` 和 `wiki/log.md`。
4. 用 Obsidian 打开本目录，浏览 `wiki/index.md` 和图谱视图。

## CLI

项目内置一个零依赖 Python CLI，帮助代理和人类维护 wiki。

```bash
python3 tools/wiki.py index
python3 tools/wiki.py search "关键词"
python3 tools/wiki.py lint
python3 tools/wiki.py backlinks wiki/concepts/example.md
python3 tools/wiki.py log ingest "Article Title" --body "Processed raw/article.md"
python3 tools/wiki.py new-source raw/article.md --title "Article Title" --kind article
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

## 推荐工作流

### 摄入

```text
请摄入 raw/<file>，更新 wiki，并记录来源、关键结论、相关页面、矛盾和开放问题。
```

### 查询

```text
请基于 wiki 回答：<问题>。先读 index，再读取相关页面；如果答案值得复用，请沉淀到 wiki/queries/ 或 wiki/synthesis/。
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
