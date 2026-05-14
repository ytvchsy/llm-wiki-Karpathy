# Feishu Integration

本仓库的飞书接入定位是“把飞书文档同步到 `raw/`，再由 LLM 脱水进 `wiki/`”。飞书是协作入口，Git + Obsidian 是可审计知识库。

## 接入目标

- 从飞书文档读取项目会议、需求、进度、架构讨论和使用说明。
- 原文落到 `raw/feishu/`，保持可追溯。
- LLM 将原文整理到 `wiki/project/`、`wiki/sources/`、`wiki/concepts/` 和 `wiki/synthesis/`。
- 每次同步都能通过 GitHub 记录变更。

## 准备飞书应用

1. 在飞书开放平台创建自建应用。
2. 获取 `APP_ID` 和 `APP_SECRET`。
3. 给应用开通新版文档读取权限，至少需要读取文档内容的权限。
4. 发布应用到可用范围。
5. 在目标飞书文档里添加该应用为协作者，确保应用有读取权限。
6. 在本地创建 `.env`，参考 `.env.example`：

```bash
FEISHU_APP_ID=cli_xxxxxxxxxxxxxxxx
FEISHU_APP_SECRET=xxxxxxxxxxxxxxxx
```

## 同步命令

同步单个飞书文档到 `raw/feishu/`：

```bash
python3 tools/feishu_sync.py fetch "https://example.feishu.cn/docx/xxxxxxxxxxxxxxxx" --title "项目周报"
```

同步后摄入 wiki：

```text
请摄入 raw/feishu/项目周报.md，并更新项目进度、功能、架构和使用文档。
```

也可以用 `make`：

```bash
make feishu url="https://example.feishu.cn/docx/xxxxxxxxxxxxxxxx" title="项目周报"
```

## 推荐飞书文档类型

| 飞书文档 | 落盘位置 | wiki 目标 |
| --- | --- | --- |
| 会议纪要 | `raw/feishu/meetings/` 或 `raw/feishu/` | `wiki/project/project-progress.md`、`wiki/project/project-decisions.md` |
| 需求文档 | `raw/feishu/requirements/` 或 `raw/feishu/` | `wiki/project/project-features.md` |
| 架构讨论 | `raw/feishu/architecture/` 或 `raw/feishu/` | `wiki/project/project-architecture.md`、`wiki/synthesis/` |
| 使用说明 | `raw/feishu/usage/` 或 `raw/feishu/` | `wiki/project/project-usage.md` |
| 发布记录 | `raw/feishu/releases/` 或 `raw/feishu/` | `wiki/project/project-progress.md` |

## 同步后的 LLM 维护动作

每次从飞书同步后，LLM 应执行：

1. 创建或更新 `wiki/sources/<source>.md`。
2. 将稳定事实写入 `wiki/project/`。
3. 将概念、实体、长期判断分别写入对应目录。
4. 对冲突或不确定信息写入 `wiki/questions.md`。
5. 运行 `python3 tools/wiki.py index` 和 `python3 tools/wiki.py lint`。
6. 追加 `wiki/log.md`。
7. 提交并推送到 GitHub。

## 限制

- 当前脚本优先支持新版飞书文档 `docx` 的纯文本读取。
- 复杂表格、图片和多维表格建议先导出为 Markdown、CSV 或截图附件，再放入 `raw/`。
- 如果飞书 API 返回权限错误，先检查应用权限、发布范围、文档协作者设置和文档 URL 中的 token。
