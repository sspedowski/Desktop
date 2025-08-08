"""Text extraction stubs. Expand with pdfplumber/docx2txt/ocr as needed."""
from __future__ import annotations
from pathlib import Path
from typing import List

# Optional imports (uncomment after installing libs)
# import pdfplumber
# import docx2txt

SUPPORTED_EXT = {".txt",".md"}  # Extend to .pdf, .docx when ready

def extract_text(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in (".txt",".md"):
        return path.read_text(encoding="utf-8", errors="ignore")
    # elif ext == ".pdf":
    #     with pdfplumber.open(str(path)) as pdf:
    #         return "\n".join(page.extract_text() or "" for page in pdf.pages)
    # elif ext == ".docx":
    #     return docx2txt.process(str(path)) or ""
    return f"UNSUPPORTED FILE TYPE: {ext}"

def batch_extract(paths: List[Path]) -> List[str]:
    return [extract_text(p) for p in paths]
