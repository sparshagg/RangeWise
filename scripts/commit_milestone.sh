#!/bin/sh
set -eu

if [ "$#" -ne 1 ]; then
  echo "Usage: ./scripts/commit_milestone.sh \"type: message\""
  exit 1
fi

COMMIT_MESSAGE="$1"

if [ -x ".venv/bin/python" ]; then
  PYTHON_BIN=".venv/bin/python"
else
  PYTHON_BIN="python3"
fi

"$PYTHON_BIN" scripts/build_processed_dataset.py
"$PYTHON_BIN" scripts/sync_project_docs.py

if [ -x ".venv/bin/pytest" ]; then
  .venv/bin/pytest
fi

git add -A

if git diff --cached --quiet; then
  echo "No staged changes to commit."
  exit 0
fi

git commit -m "$COMMIT_MESSAGE"

CURRENT_BRANCH="$(git branch --show-current)"
git push origin "$CURRENT_BRANCH"
