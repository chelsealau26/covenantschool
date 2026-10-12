#!/bin/bash
set -e

# Reinstall Python dependencies after a merge
if [ -f "pyproject.toml" ]; then
  uv sync --quiet
fi

if [ -f "package-lock.json" ]; then
  npm ci --no-audit --no-fund
fi
