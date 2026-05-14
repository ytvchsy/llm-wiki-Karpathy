#!/usr/bin/env python3
"""Fetch Feishu docx raw content into raw/feishu for LLM wiki ingest."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_FEISHU = ROOT / "raw" / "feishu"
FEISHU_BASE = "https://open.feishu.cn/open-apis"


def today() -> str:
    return dt.date.today().isoformat()


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^\w\s.-]+", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-{2,}", "-", text)
    return text.strip("-") or "feishu-document"


def extract_doc_id(value: str) -> str:
    value = value.strip()
    patterns = [
        r"/docx/([A-Za-z0-9]+)",
        r"/docs/([A-Za-z0-9]+)",
        r"/wiki/([A-Za-z0-9]+)",
        r"document_id=([A-Za-z0-9]+)",
        r"doc_token=([A-Za-z0-9]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, value)
        if match:
            return match.group(1)
    if re.fullmatch(r"[A-Za-z0-9]+", value):
        return value
    raise ValueError(f"could not extract Feishu document id from: {value}")


def request_json(method: str, url: str, *, token: str | None = None, data: dict | None = None) -> dict:
    body = None
    headers = {"Content-Type": "application/json; charset=utf-8"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if data is not None:
        body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Feishu API HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Feishu API network error: {exc}") from exc
    try:
        result = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Feishu API returned non-JSON response: {payload[:300]}") from exc
    code = result.get("code", 0)
    if code not in (0, None):
        raise RuntimeError(f"Feishu API error {code}: {result.get('msg') or result}")
    return result


def get_tenant_token(app_id: str, app_secret: str) -> str:
    result = request_json(
        "POST",
        f"{FEISHU_BASE}/auth/v3/tenant_access_token/internal",
        data={"app_id": app_id, "app_secret": app_secret},
    )
    token = result.get("tenant_access_token")
    if not token:
        raise RuntimeError("Feishu response did not include tenant_access_token")
    return str(token)


def fetch_raw_content(document_id: str, token: str) -> str:
    url = f"{FEISHU_BASE}/docx/v1/documents/{urllib.parse.quote(document_id)}/raw_content"
    result = request_json("GET", url, token=token)
    data = result.get("data") or {}
    if isinstance(data, dict):
        for key in ("content", "raw_content", "text", "plain_text"):
            value = data.get(key)
            if isinstance(value, str):
                return value
    for key in ("content", "raw_content", "text", "plain_text"):
        value = result.get(key)
        if isinstance(value, str):
            return value
    raise RuntimeError(f"could not find raw content in Feishu response keys: {sorted(result.keys())}")


def write_raw_file(document_id: str, title: str, source: str, content: str, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{today()}-{slugify(title or document_id)}.md"
    path = out_dir / filename
    text = f"""---
title: {title or document_id}
source: feishu
document_id: {document_id}
source_url: {source}
captured: {today()}
---

# {title or document_id}

{content.rstrip()}
"""
    path.write_text(text, encoding="utf-8")
    return path


def command_fetch(args: argparse.Namespace) -> int:
    load_dotenv(ROOT / ".env")
    app_id = args.app_id or os.environ.get("FEISHU_APP_ID")
    app_secret = args.app_secret or os.environ.get("FEISHU_APP_SECRET")
    if not app_id or not app_secret:
        print("missing FEISHU_APP_ID or FEISHU_APP_SECRET; create .env from .env.example", file=sys.stderr)
        return 2
    document_id = extract_doc_id(args.document)
    title = args.title or document_id
    token = get_tenant_token(app_id, app_secret)
    content = fetch_raw_content(document_id, token)
    out_dir = Path(args.out_dir)
    if not out_dir.is_absolute():
        out_dir = ROOT / out_dir
    path = write_raw_file(document_id, title, args.document, content, out_dir)
    print(path.relative_to(ROOT).as_posix())
    return 0


def command_extract_id(args: argparse.Namespace) -> int:
    print(extract_doc_id(args.document))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Sync Feishu documents into raw/feishu.")
    sub = parser.add_subparsers(dest="command", required=True)

    fetch = sub.add_parser("fetch", help="fetch a Feishu docx document into raw/feishu")
    fetch.add_argument("document", help="Feishu doc URL or document id")
    fetch.add_argument("--title", default="", help="title used for the raw markdown file")
    fetch.add_argument("--out-dir", default="raw/feishu", help="output directory")
    fetch.add_argument("--app-id", default="", help="override FEISHU_APP_ID")
    fetch.add_argument("--app-secret", default="", help="override FEISHU_APP_SECRET")
    fetch.set_defaults(func=command_fetch)

    extract = sub.add_parser("extract-id", help="extract a Feishu document id from a URL")
    extract.add_argument("document", help="Feishu doc URL or document id")
    extract.set_defaults(func=command_extract_id)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
