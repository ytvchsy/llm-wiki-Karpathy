# LLM Wiki Agent Rules

You are maintaining an LLM-owned Markdown wiki. Treat this repository as a knowledge codebase.

## Architecture

- `raw/` contains immutable source material. Read it, cite it, but do not edit it unless the user explicitly asks.
- `wiki/` contains the maintained knowledge layer. You may create, rewrite, split, merge, and cross-link these pages.
- `wiki/index.md` is the content catalog. Update it after every meaningful wiki change.
- `wiki/log.md` is append-only chronological history. Append an entry after every ingest, query synthesis, lint pass, or structural change.
- `docs/architecture.md` contains the architecture diagram, legend, flow meanings, and directory responsibilities. Update it when the topology or directory contract changes.
- `wiki/project/` contains durable project documentation for Hermes/OpenClaw development: progress, features, architecture, usage, and decisions.
- `raw/feishu/` contains Feishu document sync output. Treat it as immutable source material.
- `tools/wiki.py` provides helper commands for indexing, search, backlinks, logging, source scaffolding, and linting.
- `tools/feishu_sync.py` fetches Feishu docx raw content into `raw/feishu/`.

## Page Conventions

Every maintained wiki page should start with YAML frontmatter:

```yaml
---
title: Page Title
type: source | concept | entity | synthesis | query | overview | note
status: seed | active | stable | deprecated
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - raw/example.md
tags:
  - tag
---
```

Use Obsidian-style links for wiki references: `[[concept-name]]` or `[[concept-name|label]]`.

Use normal Markdown links for raw files and external URLs.

## Source Ingest Workflow

When the user asks you to ingest a source:

1. Read the source from `raw/`.
2. Identify title, author, date, source type, and reliability if available.
3. Create or update a page in `wiki/sources/` using `wiki/_templates/source.md`.
4. Extract:
   - key claims
   - evidence
   - definitions
   - entities
   - concepts
   - contradictions or tensions with existing wiki pages
   - open questions
5. Update relevant `wiki/concepts/`, `wiki/entities/`, `wiki/synthesis/`, and `wiki/questions.md`.
6. Add cross-links between all touched pages.
7. Run `python3 tools/wiki.py index`.
8. Run `python3 tools/wiki.py lint` and fix high-value issues.
9. Append a log entry with `python3 tools/wiki.py log ingest "<title>" --body "..."`

Prefer ingesting one source carefully over batch ingestion when the source is dense.

## Hermes/OpenClaw Development Documentation Workflow

After every meaningful Hermes/OpenClaw development task:

1. Update `wiki/project/project-progress.md` with what changed, current status, blockers, and next steps.
2. Update `wiki/project/project-features.md` for new or changed functionality.
3. Update `wiki/project/project-architecture.md` for system boundary, component, data-flow, or integration changes.
4. Update `wiki/project/project-usage.md` for commands, configuration, and operator-facing instructions.
5. Update `wiki/project/project-decisions.md` for important tradeoffs or irreversible decisions.
6. Update `docs/architecture.md` when the overall topology changes.
7. Run `python3 tools/wiki.py index`.
8. Run `python3 tools/wiki.py lint`.
9. Append to `wiki/log.md`.

Do not leave development knowledge only in chat or commit messages.

## Feishu Workflow

When ingesting Feishu material:

1. Use `python3 tools/feishu_sync.py fetch "<doc-url>" --title "<title>"` when credentials are configured.
2. Treat the generated `raw/feishu/*.md` file as immutable source material.
3. Create or update a source page in `wiki/sources/`.
4. Move stable project knowledge into `wiki/project/`.
5. Record uncertainty, missing credentials, or permission problems in `wiki/questions.md`.
6. Update index, lint, log, then commit.

## Query Workflow

When answering a question against the wiki:

1. Read `wiki/index.md` first.
2. Search with `python3 tools/wiki.py search "<terms>"` if relevant pages are not obvious.
3. Read the relevant pages and their source links.
4. Answer with citations to wiki pages and raw sources where possible.
5. If the answer is reusable, create a page in `wiki/queries/` or `wiki/synthesis/`.
6. Update `wiki/index.md` and append to `wiki/log.md`.

Do not claim the wiki supports an answer if the evidence is missing. Add the gap to `wiki/questions.md`.

## Maintenance Workflow

Run periodic health checks:

```bash
python3 tools/wiki.py lint
python3 tools/wiki.py index
```

Look for:

- broken wiki links
- orphan pages
- pages without source references
- stale claims
- duplicate concepts
- contradictions between pages
- missing cross-links
- valuable query answers not filed back into the wiki

When you find contradictions, do not smooth them away. Record:

- the conflicting claims
- the source for each claim
- what would resolve the conflict
- current best interpretation, if any

## Editing Discipline

- Keep raw sources immutable.
- Keep pages concise but complete enough to be reusable.
- Preserve provenance.
- Prefer explicit uncertainty over false synthesis.
- Use frontmatter dates in local `YYYY-MM-DD` format.
- Do not create decorative files or unrelated app code unless the user asks.
