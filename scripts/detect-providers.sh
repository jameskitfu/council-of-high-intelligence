#!/usr/bin/env bash
set -euo pipefail

# Backwards-compatible entry point; --host defaults to claude.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "${SCRIPT_DIR}/detect_providers.py" "$@"
