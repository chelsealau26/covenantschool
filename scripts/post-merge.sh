#!/bin/bash
set -e

# Reinstall Python dependencies after a merge
if [ -f "pyproject.toml" ]; then
  uv sync --quiet
fi
