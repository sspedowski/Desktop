"""Master GPT-5 pipeline orchestrator.
Run tasks:
 A: Per-document structured summaries
 B: Contradiction mapping
 C: Evidence brief

Example:
 python MASTER_PIPELINE_GPT5.py --input ./evidence --tasks A,B,C --children "Jace,Josh" --out ./pipeline/outputs
"""
from __future__ import annotations
import argparse
from pathlib import Path
from typing import List, Dict
import pandas as pd

from pipeline.gpt5_client import get_client
from pipeline.utils.io_utils import write_text
from pipeline.utils.pdf_export import bulk_convert
from pipeline.utils.excel_sync import sync_markdowns
from pipeline.utils.text_extract import extract_text

PROMPTS_DIR = Path("pipeline/prompts")

def load_prompt(name: str) -> str:
    return (PROMPTS_DIR / name).read_text(encoding="utf-8")

def list_documents(input_dir: Path) -> List[Path]:
    exts = {".txt",".md"}  # Extend as extractors added
    return [p for p in input_dir.iterdir() if p.suffix.lower() in exts]

def task_A_summaries(docs: List[Path], children: str, out_dir: Path) -> List[Dict]:
    client = get_client()
    system = "You are a disciplined legal evidence summarizer producing structured outputs."
    template = load_prompt("A_SUMMARY.txt")
    results = []
    for doc in docs:
        raw = extract_text(doc)
        prompt = f"{template}\n\nFILENAME: {doc.name}\nCHILDREN: {children}\nRAW CONTENT (truncate if huge):\n{raw[:12000]}"
        completion = client.complete(system, prompt)
        out_path = out_dir / f"SUMMARY_{doc.stem}.md"
        write_text(out_path, completion)
        results.append({"filename": doc.name, "output": str(out_path)})
    return results

def task_B_contradictions(docs: List[Path], out_dir: Path):
    client = get_client()
    system = "You map contradictions precisely."
    template = load_prompt("B_CONTRADICTIONS.txt")
    combined = []
    for doc in docs:
        combined.append(f"== {doc.name} ==\n" + extract_text(doc)[:8000])
    prompt = f"{template}\n\nDOCUMENT SET RAW EXTRACTS:\n\n" + "\n\n".join(combined)
    completion = client.complete(system, prompt)
    out_path = out_dir / "CONTRADICTIONS_MAP.md"
    write_text(out_path, completion)
    return str(out_path)

def task_C_brief(docs: List[Path], out_dir: Path):
    client = get_client()
    system = "You draft structured court-oriented evidence briefs."
    template = load_prompt("C_BRIEF.txt")
    snippets = []
    for doc in docs:
        snippets.append(f"== {doc.name} ==\n" + extract_text(doc)[:6000])
    prompt = f"{template}\n\nSOURCE DOCUMENT SNIPPETS:\n" + "\n\n".join(snippets)
    completion = client.complete(system, prompt)
    out_path = out_dir / "EVIDENCE_BRIEF.md"
    write_text(out_path, completion)
    return str(out_path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Folder containing source evidence text files")
    parser.add_argument("--tasks", default="A,B,C", help="Comma list of tasks: A,B,C")
    parser.add_argument("--children", default="Jace,Josh", help="Children names for context")
    parser.add_argument("--out", default="pipeline/outputs", help="Output directory")
    args = parser.parse_args()

    input_dir = Path(args.input)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    docs = list_documents(input_dir)
    if not docs:
        print("No supported documents (.txt/.md) found in input folder.")
        return
    print(f"Found {len(docs)} documents.")

    tasks = {t.strip().upper() for t in args.tasks.split(',') if t.strip()}

    if 'A' in tasks:
        print("Running Task A (Summaries)...")
        task_A_summaries(docs, args.children, out_dir)
        print("Task A complete.")
    if 'B' in tasks:
        print("Running Task B (Contradictions)...")
        task_B_contradictions(docs, out_dir)
        print("Task B complete.")
    if 'C' in tasks:
        print("Running Task C (Evidence Brief)...")
        task_C_brief(docs, out_dir)
        print("Task C complete.")

    print(f"Outputs written to: {out_dir}")
    # PDF export stage
    pdf_dir = Path("legal_export/pdf")
    try:
        converted = bulk_convert(out_dir, pdf_dir)
        print(f"PDF export complete: {converted} files -> {pdf_dir}")
    except Exception as e:
        print(f"PDF export skipped (error): {e}")

    # Excel sync stage
    excel_path = Path("MASTER_JUSTICE_FILE_SUPREME_v1.xlsx")
    try:
        added = sync_markdowns(out_dir, excel_path, ",".join(sorted(tasks)), args.children, pdf_dir)
        print(f"Excel sync: {added} new rows into AI_Outputs sheet.")
    except Exception as e:
        print(f"Excel sync skipped (error): {e}")

if __name__ == "__main__":
    main()
