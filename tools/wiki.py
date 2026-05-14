#!/usr/bin/env python3
"""Small helper CLI for a Markdown-first LLM wiki."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"
RAW = ROOT / "raw"
INDEX = WIKI / "index.md"
LOG = WIKI / "log.md"

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
HEADING_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)


@dataclass
class Page:
    path: Path
    rel: str
    title: str
    page_type: str
    status: str
    sources: list[str]
    summary: str

    @property
    def stem(self) -> str:
        return self.path.stem

    @property
    def link(self) -> str:
        return f"[[{self.stem}]]"


def today() -> str:
    return dt.date.today().isoformat()


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^\w\s.-]+", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-{2,}", "-", text)
    return text.strip("-") or "untitled"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def iter_markdown() -> list[Path]:
    ignored_parts = {"_templates"}
    paths = []
    for path in WIKI.rglob("*.md"):
        if any(part in ignored_parts for part in path.parts):
            continue
        if path.name in {"index.md", "log.md"}:
            continue
        paths.append(path)
    return sorted(paths)


def parse_frontmatter(text: str) -> dict[str, object]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    data: dict[str, object] = {}
    current_key: str | None = None
    for raw_line in match.group(1).splitlines():
        line = raw_line.rstrip()
        if not line:
            continue
        if line.startswith("  - ") and current_key:
            data.setdefault(current_key, [])
            if isinstance(data[current_key], list):
                data[current_key].append(line[4:].strip().strip('"'))
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            current_key = key
            if value == "[]":
                data[key] = []
            elif value:
                data[key] = value.strip('"')
            else:
                data[key] = []
    return data


def first_heading(text: str) -> str | None:
    match = HEADING_RE.search(text)
    return match.group(1).strip() if match else None


def first_summary(text: str) -> str:
    body = FRONTMATTER_RE.sub("", text, count=1)
    lines = []
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("- "):
            continue
        lines.append(stripped)
        if len(" ".join(lines)) > 180:
            break
    summary = " ".join(lines)
    if not summary:
        return "No summary yet."
    return summary[:220].rstrip()


def load_pages() -> list[Page]:
    pages = []
    for path in iter_markdown():
        text = read(path)
        fm = parse_frontmatter(text)
        title = str(fm.get("title") or first_heading(text) or path.stem)
        page_type = str(fm.get("type") or "note")
        status = str(fm.get("status") or "active")
        sources_raw = fm.get("sources") or []
        sources = sources_raw if isinstance(sources_raw, list) else [str(sources_raw)]
        pages.append(
            Page(
                path=path,
                rel=path.relative_to(ROOT).as_posix(),
                title=title,
                page_type=page_type,
                status=status,
                sources=[s for s in sources if s],
                summary=first_summary(text),
            )
        )
    return pages


def command_index(_: argparse.Namespace) -> int:
    pages = load_pages()
    groups = [
        ("Overview", {"overview"}),
        ("Project", {"project", "progress", "feature", "architecture", "usage", "decision"}),
        ("Sources", {"source"}),
        ("Concepts", {"concept"}),
        ("Entities", {"entity"}),
        ("Synthesis", {"synthesis"}),
        ("Queries", {"query"}),
        ("Notes", {"note"}),
    ]
    lines = [
        "---",
        "title: Wiki Index",
        "type: index",
        "status: active",
        f"created: {creation_date(INDEX)}",
        f"updated: {today()}",
        "sources: []",
        "tags:",
        "  - index",
        "---",
        "",
        "# Wiki Index",
        "",
        "This file is maintained by `python3 tools/wiki.py index`.",
        "",
    ]
    seen: set[Path] = set()
    for heading, types in groups:
        lines.append(f"## {heading}")
        lines.append("")
        group_pages = [page for page in pages if page.page_type in types]
        if not group_pages:
            lines.append("No pages yet.")
        for page in sorted(group_pages, key=lambda p: (p.title.lower(), p.rel)):
            status = f" `{page.status}`" if page.status else ""
            lines.append(f"- {page.link} - {page.summary}{status}")
            seen.add(page.path)
        lines.append("")
    other_pages = [page for page in pages if page.path not in seen]
    if other_pages:
        lines.append("## Other")
        lines.append("")
        for page in sorted(other_pages, key=lambda p: (p.page_type, p.title.lower())):
            lines.append(f"- {page.link} - {page.summary} `{page.page_type}`")
        lines.append("")
    write(INDEX, "\n".join(lines).rstrip() + "\n")
    print(f"indexed {len(pages)} pages -> {INDEX.relative_to(ROOT)}")
    return 0


def creation_date(path: Path) -> str:
    if not path.exists():
        return today()
    fm = parse_frontmatter(read(path))
    return str(fm.get("created") or today())


def command_search(args: argparse.Namespace) -> int:
    query = args.query
    flags = 0 if args.case_sensitive else re.IGNORECASE
    try:
        pattern = re.compile(re.escape(query), flags)
    except re.error as exc:
        print(f"invalid query: {exc}", file=sys.stderr)
        return 2
    results = []
    for path in iter_markdown() + [INDEX, LOG]:
        if not path.exists():
            continue
        for lineno, line in enumerate(read(path).splitlines(), start=1):
            if pattern.search(line):
                results.append((path, lineno, line.strip()))
    for path, lineno, line in results[: args.limit]:
        print(f"{path.relative_to(ROOT)}:{lineno}: {line}")
    if len(results) > args.limit:
        print(f"... {len(results) - args.limit} more")
    return 0 if results else 1


def command_log(args: argparse.Namespace) -> int:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    if not LOG.exists():
        write(
            LOG,
            "---\n"
            "title: Wiki Log\n"
            "type: log\n"
            "status: active\n"
            f"created: {today()}\n"
            f"updated: {today()}\n"
            "sources: []\n"
            "tags:\n"
            "  - log\n"
            "---\n\n"
            "# Wiki Log\n\n",
        )
    text = read(LOG).rstrip()
    entry = f"\n\n## [{today()}] {args.kind} | {args.title}\n"
    if args.body:
        entry += f"\n{args.body.strip()}\n"
    write(LOG, text + entry)
    print(f"appended log entry -> {LOG.relative_to(ROOT)}")
    return 0


def command_new_source(args: argparse.Namespace) -> int:
    raw_path = Path(args.path)
    if not raw_path.is_absolute():
        raw_path = ROOT / raw_path
    if not raw_path.exists():
        print(f"source not found: {raw_path}", file=sys.stderr)
        return 2
    try:
        raw_rel = raw_path.relative_to(ROOT).as_posix()
    except ValueError:
        print("source must live inside this wiki repository", file=sys.stderr)
        return 2
    title = args.title or raw_path.stem.replace("-", " ").replace("_", " ").title()
    out = WIKI / "sources" / f"{slugify(title)}.md"
    if out.exists() and not args.force:
        print(f"page already exists: {out.relative_to(ROOT)}", file=sys.stderr)
        return 1
    page = f"""---
title: {title}
type: source
status: seed
created: {today()}
updated: {today()}
sources:
  - {raw_rel}
tags:
  - source
  - {args.kind}
---

# {title}

## Bibliographic Metadata

- Source path: [{raw_rel}](../../{raw_rel})
- Original URL:
- Author:
- Published:
- Captured: {today()}
- Source type: {args.kind}
- Reliability:

## Summary

Draft summary pending LLM ingest.

## Key Claims

- Pending.

## Entities

- Pending.

## Concepts

- Pending.

## Contradictions And Tensions

- None recorded.

## Open Questions

- None recorded.

## Follow-up Actions

- Complete source ingest and update related pages.
"""
    write(out, page)
    print(f"created {out.relative_to(ROOT)}")
    return 0


def collect_link_targets() -> dict[str, Path]:
    targets: dict[str, Path] = {}
    for path in iter_markdown() + [INDEX, LOG]:
        targets[path.stem.lower()] = path
        text = read(path)
        fm = parse_frontmatter(text)
        title = fm.get("title") or first_heading(text)
        if title:
            targets[str(title).lower()] = path
    return targets


def links_in(path: Path) -> list[str]:
    return [link.strip() for link in WIKILINK_RE.findall(read(path))]


def command_backlinks(args: argparse.Namespace) -> int:
    target = Path(args.path)
    target_stem = target.stem.lower()
    hits = []
    for path in iter_markdown() + [INDEX, LOG]:
        if path == target:
            continue
        for link in links_in(path):
            if link.lower() == target_stem:
                hits.append(path)
                break
    for path in hits:
        print(path.relative_to(ROOT))
    return 0 if hits else 1


def command_lint(_: argparse.Namespace) -> int:
    pages = load_pages()
    targets = collect_link_targets()
    all_paths = {page.path for page in pages}
    linked_paths: set[Path] = set()
    issues: list[str] = []

    for page in pages:
        text = read(page.path)
        fm = parse_frontmatter(text)
        if not fm:
            issues.append(f"missing frontmatter: {page.rel}")
        source_optional_types = {
            "overview",
            "note",
            "query",
            "project",
            "progress",
            "feature",
            "architecture",
            "usage",
            "decision",
        }
        if page.page_type not in source_optional_types and not page.sources:
            issues.append(f"missing sources: {page.rel}")
        for source in page.sources:
            source_path = ROOT / source
            if source and not source_path.exists():
                issues.append(f"missing source file: {page.rel} -> {source}")
        for link in links_in(page.path):
            target = targets.get(link.lower())
            if not target:
                issues.append(f"broken wikilink: {page.rel} -> [[{link}]]")
            else:
                linked_paths.add(target)

    for page in pages:
        if page.path.name in {"overview.md", "questions.md"}:
            continue
        if page.path not in linked_paths and page.path in all_paths:
            issues.append(f"orphan page: {page.rel}")

    title_seen: dict[str, str] = {}
    for page in pages:
        key = page.title.lower()
        if key in title_seen:
            issues.append(f"duplicate title: {title_seen[key]} and {page.rel}")
        else:
            title_seen[key] = page.rel

    if not issues:
        print("lint ok")
        return 0
    for issue in issues:
        print(issue)
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Maintain a Markdown-first LLM wiki.")
    sub = parser.add_subparsers(dest="command", required=True)

    index_cmd = sub.add_parser("index", help="rebuild wiki/index.md")
    index_cmd.set_defaults(func=command_index)

    search_cmd = sub.add_parser("search", help="search wiki markdown files")
    search_cmd.add_argument("query")
    search_cmd.add_argument("--case-sensitive", action="store_true")
    search_cmd.add_argument("--limit", type=int, default=50)
    search_cmd.set_defaults(func=command_search)

    log_cmd = sub.add_parser("log", help="append an entry to wiki/log.md")
    log_cmd.add_argument("kind", help="ingest, query, lint, setup, decision, etc.")
    log_cmd.add_argument("title")
    log_cmd.add_argument("--body", default="")
    log_cmd.set_defaults(func=command_log)

    new_source_cmd = sub.add_parser("new-source", help="create a source summary page")
    new_source_cmd.add_argument("path")
    new_source_cmd.add_argument("--title")
    new_source_cmd.add_argument("--kind", default="source")
    new_source_cmd.add_argument("--force", action="store_true")
    new_source_cmd.set_defaults(func=command_new_source)

    backlinks_cmd = sub.add_parser("backlinks", help="list pages linking to a target page")
    backlinks_cmd.add_argument("path")
    backlinks_cmd.set_defaults(func=command_backlinks)

    lint_cmd = sub.add_parser("lint", help="check links, sources, orphans, and metadata")
    lint_cmd.set_defaults(func=command_lint)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
