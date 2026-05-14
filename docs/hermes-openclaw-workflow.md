# Hermes + OpenClaw Workflow

本仓库把 Hermes/OpenClaw 开发过程纳入 wiki：代码可以在项目仓库里演进，项目知识在本仓库里沉淀。

云服务器部署和同步方式见 [cloud-deployment.md](cloud-deployment.md)。

## 工作模型

```text
Feishu discussions / issues / code changes
              │
              ▼
        raw/ source record
              │
              ▼
Hermes / OpenClaw development agent
              │
              ▼
wiki/project/{progress,features,architecture,usage,decisions}
              │
              ▼
Obsidian graph + GitHub history
```

## 每次开发后的文档落点

| 开发输出 | 必须更新 | 可选更新 |
| --- | --- | --- |
| 新功能 | `wiki/project/project-features.md`、`wiki/project/project-usage.md` | `wiki/concepts/` |
| 架构调整 | `wiki/project/project-architecture.md`、`wiki/project/project-decisions.md` | `docs/architecture.md` |
| Bug 修复 | `wiki/project/project-progress.md` | `wiki/questions.md` |
| 接入飞书或外部系统 | `docs/feishu-integration.md`、`wiki/project/project-architecture.md` | `wiki/sources/` |
| 发布版本 | `wiki/project/project-progress.md`、`wiki/log.md` | `wiki/project/project-usage.md` |

## Hermes/OpenClaw 提示词

用于开发前：

```text
请基于当前仓库实现 <功能>。
完成后必须更新 llm-wiki：
1. wiki/project/project-progress.md：记录开发进度和完成状态
2. wiki/project/project-features.md：记录新增或变化的功能
3. wiki/project/project-architecture.md：记录架构影响
4. wiki/project/project-usage.md：记录用户如何使用
5. wiki/project/project-decisions.md：记录关键技术决策
最后运行 python3 tools/wiki.py index 和 python3 tools/wiki.py lint。
```

用于飞书资料摄入后：

```text
请读取 raw/feishu/<file>.md，把其中和项目有关的信息写入 wiki/project/。
不要改 raw 原文；对不确定内容写入 wiki/questions.md；完成后更新 index 和 log。
```

## 质量门禁

每次提交前至少执行：

```bash
python3 tools/wiki.py index
python3 tools/wiki.py lint
```

如果改动涉及飞书同步脚本：

```bash
python3 -m py_compile tools/feishu_sync.py
```

云端开发完成后推荐直接执行：

```bash
scripts/wiki_commit_push.sh "Update wiki after Hermes development"
```
