@echo off
set PY_MIN=3.10
python - <<PY
import sys
req = (3,10)
cur = sys.version_info
if cur < req:
    print(f"[pre-commit] Python {req[0]}.{req[1]}+ required, found {cur.major}.{cur.minor}.{cur.micro}")
    sys.exit(1)
PY
if errorlevel 1 exit /b 1
python pipeline/diagnostics/quick_check.py --deps-only --timing --min-python %PY_MIN% > .git\quick_check_last.json
if errorlevel 1 (
  echo [pre-commit] quick_check failed
  exit /b 1
)
python pipeline/diagnostics/quick_check.py --deps-only --min-python %PY_MIN% --out .git\quick_check_last.json >nul
if errorlevel 1 exit /b 1
echo [pre-commit] OK
