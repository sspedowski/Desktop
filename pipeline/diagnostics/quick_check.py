"""Justice File System - Quick Environment & Pipeline Health Check

Run:
  python pipeline/diagnostics/quick_check.py

What it does:
 1. Validates Python version (>=3.9 recommended)
 2. Checks core dependencies (markdown, openpyxl, pdfplumber, docx2txt, weasyprint or reportlab, tkinter)
 3. Creates a sample evidence file if none present
 4. Executes MASTER_PIPELINE_GPT5.py in --dry-run mode (tasks A,B,C)
 5. Captures recent log lines & outputs JSON summary

Exits with code 0 if all PASS, otherwise 1.
"""
from __future__ import annotations
import sys
import json
import subprocess
import shutil
from pathlib import Path
import importlib
import tempfile
import textwrap

ROOT = Path(__file__).resolve().parents[2]
PIPELINE = ROOT / 'MASTER_PIPELINE_GPT5.py'
EVIDENCE_DIR = ROOT / 'evidence'
OUTPUT_DIR = ROOT / 'pipeline' / 'outputs'
PDF_DIR = ROOT / 'legal_export' / 'pdf'
EXCEL = ROOT / 'MASTER_JUSTICE_FILE_SUPREME_v1.xlsx'

CORE_MODULES = [
    'markdown',
    'openpyxl',
    'pdfplumber',
    'docx2txt'
]
ALT_MODULES = ['weasyprint', 'reportlab']  # Need at least one
OPTIONAL_MODULES = ['tkinter']


def check_python():
    ver = sys.version_info
    return {'version': f'{ver.major}.{ver.minor}.{ver.micro}', 'ok': ver >= (3,9)}


def check_imports():
    results = {}
    for mod in CORE_MODULES:
        try:
            importlib.import_module(mod)
            results[mod] = True
        except Exception:
            results[mod] = False
    alt_ok = False
    alt_available = []
    for mod in ALT_MODULES:
        try:
            importlib.import_module(mod)
            alt_ok = True
            alt_available.append(mod)
        except Exception:
            pass
    results['pdf_engine'] = alt_available
    results['pdf_engine_ok'] = alt_ok
    # Tkinter check
    try:
        importlib.import_module('tkinter')
        results['tkinter'] = True
    except Exception:
        results['tkinter'] = False
    return results


def ensure_sample_evidence():
    EVIDENCE_DIR.mkdir(exist_ok=True)
    sample = EVIDENCE_DIR / 'example.txt'
    if not sample.exists():
        sample.write_text(textwrap.dedent('''\
        This is a sample evidence text document used for dry-run health checking.
        It contains a brief line of content to allow summary/brief mock generation.
        '''), encoding='utf-8')
    return sample


def run_dry_pipeline():
    if not PIPELINE.exists():
        return {'ok': False, 'error': 'Pipeline script missing'}
    ensure_sample_evidence()
    cmd = [sys.executable, str(PIPELINE), '--input', str(EVIDENCE_DIR), '--tasks', 'A,B,C', '--children', 'HealthCheckChild', '--out', str(OUTPUT_DIR), '--dry-run']
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        ok = proc.returncode == 0
        lines = proc.stdout.strip().splitlines()
        tail = lines[-12:]
        return {
            'ok': ok,
            'returncode': proc.returncode,
            'tail': tail,
            'stdout_bytes': len(proc.stdout.encode('utf-8')),
            'stderr': proc.stderr.strip() or None
        }
    except subprocess.TimeoutExpired:
        return {'ok': False, 'error': 'Pipeline timeout'}
    except Exception as e:
        return {'ok': False, 'error': str(e)}


def scan_outputs():
    outputs = list(OUTPUT_DIR.glob('*.md'))
    pdfs = list(PDF_DIR.glob('*.pdf'))
    return {
        'md_files': len(outputs),
        'pdf_files': len(pdfs),
        'excel_exists': EXCEL.exists()
    }


def main():
    py_info = check_python()
    imports = check_imports()
    pipeline_result = run_dry_pipeline()
    artifacts = scan_outputs()

    overall_ok = py_info['ok'] and imports['pdf_engine_ok'] and all(imports.get(m) for m in CORE_MODULES) and pipeline_result.get('ok')

    report = {
        'python': py_info,
        'imports': imports,
        'pipeline': pipeline_result,
        'artifacts': artifacts,
        'overall_ok': overall_ok
    }
    print(json.dumps(report, indent=2))
    sys.exit(0 if overall_ok else 1)

if __name__ == '__main__':
    main()
