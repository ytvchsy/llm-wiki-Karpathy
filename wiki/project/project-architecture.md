---
title: Project Architecture
type: architecture
status: active
created: 2026-05-14
updated: 2026-05-14
sources: []
tags:
  - project
  - architecture
---

# Project Architecture

## System Boundary

This repository is the knowledge layer for a Hermes + Obsidian + LLM wiki workflow.

It does not replace the Hermes/OpenClaw code repository. Instead, it records project knowledge produced by development, Feishu collaboration, and LLM maintenance.

## Components

| Component | Responsibility |
| --- | --- |
| Feishu | Collaborative documents, meetings, requirements, and team discussion records |
| `tools/feishu_sync.py` | Pull Feishu docx raw content into `raw/feishu/` |
| `raw/` | Immutable source material |
| Hermes/OpenClaw | Development agent or project code workflow |
| LLM/Codex | Ingest raw material and maintain wiki pages |
| `wiki/project/` | Project-facing docs: progress, features, architecture, usage, decisions |
| Obsidian | Local browsing, backlinks, graph view |
| GitHub | Remote history, sync, backup |

## Data Flow

```text
Feishu docx -> tools/feishu_sync.py -> raw/feishu/*.md
raw/feishu/*.md -> LLM ingest -> wiki/project/*.md
Hermes/OpenClaw development -> LLM summary -> wiki/project/*.md
wiki updates -> tools/wiki.py index/lint -> git push -> GitHub
```

## Integration Points

- Feishu OpenAPI: tenant token + document raw content endpoint.
- Git: version history and remote sync.
- Obsidian: Markdown vault and graph view.
- Hermes/OpenClaw: development process that must update wiki project docs.

## Known Gaps

- Actual Feishu app credentials are not configured in this repository.
- Actual Hermes/OpenClaw project repository path and commands are not configured yet.
- Complex Feishu tables and rich media need a dedicated export strategy.
