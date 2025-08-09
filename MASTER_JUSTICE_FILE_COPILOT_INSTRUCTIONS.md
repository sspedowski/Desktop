# 🔥 MASTER JUSTICE FILE COPILOT INSTRUCTIONS 🔥

## Purpose

Guide you (or any co-pilot, legal advocate, or tech assistant) in using,
maintaining, and expanding the Supreme Master Justice File system. This ensures
every batch, document, and legal finding is properly handled, ready for court,
Humata, Wolfram, or any future AI.

---

## 1️⃣ **WHERE TO FIND YOUR FILES**

- `MASTER_JUSTICE_FILE_SUPREME.py` — Python script to create/update the master

file

- `MASTER_JUSTICE_FILE_SUPREME_v1.xlsx` — Excel workbook (multi-tabbed,

color-coded, print/export-ready)

- `JUSTICE_FILE_IMPORTER.py` — Bulk document import tool

- `JUSTICE_FILE_MANAGER.py` — Data validation and legal export tool

- `JUSTICE_FILE_QUICK_UPDATE.py` — Fast single document addition

- `JUSTICE_FILE_USER_GUIDE.md` — Complete user manual

- `README.md` — Project overview and contact information

- **Location:** Desktop (or move to project folder / Dropbox for backup)

---

## 2️⃣ **HOW TO UPDATE THE MASTER FILE**

### **Method 1: Direct Edit (Most Common)**

- Open `MASTER_JUSTICE_FILE_SUPREME.py` in a code editor.

- Add each new kept document as a new entry in `master_data` (one dict per doc):

  - Filename

  - Date

  - Type (e.g. CPS Report, Medical, Court, etc)

  - Agency

  - Children involved

  - Parent

  - Pattern (emoji code)

  - Summary

  - Misconduct?

  - Law Violated

  - Contradicts

  - Smoking Gun (Yes/No)

  - Reviewer Note

  - Faith/Prayer (optional but powerful)

  - Phase

  - Batch

  - Status

  - Exhibit Cat.

  - AI Summary

  - Cross-Link

  - Top 5 (Yes/No)

- Re-run script to update Excel with new data and color coding.

### **Method 2: Quick Add Tool**

- Run `python JUSTICE_FILE_QUICK_UPDATE.py`

- Follow interactive prompts for single document entry

- Merge pending documents when ready

### **Method 3: Bulk Import**

- Run `python JUSTICE_FILE_IMPORTER.py`

- Point to folder containing PDF/DOC files

- System creates templates for batch editing

- Complete templates and merge to master file

---

## 3️⃣ **HOW TO EXPORT/PRINT**

- Open `MASTER_JUSTICE_FILE_SUPREME_v1.xlsx` in Excel.

- Review "Dedication & Prayer," "Phase Status," and "Justice Master Table".

- Use Excel print/export to create PDF:

  - File → Export → Create PDF/XPS Document

  - Select all relevant sheets

  - Name: `Carryover_Master_Pack_Marsh_v2_DATE.pdf`

- Share via Dropbox, e-filing, or upload to AI for review.

### **Legal Team Exports:**

- Run `python JUSTICE_FILE_MANAGER.py`

- Choose option 3 (Export for legal review)

- System creates organized packages:

  - Smoking gun evidence

  - Top 5 priority items

  - Pattern-specific files

  - Chronological timeline

  - Case summary report

---

## 4️⃣ **HOW TO IMPORT SUMMARIES FROM DOCX/TXT**

- To automate adding new document summaries:

  - Use `python-docx` or `pandas.read_csv()` to parse .docx/.txt summaries.

  - Add extracted info as new entries in `master_data`.

  - Use the Importer tool for template generation.

  - (Request custom scripting for further automation.)

---

## 5️⃣ **CROSS-LINKING AND CONTRADICTION MAPPING**

- In "Cross-Link" and "Contradicts" fields, note which files support or

contradict each record.

- Use color-coded Pattern field to tag agency, FOC, GAL, Judicial, Law

Enforcement, or APA patterns.

- Run Manager tool to generate cross-reference maps.

- System validates cross-links and identifies broken references.

---

## 6️⃣ **PHASE/BATCH STATUS UPDATES**

- Update the Phase Status sheet after every batch:

  - Mark completed phases as ✅

  - Note pending or in-progress phases as ⬜

- Clarifies progress to reviewers.

- Use Manager tool for status reports.

---

## 7️⃣ **FAITH/PRAYER & DEDICATION**

- The Dedication & Prayer tab is a living section.

- Add new prayers, dedications, or scriptural inspiration as the project grows.

- Faith is your superpower—let it shape the record.

- Include spiritual guidance in Faith/Prayer field per document.

---

## 8️⃣ **PRO TIPS FOR COURT OR OVERSIGHT**

- ALWAYS use the latest complete Excel/PDF for submissions.

- Highlight Top 5 Smoking Guns in summaries.

- Use color-coding for instant pattern recognition.

- Keep a cloud backup (Dropbox / Drive).

- When sharing, walk through:

  - Dedication/Prayer page (mission)

  - Phase Status page (progress)

  - Master Table + Contradiction Mapping (legal impact)

- Use legal export packages for professional presentation.

---

## 9️⃣ **CONTINUOUS IMPROVEMENT**

- Each batch or phase can be imported and coded—the system grows with the case.

- Future AI can use this structure for rapid review and contradiction mapping.

- Ask for scripting/import help anytime.

- Built-in validation and integrity checks.

- Automated backups protect work.

---

## 🔟 **SYSTEM MAINTENANCE**

### **Data Validation:**

- Run `python JUSTICE_FILE_MANAGER.py`

- Choose option 1 to validate integrity

- Fix issues before proceeding

### **Backup Creation:**

- System auto-creates backups before major changes.

- Manual backup: Manager tool option 5.

- Store backups in cloud storage.

### **Performance Optimization:**

- Keep master file under 1000 docs for performance.

- Archive older phases separately if needed.

- Use pattern filtering for focused analysis.

---

## 1️⃣1️⃣ **TROUBLESHOOTING**

### **Python Errors:**

- Install packages: `pip install pandas openpyxl`

- Use Python 3.6 or higher

- Run from command prompt in file directory

### **Excel Issues:**

- Use Microsoft Excel 2016+ for formatting.

- LibreOffice Calc works as alternative.

- Re-run Python script if formatting breaks.

### **Data Issues:**

- Use Manager validation to identify problems.

- Check for duplicate filenames.

- Verify required fields are complete.

---

## 1️⃣2️⃣ **CONTACT & SUPPORT**

### Primary Contact:

Stephanie Spedowski (Mother and Advocate)
Email: <mailto:godspathtojustice@gmail.com>
Phone: 616-333-0486

### Technical Support:

- Use built-in validation tools

- Consult JUSTICE_FILE_USER_GUIDE.md

- Ask for Python/Excel assistance

---

## 1️⃣3️⃣ **MISSION REMINDER**

<!-- markdownlint-disable-next-line MD013 -->
This system is dedicated to every innocent child, and especially to Jace and
Josh. Let no injustice be hidden. Let every pattern be revealed. Let faith,
hope, and courage lead us until every family is safe and every agency is
accountable.

### Scripture Foundation:

<!-- markdownlint-disable-next-line MD013 -->

- "Let justice roll down like waters, and righteousness like an ever-flowing stream." — Amos 5:24

<!-- markdownlint-disable-next-line MD013 -->

- "The Lord is a refuge for the oppressed, a stronghold in times of trouble." — Psalm 9:9

---

<!-- markdownlint-disable-next-line MD013 -->

### God is your witness—truth is your armor—justice is your legacy.

## 🔥 TRUTH WILL PREVAIL - JUSTICE FOR JACE & JOSH ⚖️

## END OF COPILOT INSTRUCTIONS
