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
import time
import argparse

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


def parse_version_tuple(spec: str):
    parts = spec.strip().split('.')
    try:
        nums = [int(p) for p in parts if p.isdigit()]
        while len(nums) < 2:
            nums.append(0)
        return tuple(nums[:3]) if len(nums) >= 3 else (nums[0], nums[1], 0)
    except Exception:
        return (0,0,0)

def check_python(min_required: tuple[int,int,int]|None=None):
    ver = sys.version_info
    meets_default = ver >= (3,9)
    meets_user = True
    if min_required:
        meets_user = ver >= min_required
    return {
        'version': f'{ver.major}.{ver.minor}.{ver.micro}',
        'ok': meets_default and meets_user,
        'meets_default_3_9': meets_default,
        'meets_min_spec': meets_user,
        'min_required': '.'.join(str(x) for x in min_required) if min_required else None
    }


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


def run_dry_pipeline(timing: bool=False):
    t0 = time.time()
    if not PIPELINE.exists():
        return {'ok': False, 'error': 'Pipeline script missing'}
    ensure_sample_evidence()
    cmd = [sys.executable, str(PIPELINE), '--input', str(EVIDENCE_DIR), '--tasks', 'A,B,C', '--children', 'HealthCheckChild', '--out', str(OUTPUT_DIR), '--dry-run']
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        ok = proc.returncode == 0
        lines = proc.stdout.strip().splitlines()
        tail = lines[-12:]
        result = {
            'ok': ok,
            'returncode': proc.returncode,
            'tail': tail,
            'stdout_bytes': len(proc.stdout.encode('utf-8')),
            'stderr': proc.stderr.strip() or None
        }
        if timing:
            result['duration_sec'] = round(time.time() - t0, 3)
        return result
    except subprocess.TimeoutExpired:
        r = {'ok': False, 'error': 'Pipeline timeout'}
        if timing:
            r['duration_sec'] = round(time.time() - t0, 3)
        return r
    except Exception as e:
        r = {'ok': False, 'error': str(e)}
        if timing:
            r['duration_sec'] = round(time.time() - t0, 3)
        return r


def scan_outputs(verbose: bool=False):
    outputs = list(OUTPUT_DIR.glob('*.md'))
    pdfs = list(PDF_DIR.glob('*.pdf'))
    data = {
        'md_files': len(outputs),
        'pdf_files': len(pdfs),
        'excel_exists': EXCEL.exists()
    }
    if verbose:
        data['md_list'] = [p.name for p in outputs]
        data['pdf_list'] = [p.name for p in pdfs]
    return data


def main():
    parser = argparse.ArgumentParser(description='Justice File quick environment & pipeline checker')
    parser.add_argument('--deps-only', action='store_true', help='Only verify Python & imports; skip dry-run pipeline execution')
    parser.add_argument('--timing', action='store_true', help='Include timing metrics for steps')
    parser.add_argument('--out', type=str, help='Write JSON report to this file path')
    parser.add_argument('--verbose', action='store_true', help='Include detailed artifact file lists')
    parser.add_argument('--no-exit-fail', action='store_true', help='Always exit 0 even if failures (CI collection)')
    parser.add_argument('--min-python', type=str, help='Minimum Python version required (e.g. 3.10)')
    parser.add_argument('--html', type=str, help='Write an HTML report to the given file path')
    args = parser.parse_args()

    timings = {}
    t_start = time.time()
    min_spec = parse_version_tuple(args.min_python) if args.min_python else None
    t0 = time.time(); py_info = check_python(min_spec); timings['python_check'] = round(time.time()-t0,3) if args.timing else None
    t0 = time.time(); imports = check_imports(); timings['import_check'] = round(time.time()-t0,3) if args.timing else None

    deps_missing = (not py_info['ok']) or (not imports['pdf_engine_ok']) or any(not imports.get(m) for m in CORE_MODULES)
    auto_deps_only = False
    if deps_missing and not args.deps_only:
        auto_deps_only = True

    pipeline_result = {'skipped': True}
    artifacts = {'md_files': 0, 'pdf_files': 0, 'excel_exists': EXCEL.exists()}
    if not (args.deps_only or auto_deps_only):
        t0 = time.time(); pipeline_result = run_dry_pipeline(timing=args.timing); timings['pipeline_run'] = round(time.time()-t0,3) if args.timing else None
    t0 = time.time(); artifacts = scan_outputs(verbose=args.verbose); timings['artifact_scan'] = round(time.time()-t0,3) if args.timing else None

    overall_ok = py_info['ok'] and imports['pdf_engine_ok'] and all(imports.get(m) for m in CORE_MODULES)
    if not (args.deps_only or auto_deps_only):
        overall_ok = overall_ok and pipeline_result.get('ok', False)

    report = {
        'python': py_info,
        'imports': imports,
        'pipeline': pipeline_result,
        'artifacts': artifacts,
        'overall_ok': overall_ok,
        'mode': 'deps-only' if (args.deps_only or auto_deps_only) else 'full',
    }
    if auto_deps_only:
        report['note'] = 'Dependencies missing -> auto switched to deps-only mode'
    if args.timing:
        timings['total'] = round(time.time()-t_start,3)
        report['timings'] = {k:v for k,v in timings.items() if v is not None}
    json_text = json.dumps(report, indent=2)
    print(json_text)
    if args.out:
        try:
            Path(args.out).write_text(json_text, encoding='utf-8')
        except Exception as e:
            print(f"[warn] Could not write report file: {e}")
    if args.html:
        try:
            html = [
                '<!DOCTYPE html><html><head><meta charset="utf-8"/>',
                '<title>Justice File Health Report</title>',
                '<style>body{font-family:Segoe UI,Arial,sans-serif;margin:20px;}h1{margin-top:0}pre{background:#111;color:#0f0;padding:12px;overflow:auto;}table{border-collapse:collapse;margin:16px 0;}td,th{border:1px solid #ccc;padding:6px 10px;font-size:14px;}th{background:#f5f5f5;text-align:left;} .bad{color:#b00;font-weight:bold;} .ok{color:#060;font-weight:bold;} .sec{margin-top:32px;} code{background:#eee;padding:2px 4px;border-radius:4px;} </style>',
                '</head><body>',
                '<h1>Justice File Health Report</h1>'
            ]
            html.append('<h2>Summary</h2><table>')
            html.append('<tr><th>Overall OK</th><td class="{}">{}</td></tr>'.format('ok' if report['overall_ok'] else 'bad', report['overall_ok']))
            html.append('<tr><th>Mode</th><td>{}</td></tr>'.format(report['mode']))
            if report.get('note'):
                html.append('<tr><th>Note</th><td>{}</td></tr>'.format(report['note']))
            html.append('</table>')
            # Python
            py = report['python']
            html.append('<h2>Python</h2><table>')
            for k in ['version','min_required','meets_default_3_9','meets_min_spec','ok']:
                if py.get(k) is not None:
                    v = py.get(k)
                    cls = 'ok' if v is True else ('bad' if v is False and k in ('ok','meets_min_spec','meets_default_3_9') else '')
                    html.append(f'<tr><th>{k}</th><td class="{cls}">{v}</td></tr>')
            html.append('</table>')
            # Imports
            html.append('<h2>Imports</h2><table>')
            imp = report['imports']
            for k,v in imp.items():
                if isinstance(v,(list,tuple)):
                    disp = ', '.join(v)
                    html.append(f'<tr><th>{k}</th><td>{disp}</td></tr>')
                else:
                    cls = 'ok' if v is True else ('bad' if v is False and k not in ('tkinter',) else '')
                    html.append(f'<tr><th>{k}</th><td class="{cls}">{v}</td></tr>')
            html.append('</table>')
            # Pipeline
            html.append('<h2>Pipeline</h2><table>')
            pipe = report['pipeline']
            for k,v in pipe.items():
                if k == 'tail':
                    continue
                html.append(f'<tr><th>{k}</th><td>{v}</td></tr>')
            html.append('</table>')
            if pipe.get('tail'):
                tail_block = '\n'.join(pipe['tail'])
                html.append('<h3>Log Tail</h3><pre>{}</pre>'.format(
                    tail_block.replace('&','&amp;').replace('<','&lt;')
                ))
            # Artifacts
            art = report['artifacts']
            html.append('<h2>Artifacts</h2><table>')
            for k,v in art.items():
                html.append(f'<tr><th>{k}</th><td>{v}</td></tr>')
            html.append('</table>')
            # Timings
            if report.get('timings'):
                html.append('<h2>Timings</h2><table>')
                for k,v in report['timings'].items():
                    html.append(f'<tr><th>{k}</th><td>{v} s</td></tr>')
                html.append('</table>')
            html.append('<h2>Raw JSON</h2><pre>{}</pre>'.format(
                json_text.replace('&','&amp;').replace('<','&lt;')
            ))
            html.append('</body></html>')
            Path(args.html).write_text('\n'.join(html), encoding='utf-8')
        except Exception as e:
            print(f"[warn] Could not write HTML report: {e}")
    if args.no_exit_fail:
        sys.exit(0)
    sys.exit(0 if overall_ok else 1)

if __name__ == '__main__':
    main()
