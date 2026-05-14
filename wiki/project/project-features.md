---
title: Project Features
type: feature
status: active
created: 2026-05-14
updated: 2026-05-14
sources: []
tags:
  - project
  - feature
---

# Project Features

Functional scope for the AI knowledge base and its Feishu, Hermes/OpenClaw, Obsidian, and GitHub workflow.

## Knowledge Base Core

- `raw/` stores immutable source material.
- `wiki/` stores LLM-maintained Markdown knowledge.
- `tools/wiki.py` maintains index, search, backlinks, log, source pages, and lint checks.
- Obsidian can open the repository directly as a vault.
- GitHub stores version history and sync state.

## Feishu Ingestion

- `tools/feishu_sync.py` can fetch Feishu docx raw content into `raw/feishu/`.
- `.env.example` documents required credentials.
- `docs/feishu-integration.md` explains setup, sync, and post-sync wiki maintenance.

## Project Documentation Layer

- `wiki/project/project-progress.md` tracks development progress.
- `wiki/project/project-features.md` tracks functional scope.
- `wiki/project/project-architecture.md` tracks system architecture.
- `wiki/project/project-usage.md` tracks how to run and use the system.
- `wiki/project/project-decisions.md` tracks important technical decisions.

## Hermes/OpenClaw Development Contract

- `docs/hermes-openclaw-workflow.md` defines what documentation must be updated after development.
- AGENTS rules require project documentation updates after functional or architecture changes.
