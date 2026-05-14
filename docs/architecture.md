# Hermes + Obsidian + LLM Wiki Knowledge Base

双环境知识管理系统：云端飞书/代码/资料采集 + Hermes/OpenClaw/LLM 脱水整理 + 本地 Obsidian 知识图谱。

## 架构

```text
 External / Cloud Sources              Cloud Server                         Local Mac

┌─────────────────────────┐       push raw       ┌─────────────────────────┐
│ Feishu / Code / Web     │ ───────────────────▶ │ raw/                    │
│ papers / notes / chats  │                      │ immutable source layer  │
└─────────────────────────┘                      └────────────┬────────────┘
                                                               │ ingest
                                                               ▼
                                                     ┌─────────────────────┐
                                                     │ Hermes / OpenClaw   │
                                                     │ LLM agent / Codex   │
                                                     │ dehydration engine  │
                                                     └──────────┬──────────┘
                                                                │ compile
                                                                ▼
┌─────────────────────────┐       git push       ┌─────────────────────────┐       git pull       ┌─────────────────────┐
│ GitHub                  │ ◀─────────────────── │ wiki/                   │ ───────────────────▶ │ Obsidian / MOC      │
│ sync + history          │                      │ maintained knowledge   │                      │ index, log, graph   │
└─────────────────────────┘                      └─────────────────────────┘                      └─────────────────────┘
```

## 图例

### 节点

| 节点 | 含义 | 是否由 LLM 修改 |
| --- | --- | --- |
| External / Cloud Sources | 飞书、代码仓库、Discord、网页、论文、聊天记录、手工笔记等外部资料入口 | 否 |
| `raw/` | 原始事实层，保留未加工资料和附件 | 默认否 |
| Hermes / OpenClaw / LLM agent | 执行开发、摄入、摘要、交叉链接、去重、矛盾检查的脱水引擎 | 是 |
| `wiki/` | 由 LLM 维护的 Markdown 知识层 | 是 |
| Obsidian / MOC / indexes | Obsidian vault、Map of Content、索引、日志、图谱入口 | 是 |
| GitHub | 远端备份、同步、版本历史和审计轨迹 | 通过 git 同步 |

### 流程

| 流程 | 说明 | 典型命令或动作 |
| --- | --- | --- |
| `push raw` | 将外部资料保存到 `raw/`，保持原貌 | 手工复制、脚本导出、爬虫落盘 |
| `ingest` | LLM 阅读原始资料，生成来源摘要页和相关概念页 | `摄入 raw/<file>` |
| `compile` | 把来源事实编译成可复用知识页 | 更新 `wiki/sources/`、`concepts/`、`entities/`、`synthesis/` |
| `index` | 重建索引、记录日志、检查链接健康 | `python3 tools/wiki.py index`、`python3 tools/wiki.py lint` |
| `git push` | 推送本地 wiki 演化历史到 GitHub | `git push` |
| `git pull` | 从远端同步其他机器或自动化任务的更新 | `git pull` |
| `cloud publish` | 云端完成 Hermes/OpenClaw 开发后发布 wiki 更新 | `scripts/wiki_commit_push.sh "message"` |

## 目录说明

| 路径 | 职责 |
| --- | --- |
| `raw/` | 原始资料。这里是事实源，尽量不可变。 |
| `raw/assets/` | 图片、PDF、音频、导出附件等二进制资料。 |
| `wiki/sources/` | 每个原始资料对应的来源摘要、关键 claim、开放问题。 |
| `wiki/concepts/` | 可复用概念、主题、框架和长期知识单元。 |
| `wiki/entities/` | 人、组织、产品、地点、项目等实体档案。 |
| `wiki/synthesis/` | 跨来源综合、判断、矛盾整理和长期分析。 |
| `wiki/queries/` | 值得沉淀的一次性问答和研究结果。 |
| `wiki/index.md` | 主索引，类似 MOC 入口。 |
| `wiki/log.md` | 追加式操作日志，用于审计 wiki 的演化。 |
| `wiki/questions.md` | 待验证假设、资料缺口、冲突和后续研究问题。 |
| `tools/wiki.py` | 本地维护工具：索引、搜索、lint、日志、来源页脚手架。 |
| `scripts/wiki_commit_push.sh` | 云端发布脚本：pull、index、lint、commit、push。 |

## 维护规则

- 每次新增或重构目录职责时，同步更新本页和 `README.md`。
- 每次摄入资料后，至少更新相关来源页、索引和日志。
- `raw/` 到 `wiki/` 是单向脱水过程；不要为了让摘要更好看而改写原始资料。
- 如果 `wiki/` 中出现冲突说法，保留冲突并标注来源，不要直接合并成不确定的结论。
