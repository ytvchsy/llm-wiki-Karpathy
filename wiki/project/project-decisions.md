---
title: Project Decisions
type: decision
status: active
created: 2026-05-14
updated: 2026-05-14
sources: []
tags:
  - project
  - decision
---

# Project Decisions

## 2026-05-14 | Use Markdown Wiki As The Durable Knowledge Layer

## Context

The project needs a knowledge base that can be maintained by LLM agents, opened locally in Obsidian, synced through GitHub, and fed by Feishu collaboration documents.

## Decision

Use this repository as the durable Markdown knowledge layer. Keep source material in `raw/`, maintained knowledge in `wiki/`, and project documentation in `wiki/project/`.

## Consequences

- Positive: simple local files, easy Git history, Obsidian-compatible, LLM-friendly.
- Negative: rich Feishu content may need conversion or export strategy.
- Follow-up: configure real Feishu credentials and link the Hermes/OpenClaw project repository.
