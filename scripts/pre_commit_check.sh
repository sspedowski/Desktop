#!/usr/bin/env bash
# Justice File pre-commit health gate
set -euo pipefail
PY_MIN="3.10"
python - <<'PY'
import sys, re
req = tuple(int(x) for x in "3.10".split('.'))
cur = sys.version_info
if cur < req:
    print(f"[pre-commit] Python {req[0]}.{req[1]}+ required, found {cur.major}.{cur.minor}.{cur.micro}")
    sys.exit(1)
PY
python pipeline/diagnostics/quick_check.py --deps-only --timing --min-python "$PY_MIN" > .git/quick_check_last.json || {
  echo "[pre-commit] quick_check failed" >&2
  exit 1
}
# Optionally block if AI pipeline not ok (skip for speed)
python pipeline/diagnostics/quick_check.py --deps-only --min-python "$PY_MIN" --out .git/quick_check_last.json >/dev/null || exit 1

# Basic lint for markdown structure (optional placeholder)
# grep -R "\<TODO\>" -n . && { echo "[pre-commit] TODO markers present"; exit 1; } || true

echo "[pre-commit] OK"
