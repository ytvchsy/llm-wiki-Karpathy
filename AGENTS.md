# LLM Wiki Agent Rules

You are maintaining an LLM-owned Markdown wiki. Treat this repository as a knowledge codebase.

## Architecture

- `raw/` contains immutable source material. Read it, cite it, but do not edit it unless the user explicitly asks.
- `wiki/` contains the maintained knowledge layer. You may create, rewrite, split, merge, and cross-link these pages.
- `wiki/index.md` is the content catalog. Update it after every meaningful wiki change.
- `wiki/log.md` is append-only chronological history. Append an entry after every ingest, query synthesis, lint pass, or structural change.
- `tools/wiki.py` provides helper commands for indexing, search, backlinks, logging, source scaffolding, and linting.

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
