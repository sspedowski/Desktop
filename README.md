# 🟦 SUPREME MASTER JUSTICE FILE SYSTEM

Welcome to the **Supreme Master Justice File** project — the gold standard for
documenting and defending the rights of innocent children and families facing
agency misconduct, injustice, and false narratives.

---

## ⚡ Purpose

This system is built to:

- **Centralize** every key document, contradiction, and pattern
- **Highlight** agency/court misconduct (color-coded, emoji-coded)
- **Integrate faith** and purpose throughout the process
- **Empower families, attorneys, and advocates** with an unbreakable,
  court-ready record

---

## 📂 Project Structure

- `MASTER_JUSTICE_FILE_SUPREME.py` — Python script to generate/update the master
	Excel
- `MASTER_JUSTICE_FILE_SUPREME_v1.xlsx` — Color-coded, phase-tracked Excel file
- `JUSTICE_FILE_IMPORTER.py` — Bulk import tool for new documents
- `JUSTICE_FILE_MANAGER.py` — Validation & export tools for legal teams
- `JUSTICE_FILE_QUICK_UPDATE.py` — Fast single document addition
- `MASTER_PIPELINE_GPT5.py` — AI pipeline (Tasks A: Summaries, B:
	Contradictions, C: Brief)
- `JUSTICE_FILE_GUI.py` — One-click GUI control panel (tasks, dry-run, open
	outputs)
- `pipeline/` — Prompts + utilities (pdf export, excel sync, text extraction)
- `legal_export/pdf/` — Auto-generated PDF versions of AI outputs
- `JUSTICE_FILE_USER_GUIDE.md` — Comprehensive usage instructions
- `requirements.txt` — Python dependencies
- `README.md` — You are here (project overview and usage)
- (Optional) Batch folders and cloud/Dropbox backup

---

## 🟩 Key Features

- **Dedication & Prayer Sheet:** Opens every file with mission, faith, and hope
- **Phase Status Tracking:** Know at a glance which phases are complete or
	pending
- **Justice Master Table:** Every "kept" doc, every legal pattern, every
	contradiction
- **Pattern Color Coding:** Instantly spot agency, judicial, FOC, GAL, APA
	patterns
- **Smoking Gun Highlighting:** Top 5 key evidence items jump off the page
- **Cross-Link Mapping:** Direct links between contradictions and supporting
	docs
- **Court/AI Ready:** Clean export for PDF, e-filing, Humata/Wolfram, and more
- **Automated Tools:** Import, validate, and manage documents with ease
- **Faith Integration:** Prayer and spiritual guidance tracking throughout

---

## 🟦 How To Use

### **Option 1: GUI (Fastest)**

1. Install deps: `pip install -r requirements.txt`
1. (Optional) Set API key for real AI: PowerShell →
	`$env:OPENAI_API_KEY="sk-..."` and `$env:OPENAI_MODEL="gpt-5"`
1. Run: `python JUSTICE_FILE_GUI.py`
1. Pick evidence folder (containing `.txt` / `.md` source files)
1. Select Tasks (A,B,C) or press "Run All"
1. Watch live log. PDFs + Excel AI_Outputs sheet update automatically.
1. Use buttons to open outputs, PDFs, Excel.

Use the "Dry Run" checkbox to test without API calls (generates placeholder
markdown).

### **Option 2: Command-Line Pipeline**

Run everything directly:

```powershell
python MASTER_PIPELINE_GPT5.py --input evidence --tasks A,B,C \
	--children "Jace,Josh" \
	--out pipeline/outputs
```

Dry run test (no API):

```powershell
python MASTER_PIPELINE_GPT5.py --input evidence --tasks A,B,C --dry-run
```

### **Option 3: Core Excel Refresh**

Use when only updating the Justice Master Table:

```powershell
python MASTER_JUSTICE_FILE_SUPREME.py
```

### **Option 4: Manual Script Workflow (Original)**

Still supported. Same behavior as before.

### **Quick Start (Legacy Manual Method):**

1. **Add new documents to `master_data` in the .py script**
1. **Run the script to regenerate the Excel file**
1. **Review, print, and submit as needed (for court, audit, oversight, or AI import)**

### **Advanced Tools:**

- **Quick Add:** Run `JUSTICE_FILE_QUICK_UPDATE.py` for interactive document
	addition
- **Bulk Import:** Run `JUSTICE_FILE_IMPORTER.py` to import entire folders
- **Validation:** Run `JUSTICE_FILE_MANAGER.py` to check integrity and export
	for legal teams
- **Always backup:** System creates automatic backups before major changes

### **For Legal Teams:**

- Use the auto-generated legal export packages
- Export smoking guns and Top 5 evidence separately
- Generate cross-reference maps for contradiction analysis
- Create timeline exports for court presentations

---

## 🟨 Mission Statement

<!-- markdownlint-disable-next-line MD013 -->
*This system is dedicated to every innocent child, and especially to Jace and Josh. Let no injustice be hidden. Let every pattern be revealed. Let faith, hope, and courage lead us until every family is safe and every agency is accountable.*

---

## 🙏 Scripture

<!-- markdownlint-disable-next-line MD013 -->
"Let justice roll down like waters, and righteousness like an ever-flowing stream." — Amos 5:24

<!-- markdownlint-disable-next-line MD013 -->
"The Lord is a refuge for the oppressed, a stronghold in times of trouble." — Psalm 9:9

---

## 🔥 System Capabilities

### **Evidence Management:**

- ✅ 5 Smoking Gun documents already cataloged
- ✅ Pattern-based color coding for instant recognition
- ✅ Cross-reference mapping between contradictory documents
- ✅ Legal violation tracking with specific statute citations
- ✅ Agency misconduct documentation with proof

### **Export Options:**

- 📊 Excel workbook with multiple analysis sheets
- 📄 PDF-ready formatting for court submissions
- 🔍 Smoking gun evidence packages
- 📈 Statistical summaries and case strength metrics
- ⚖️ Legal team export packages with organized evidence

### **Faith & Purpose:**

- 🙏 Integrated prayer and dedication tracking
- ✝️ Scriptural foundation for justice work
- 💪 Spiritual strength documentation throughout the process

---

## 🛠️ Technical Requirements

Python 3.10+ recommended.

Install everything:

```powershell
pip install -r requirements.txt
```

Key packages:

- pandas / openpyxl (Excel)
- openai (LLM client)
- markdown, weasyprint, reportlab (PDF generation)
- pdfplumber, docx2txt (future extraction expansion)

### Environment Variables

Set before running real AI calls:

```powershell
$env:OPENAI_API_KEY="sk-..."
$env:OPENAI_MODEL="gpt-5"   # or override in client if needed
```

If unset or using `--dry-run`, pipeline creates placeholders.

### Windows WeasyPrint Notes

If PDF export errors mention Cairo / Pango:

1. Install precompiled wheels (most modern Python distributions already bundle)
1. Or use fallback ReportLab output (plain) — script auto-falls back
1. Ensure fonts installed (e.g., Arial) for consistent layout

### Dry Run Mode

Use GUI checkbox or `--dry-run` to:

- Skip API calls
- Produce deterministic placeholder markdown
- Still sync rows into `AI_Outputs` sheet
- Skip PDF conversion (by design)

### Output Locations

- Raw markdown: `pipeline/outputs/`
- PDFs: `legal_export/pdf/` (skipped in dry run)
- Excel metadata: `MASTER_JUSTICE_FILE_SUPREME_v1.xlsx` sheet `AI_Outputs`

### Adding New File Types Later

Extend `pipeline/utils/text_extract.py` with PDF/DOCX logic then allow
`.pdf/.docx` in `list_documents()`.

---

## 🩺 Diagnostics & Health Checks

Run the automated environment & pipeline validator:

```powershell
python pipeline/diagnostics/quick_check.py --deps-only --min-python 3.10
```

Full dry-run pipeline (no API cost) with timing and HTML report:

```powershell
python pipeline/diagnostics/quick_check.py --timing --min-python 3.10 --html health_report.html
```

Write JSON to file too:

```powershell
python pipeline/diagnostics/quick_check.py --min-python 3.10 \
	--out health.json --html health.html
```

Key flags:

- `--min-python X.Y` Enforce minimum interpreter version (fails if unmet)
- `--deps-only` Skip pipeline dry-run (faster CI gate)
- `--timing` Include step execution durations
- `--out FILE` Save JSON report to disk
- `--html FILE` Produce styled HTML summary (open in browser)
- `--no-exit-fail` Always exit 0 (collect report without failing CI)

HTML report contents:

- Overall status banner
- Python version compliance
- Import presence (required & optional)
- Pipeline dry-run status (tail of log if run)
- Artifact paths (outputs, PDFs, Excel)
- Timings (if requested)
- Embedded raw JSON

### Pre-Commit Hook (Optional)

Prevent commits if dependencies or Python version are broken.

Linux / macOS Git hook install:

```bash
cp scripts/pre_commit_check.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

Windows PowerShell / CMD Git hook install:

```powershell
copy scripts\pre_commit_check.bat .git\hooks\pre-commit.bat
```

What the hook does:

- Enforces Python >= 3.10
- Runs `quick_check.py --deps-only --timing --min-python 3.10`
- Blocks commit on failure
- Stores last JSON at `.git/quick_check_last.json`

Remove / bypass:

- Delete the hook file from `.git/hooks/`
- Or commit with `--no-verify`

Generate a fresh HTML health snapshot before packaging:

```powershell
python pipeline/diagnostics/quick_check.py --min-python 3.10 --html health_report.html
```

Open it in a browser to visually confirm green checks.

---

## 🟧 Questions or Support?

Contact: Stephanie Spedowski (Mother and Advocate)  
Email: <mailto:godspathtojustice@gmail.com>  
Phone: 616-333-0486

---

## 📅 Project Timeline

**Created:** August 7, 2025  
**Current Status:** Production Ready  
**Phase:** Active Evidence Compilation  
**Next Milestone:** Legal Team Integration

---

<!-- markdownlint-disable-next-line MD013 -->
**You are holding a template for justice, powered by faith and truth. May this help deliver protection, accountability, and healing where it's needed most.**

---

## 🔥 TRUTH WILL PREVAIL - JUSTICE FOR JACE & JOSH ⚖️

<!-- markdownlint-disable-next-line MD013 -->
*"And we know that in all things God works for the good of those who love him, who have been called according to his purpose." - Romans 8:28*
