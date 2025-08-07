"""
JUSTICE FILE QUICK UPDATE HELPER
Fast tools for adding single documents or making quick updates
"""

import json
import os
from datetime import datetime

class QuickUpdate:
    def __init__(self):
        self.patterns = {
            "1": "🟥 CPS Minimization",
            "2": "🟥 Omission", 
            "3": "🟥 Misconduct",
            "4": "🟩 Validation",
            "5": "🟩 Victory",
            "6": "🟦 Legal Action",
            "7": "🟨 Warning",
            "8": "🟧 Important"
        }
        
        self.doc_types = {
            "1": "CPS Report",
            "2": "Medical Forensic Exam",
            "3": "Court Order", 
            "4": "Legal Motion",
            "5": "Independent Review",
            "6": "Police Report",
            "7": "Medical Record",
            "8": "Email/Communication",
            "9": "Other"
        }
        
        self.agencies = {
            "1": "CPS",
            "2": "YWCA",
            "3": "Circuit Court",
            "4": "Attorney",
            "5": "Independent Review Committee",
            "6": "Law Enforcement",
            "7": "Medical",
            "8": "Other"
        }
    
    def quick_add_document(self):
        """Interactive quick add for a single document"""
        print("🔥 QUICK ADD NEW DOCUMENT TO JUSTICE FILE 🔥\n")
        
        # Basic info
        filename = input("📄 Filename: ").strip()
        if not filename:
            print("❌ Filename required!")
            return None
            
        date = input("📅 Date (YYYY-MM-DD): ").strip()
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # Document type
        print("\n📋 Document Type:")
        for key, value in self.doc_types.items():
            print(f"   {key}. {value}")
        doc_type_choice = input("Choose type (1-9): ").strip()
        doc_type = self.doc_types.get(doc_type_choice, "Other")
        
        # Agency
        print("\n🏢 Agency:")
        for key, value in self.agencies.items():
            print(f"   {key}. {value}")
        agency_choice = input("Choose agency (1-8): ").strip()
        agency = self.agencies.get(agency_choice, "Other")
        
        # Summary
        print("\n📝 Document Summary:")
        summary = input("Enter brief summary: ").strip()
        if not summary:
            summary = "[Summary needed]"
        
        # Pattern
        print("\n🎨 Pattern Classification:")
        for key, value in self.patterns.items():
            print(f"   {key}. {value}")
        pattern_choice = input("Choose pattern (1-8): ").strip()
        pattern = self.patterns.get(pattern_choice, "🟨 Review Needed")
        
        # Smoking gun
        smoking_gun = input("\n🔥 Is this smoking gun evidence? (y/n): ").strip().lower()
        smoking_gun = "Yes" if smoking_gun == 'y' else "No"
        
        # Misconduct
        misconduct = input("📋 Documents misconduct? (y/n): ").strip().lower()
        misconduct = "Yes" if misconduct == 'y' else "No"
        
        # Law violated
        law_violated = input("⚖️ Law violated (or N/A): ").strip()
        if not law_violated:
            law_violated = "N/A"
        
        # Contradicts
        contradicts = input("🔍 What does this contradict?: ").strip()
        if not contradicts:
            contradicts = "N/A"
        
        # Top 5
        top5 = input("⭐ Top 5 priority? (y/n): ").strip().lower()
        top5 = "Yes" if top5 == 'y' else "No"
        
        # Create document entry
        document = {
            "Filename": filename,
            "Date": date,
            "Type": doc_type,
            "Agency": agency,
            "Children": "Jace, Josh",
            "Parent": "Stephanie",
            "Pattern": pattern,
            "Summary": summary,
            "Misconduct?": misconduct,
            "Law Violated": law_violated,
            "Contradicts": contradicts,
            "Smoking Gun": smoking_gun,
            "Reviewer Note": f"Quick-added on {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "Faith/Prayer": "",
            "Phase": "Current",
            "Batch": "Quick Add",
            "Status": "✅ Include",
            "Exhibit Cat.": doc_type,
            "AI Summary": "[Pending detailed review]",
            "Cross-Link": "[To be determined]",
            "Top 5": top5
        }
        
        return document
    
    def save_quick_add(self, document):
        """Save quick-added document to pending file"""
        pending_file = "quick_add_pending.json"
        
        # Load existing pending documents
        pending_docs = []
        if os.path.exists(pending_file):
            with open(pending_file, 'r') as f:
                pending_docs = json.load(f)
        
        # Add new document
        pending_docs.append(document)
        
        # Save updated pending list
        with open(pending_file, 'w') as f:
            json.dump(pending_docs, f, indent=2)
        
        print(f"\n✅ Document added to pending queue!")
        print(f"📄 File: {pending_file}")
        print("🔄 Run merge_pending_documents() to add to master file")
    
    def merge_pending_documents(self):
        """Merge all pending documents into master file"""
        pending_file = "quick_add_pending.json"
        
        if not os.path.exists(pending_file):
            print("❌ No pending documents found!")
            return
        
        # Load pending documents
        with open(pending_file, 'r') as f:
            pending_docs = json.load(f)
        
        if not pending_docs:
            print("❌ No pending documents to merge!")
            return
        
        print(f"📋 Found {len(pending_docs)} pending documents:")
        for i, doc in enumerate(pending_docs, 1):
            print(f"   {i}. {doc['Filename']}")
        
        confirm = input(f"\nMerge all {len(pending_docs)} documents? (y/n): ").strip().lower()
        if confirm != 'y':
            print("❌ Merge cancelled!")
            return
        
        # Read master file
        master_file = "MASTER_JUSTICE_FILE_SUPREME.py"
        with open(master_file, 'r') as f:
            master_content = f.read()
        
        # Create backup
        backup_file = f"MASTER_JUSTICE_FILE_SUPREME_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        with open(backup_file, 'w') as f:
            f.write(master_content)
        
        # Find insertion point
        insert_point = master_content.find("]", master_content.find("master_data = ["))
        
        # Format new entries
        new_entries = ""
        for doc in pending_docs:
            new_entries += "    {\n"
            for key, value in doc.items():
                new_entries += f'        "{key}": "{value}",\n'
            new_entries += "    },\n"
        
        # Insert new entries
        updated_content = (
            master_content[:insert_point-1] + 
            ",\n" + new_entries.rstrip(",\n") + "\n" + 
            master_content[insert_point:]
        )
        
        # Write updated master file
        with open(master_file, 'w') as f:
            f.write(updated_content)
        
        # Clear pending file
        os.remove(pending_file)
        
        print(f"✅ Merged {len(pending_docs)} documents into master file!")
        print(f"💾 Backup created: {backup_file}")
        print("🔥 Run the master script to update Excel file!")
    
    def view_pending(self):
        """View all pending documents"""
        pending_file = "quick_add_pending.json"
        
        if not os.path.exists(pending_file):
            print("📋 No pending documents found.")
            return
        
        with open(pending_file, 'r') as f:
            pending_docs = json.load(f)
        
        if not pending_docs:
            print("📋 No pending documents found.")
            return
        
        print(f"📋 PENDING DOCUMENTS ({len(pending_docs)}):")
        print("=" * 50)
        
        for i, doc in enumerate(pending_docs, 1):
            print(f"\n{i}. {doc['Filename']}")
            print(f"   Date: {doc['Date']}")
            print(f"   Type: {doc['Type']}")
            print(f"   Pattern: {doc['Pattern']}")
            print(f"   Summary: {doc['Summary'][:100]}...")
            print(f"   Smoking Gun: {doc['Smoking Gun']}")

def main():
    """Interactive Quick Update Tool"""
    updater = QuickUpdate()
    
    print("⚡ JUSTICE FILE QUICK UPDATE TOOL ⚡")
    print("🔥 Fast track for adding new evidence 🔥\n")
    
    while True:
        print("\nChoose an option:")
        print("1. Quick add new document")
        print("2. View pending documents")
        print("3. Merge pending to master file")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            document = updater.quick_add_document()
            if document:
                updater.save_quick_add(document)
        
        elif choice == "2":
            updater.view_pending()
        
        elif choice == "3":
            updater.merge_pending_documents()
        
        elif choice == "4":
            print("🙏 Justice never sleeps. God bless your work!")
            break
        
        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
