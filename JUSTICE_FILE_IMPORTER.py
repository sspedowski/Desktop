"""
JUSTICE FILE DOCUMENT IMPORTER
Automatically import and process new documents into the Master Justice File system
"""

import pandas as pd
import os
from datetime import datetime
import re
from pathlib import Path
import json

class JusticeFileImporter:
    def __init__(self):
        self.new_documents = []
        self.patterns = {
            "🟥 CPS Minimization": ["minimization", "within normal", "no concerns", "insufficient"],
            "🟥 Omission": ["omitted", "failed to", "did not include", "missing"],
            "🟥 Misconduct": ["violation", "improper", "misconduct", "failure"],
            "🟩 Validation": ["validates", "confirms", "supports", "correct"],
            "🟩 Victory": ["dismissed", "vindicated", "successful", "granted"],
            "🟦 Legal Action": ["motion", "petition", "complaint", "lawsuit"],
            "🟨 Warning": ["concern", "issue", "problem", "discrepancy"],
            "🟧 Important": ["critical", "significant", "major", "key"]
        }
    
    def scan_folder_for_documents(self, folder_path):
        """Scan a folder for new PDF/DOC files to import"""
        folder = Path(folder_path)
        supported_types = ['.pdf', '.docx', '.doc', '.txt']
        
        found_files = []
        for file_type in supported_types:
            found_files.extend(folder.glob(f'*{file_type}'))
        
        print(f"📁 Found {len(found_files)} documents to review:")
        for file in found_files:
            print(f"   • {file.name}")
        
        return found_files
    
    def analyze_filename(self, filename):
        """Extract information from filename patterns"""
        filename_lower = filename.lower()
        
        # Extract date patterns
        date_patterns = [
            r'(\d{1,2}[\.\-/]\d{1,2}[\.\-/]\d{2,4})',  # MM.DD.YY or MM/DD/YYYY
            r'(\d{4}[\.\-/]\d{1,2}[\.\-/]\d{1,2})',    # YYYY.MM.DD
        ]
        
        extracted_date = None
        for pattern in date_patterns:
            match = re.search(pattern, filename)
            if match:
                extracted_date = match.group(1)
                break
        
        # Identify document type
        doc_type = "Unknown"
        if any(word in filename_lower for word in ['cps', 'child protective']):
            doc_type = "CPS Report"
        elif any(word in filename_lower for word in ['medical', 'exam', 'ywca']):
            doc_type = "Medical"
        elif any(word in filename_lower for word in ['court', 'order', 'motion']):
            doc_type = "Legal/Court"
        elif any(word in filename_lower for word in ['review', 'committee']):
            doc_type = "Independent Review"
        elif any(word in filename_lower for word in ['police', 'officer', 'report']):
            doc_type = "Law Enforcement"
        
        # Identify agency
        agency = "Unknown"
        if 'cps' in filename_lower:
            agency = "CPS"
        elif 'ywca' in filename_lower:
            agency = "YWCA"
        elif 'court' in filename_lower:
            agency = "Court"
        elif 'police' in filename_lower:
            agency = "Law Enforcement"
        
        return {
            "date": extracted_date,
            "doc_type": doc_type,
            "agency": agency
        }
    
    def auto_detect_pattern(self, summary_text):
        """Auto-detect pattern based on summary content"""
        summary_lower = summary_text.lower()
        
        for pattern, keywords in self.patterns.items():
            if any(keyword in summary_lower for keyword in keywords):
                return pattern
        
        return "🟨 Review Needed"
    
    def create_document_template(self, filename, analysis):
        """Create a template entry for a new document"""
        template = {
            "Filename": filename,
            "Date": analysis["date"] or "YYYY-MM-DD",
            "Type": analysis["doc_type"],
            "Agency": analysis["agency"],
            "Children": "Jace, Josh",  # Default - can be modified
            "Parent": "Stephanie",
            "Pattern": "🟨 Review Needed",  # Will be updated after manual review
            "Summary": "[SUMMARY NEEDED - Review document and add key findings]",
            "Misconduct?": "Review Needed",
            "Law Violated": "Review Needed",
            "Contradicts": "[Cross-reference with existing documents]",
            "Smoking Gun": "Review Needed",
            "Reviewer Note": f"Auto-imported on {datetime.now().strftime('%Y-%m-%d')}",
            "Faith/Prayer": "[Add prayer/dedication if applicable]",
            "Phase": "Phase 3",  # Current phase
            "Batch": "Current",
            "Status": "⬜ Review",
            "Exhibit Cat.": analysis["doc_type"],
            "AI Summary": "[Pending manual review]",
            "Cross-Link": "[To be determined after review]",
            "Top 5": "Review Needed"
        }
        return template
    
    def import_document_batch(self, folder_path, output_file="new_documents_template.json"):
        """Import a batch of documents and create templates"""
        files = self.scan_folder_for_documents(folder_path)
        
        templates = []
        for file in files:
            analysis = self.analyze_filename(file.name)
            template = self.create_document_template(file.name, analysis)
            templates.append(template)
        
        # Save templates as JSON for easy editing
        with open(output_file, 'w') as f:
            json.dump(templates, f, indent=2)
        
        print(f"\n✅ Created {len(templates)} document templates")
        print(f"📄 Templates saved to: {output_file}")
        print("\n📝 NEXT STEPS:")
        print("1. Review and edit the JSON file with actual document summaries")
        print("2. Update patterns, misconduct flags, and smoking gun status")
        print("3. Run merge_templates_to_master() to add to main file")
        
        return templates
    
    def merge_templates_to_master(self, template_file="new_documents_template.json", 
                                master_file="MASTER_JUSTICE_FILE_SUPREME.py"):
        """Merge completed templates into the master Python file"""
        
        # Load templates
        with open(template_file, 'r') as f:
            new_docs = json.load(f)
        
        # Read current master file
        with open(master_file, 'r') as f:
            master_content = f.read()
        
        # Find the end of master_data list
        insert_point = master_content.find("]", master_content.find("master_data = ["))
        
        # Format new documents as Python dict strings
        new_entries = ""
        for doc in new_docs:
            new_entries += "    {\n"
            for key, value in doc.items():
                if isinstance(value, str):
                    new_entries += f'        "{key}": "{value}",\n'
                else:
                    new_entries += f'        "{key}": {value},\n'
            new_entries += "    },\n"
        
        # Insert new entries before the closing bracket
        updated_content = (
            master_content[:insert_point-1] + 
            ",\n" + new_entries.rstrip(",\n") + "\n" + 
            master_content[insert_point:]
        )
        
        # Create backup
        backup_file = f"MASTER_JUSTICE_FILE_SUPREME_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        with open(backup_file, 'w') as f:
            f.write(master_content)
        
        # Write updated file
        with open(master_file, 'w') as f:
            f.write(updated_content)
        
        print(f"✅ Merged {len(new_docs)} new documents into master file")
        print(f"💾 Backup created: {backup_file}")
        print("🔥 Run the master script to update Excel file!")

def main():
    """Interactive document import process"""
    importer = JusticeFileImporter()
    
    print("🔥 JUSTICE FILE DOCUMENT IMPORTER 🔥")
    print("⚖️ Automated system for adding new evidence ⚖️\n")
    
    while True:
        print("\nChoose an option:")
        print("1. Scan folder for new documents")
        print("2. Merge completed templates to master file")
        print("3. Exit")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            folder = input("Enter folder path to scan: ").strip()
            if os.path.exists(folder):
                importer.import_document_batch(folder)
            else:
                print("❌ Folder not found!")
        
        elif choice == "2":
            template_file = input("Template file (default: new_documents_template.json): ").strip()
            if not template_file:
                template_file = "new_documents_template.json"
            
            if os.path.exists(template_file):
                importer.merge_templates_to_master(template_file)
            else:
                print("❌ Template file not found!")
        
        elif choice == "3":
            print("🙏 Justice will prevail! God bless.")
            break
        
        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
