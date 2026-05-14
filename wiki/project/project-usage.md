---
title: Project Usage
type: usage
status: active
created: 2026-05-14
updated: 2026-05-14
sources: []
tags:
  - project
  - usage
---

# Project Usage

## Open In Obsidian

Open `/Users/totus/data/llm-wiki` as an Obsidian vault.

Start from:

- [[index]]
- [[overview]]
- [[project-progress|Project Progress]]
- [[project-features|Project Features]]
- [[project-architecture|Project Architecture]]

## Maintain The Wiki

```bash
python3 tools/wiki.py index
python3 tools/wiki.py lint
python3 tools/wiki.py search "keyword"
```

## Sync A Feishu Document

Create `.env` from `.env.example`, then run:

```bash
python3 tools/feishu_sync.py fetch "https://example.feishu.cn/docx/xxxxxxxxxxxxxxxx" --title "Project Meeting"
```

Then ask the LLM:

```text
请摄入 raw/feishu/project-meeting.md，并更新 wiki/project/ 的进度、功能、架构、使用说明和决策。
```

## Development Documentation Rule

After Hermes/OpenClaw development, update:

- [[project-progress|Project Progress]]
- [[project-features|Project Features]]
- [[project-architecture|Project Architecture]]
- [[project-usage|Project Usage]]
- [[project-decisions|Project Decisions]]

Then run:

```bash
python3 tools/wiki.py index
python3 tools/wiki.py lint
git add -A
git commit -m "Update project wiki"
git push
```

## Cloud Publish

On the cloud server, after Hermes/OpenClaw finishes a development task and updates wiki pages:

```bash
scripts/wiki_commit_push.sh "Update project wiki after Hermes development"
```

On the local Mac, pull the latest docs before opening Obsidian:

```bash
cd /Users/totus/data/llm-wiki
git pull
```
