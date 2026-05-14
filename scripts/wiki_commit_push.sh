#!/usr/bin/env bash
set -euo pipefail

MESSAGE="${1:-Update wiki}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$ROOT"

git pull --rebase
python3 tools/wiki.py index
python3 tools/wiki.py lint

if ! git diff --quiet || ! git diff --cached --quiet || [ -n "$(git ls-files --others --exclude-standard)" ]; then
  git add -A
  git commit -m "$MESSAGE"
  git push
else
  echo "No wiki changes to commit."
fi

