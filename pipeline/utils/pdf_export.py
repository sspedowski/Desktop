"""PDF export utilities: convert markdown outputs to PDF.

Primary path: markdown -> HTML -> PDF via WeasyPrint (if installed)
Fallback path: plain text -> simple PDF via ReportLab.
"""
from __future__ import annotations
from pathlib import Path
from typing import Optional

HTML_WRAPPER = """<html><head><meta charset='utf-8'><style>
body{font-family:Arial,Helvetica,sans-serif;line-height:1.35;font-size:12pt;margin:32px;color:#222}
h1,h2,h3,h4{color:#2a2a2a;margin-top:1.2em}
code,pre{background:#f5f5f5;padding:4px 6px;border-radius:4px;font-size:11pt}
table{border-collapse:collapse;width:100%;margin:12px 0}
th,td{border:1px solid #999;padding:4px 6px;font-size:10pt;vertical-align:top}
th{background:#eee}
</style></head><body>{content}</body></html>"""

def try_import_markdown():
    try:
        import markdown  # type: ignore
        return markdown
    except Exception:
        return None

def try_import_weasyprint():
    try:
        from weasyprint import HTML  # type: ignore
        return HTML
    except Exception:
        return None

def try_import_reportlab():
    try:
        from reportlab.lib.pagesizes import LETTER
        from reportlab.pdfgen import canvas
        return (LETTER, canvas)
    except Exception:
        return None

def md_to_html(md_text: str) -> str:
    md_mod = try_import_markdown()
    if md_mod:
        html_body = md_mod.markdown(md_text, extensions=['tables','fenced_code'])
    else:
        # crude fallback: wrap plain text
        html_body = f"<pre>{md_text}</pre>"
    return HTML_WRAPPER.format(content=html_body)

def html_to_pdf(html: str, out_path: Path) -> bool:
    HTML = try_import_weasyprint()
    if not HTML:
        return False
    try:
        HTML(string=html).write_pdf(str(out_path))
        return True
    except Exception:
        return False

def text_to_pdf_fallback(text: str, out_path: Path) -> None:
    rl = try_import_reportlab()
    if not rl:
        out_path.write_text(text, encoding='utf-8')  # last resort
        return
    LETTER, canvas = rl
    c = canvas.Canvas(str(out_path), pagesize=LETTER)
    width, height = LETTER
    margin = 54
    y = height - margin
    for line in text.splitlines() or [""]:
        if y < margin:
            c.showPage()
            y = height - margin
        c.drawString(margin, y, line[:140])
        y -= 14
    c.save()

def convert_markdown_file(md_path: Path, pdf_dir: Path) -> Optional[Path]:
    pdf_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = pdf_dir / (md_path.stem + '.pdf')
    md_text = md_path.read_text(encoding='utf-8', errors='ignore')
    html = md_to_html(md_text)
    if html_to_pdf(html, pdf_path):
        return pdf_path
    # fallback plain text
    text_to_pdf_fallback(md_text, pdf_path)
    return pdf_path

def bulk_convert(md_folder: Path, pdf_dir: Path) -> int:
    count = 0
    for md_path in md_folder.glob('*.md'):
        convert_markdown_file(md_path, pdf_dir)
        count += 1
    return count

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--in', dest='in_dir', required=True, help='Folder with markdown files')
    parser.add_argument('--out', dest='out_dir', required=True, help='Output PDF folder')
    args = parser.parse_args()
    n = bulk_convert(Path(args.in_dir), Path(args.out_dir))
    print(f'Converted {n} markdown files to PDF.')
