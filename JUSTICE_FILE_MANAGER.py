"""
JUSTICE FILE MANAGER & VALIDATOR
Tools for maintaining and validating the Master Justice File system
"""

import pandas as pd
import json
import os
from datetime import datetime
from pathlib import Path

class JusticeFileManager:
    def __init__(self, master_file="MASTER_JUSTICE_FILE_SUPREME.py"):
        self.master_file = master_file
        self.data = self.load_current_data()
    
    def load_current_data(self):
        """Load current data from the master Python file"""
        try:
            # Execute the Python file to get the master_data
            namespace = {}
            with open(self.master_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract just the master_data definition
                start = content.find("master_data = [")
                end = content.find("]", start) + 1
                data_def = content[start:end]
                exec(data_def, namespace)
            
            return pd.DataFrame(namespace['master_data'])
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return pd.DataFrame()
    
    def validate_data_integrity(self):
        """Check for data integrity issues"""
        print("🔍 VALIDATING JUSTICE FILE INTEGRITY...")
        
        issues = []
        
        # Check for required fields
        required_fields = ["Filename", "Date", "Type", "Summary", "Smoking Gun"]
        for field in required_fields:
            if field not in self.data.columns:
                issues.append(f"Missing required field: {field}")
        
        # Check for empty critical fields
        for idx, row in self.data.iterrows():
            if pd.isna(row.get('Summary')) or row.get('Summary') == "":
                issues.append(f"Row {idx+1}: Missing summary for {row.get('Filename', 'Unknown')}")
            
            if row.get('Smoking Gun') == "Review Needed":
                issues.append(f"Row {idx+1}: Smoking Gun status needs review for {row.get('Filename', 'Unknown')}")
        
        # Check for duplicate filenames
        duplicates = self.data['Filename'].duplicated()
        if duplicates.any():
            dup_files = self.data[duplicates]['Filename'].tolist()
            issues.append(f"Duplicate filenames found: {dup_files}")
        
        # Report results
        if issues:
            print(f"⚠️  Found {len(issues)} integrity issues:")
            for i, issue in enumerate(issues, 1):
                print(f"   {i}. {issue}")
        else:
            print("✅ All integrity checks passed!")
        
        return issues
    
    def generate_cross_reference_map(self):
        """Generate a cross-reference map of contradictions and links"""
        print("🔗 GENERATING CROSS-REFERENCE MAP...")
        
        cross_refs = {}
        
        for idx, row in self.data.iterrows():
            filename = row['Filename']
            contradicts = str(row.get('Contradicts', ''))
            cross_link = str(row.get('Cross-Link', ''))
            
            # Extract referenced documents
            refs = []
            if contradicts and contradicts != 'nan':
                refs.extend([r.strip() for r in contradicts.split(',')])
            if cross_link and cross_link != 'nan':
                refs.extend([r.strip() for r in cross_link.split(',')])
            
            cross_refs[filename] = {
                'contradicts': contradicts,
                'cross_links': cross_link,
                'references': refs,
                'pattern': row.get('Pattern', ''),
                'smoking_gun': row.get('Smoking Gun', ''),
                'top_5': row.get('Top 5', '')
            }
        
        # Save cross-reference map
        with open('cross_reference_map.json', 'w') as f:
            json.dump(cross_refs, f, indent=2)
        
        print("✅ Cross-reference map saved to: cross_reference_map.json")
        return cross_refs
    
    def export_for_legal_review(self, output_dir="legal_export"):
        """Export organized files for legal review"""
        print("⚖️ PREPARING LEGAL EXPORT PACKAGE...")
        
        # Create export directory
        export_path = Path(output_dir)
        export_path.mkdir(exist_ok=True)
        
        # Export smoking guns
        smoking_guns = self.data[self.data['Smoking Gun'] == 'Yes'].copy()
        smoking_guns.to_excel(export_path / "SMOKING_GUNS_EVIDENCE.xlsx", index=False)
        
        # Export by pattern
        patterns = self.data['Pattern'].unique()
        for pattern in patterns:
            if pd.notna(pattern):
                pattern_data = self.data[self.data['Pattern'] == pattern].copy()
                safe_name = pattern.replace('🟥', 'RED').replace('🟩', 'GREEN').replace('🟦', 'BLUE').replace(' ', '_')
                pattern_data.to_excel(export_path / f"PATTERN_{safe_name}.xlsx", index=False)
        
        # Export Top 5
        top5 = self.data[self.data['Top 5'] == 'Yes'].copy()
        top5.to_excel(export_path / "TOP_5_PRIORITY.xlsx", index=False)
        
        # Export timeline
        timeline = self.data.copy()
        timeline['Date'] = pd.to_datetime(timeline['Date'], errors='coerce')
        timeline = timeline.sort_values('Date')
        timeline.to_excel(export_path / "CHRONOLOGICAL_TIMELINE.xlsx", index=False)
        
        # Create summary report
        summary = self.generate_case_summary()
        with open(export_path / "CASE_SUMMARY_REPORT.txt", 'w') as f:
            f.write(summary)
        
        print(f"✅ Legal export package created in: {export_path}")
        print("📁 Files included:")
        print("   • SMOKING_GUNS_EVIDENCE.xlsx")
        print("   • TOP_5_PRIORITY.xlsx") 
        print("   • CHRONOLOGICAL_TIMELINE.xlsx")
        print("   • CASE_SUMMARY_REPORT.txt")
        print("   • Pattern-specific Excel files")
    
    def generate_case_summary(self):
        """Generate a comprehensive case summary"""
        total_docs = len(self.data)
        smoking_guns = len(self.data[self.data['Smoking Gun'] == 'Yes'])
        misconduct_cases = len(self.data[self.data['Misconduct?'] == 'Yes'])
        top5_count = len(self.data[self.data['Top 5'] == 'Yes'])
        
        summary = f"""
SUPREME MASTER JUSTICE FILE - CASE SUMMARY
Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

CASE STRENGTH OVERVIEW:
======================
Total Documents Analyzed: {total_docs}
Smoking Gun Evidence: {smoking_guns}
Top 5 Priority Items: {top5_count}
Documented Misconduct: {misconduct_cases}

PATTERN ANALYSIS:
================
"""
        
        pattern_counts = self.data['Pattern'].value_counts()
        for pattern, count in pattern_counts.items():
            if pd.notna(pattern):
                summary += f"{pattern}: {count} documents\n"
        
        summary += f"""

AGENCY BREAKDOWN:
================
"""
        agency_counts = self.data['Agency'].value_counts()
        for agency, count in agency_counts.items():
            if pd.notna(agency):
                summary += f"{agency}: {count} documents\n"
        
        summary += f"""

TOP 5 SMOKING GUNS:
==================
"""
        top5_smoking = self.data[(self.data['Top 5'] == 'Yes') & (self.data['Smoking Gun'] == 'Yes')]
        for idx, row in top5_smoking.iterrows():
            summary += f"• {row['Filename']}\n  Summary: {row['Summary']}\n\n"
        
        summary += f"""

LEGAL VIOLATIONS IDENTIFIED:
============================
"""
        violations = self.data[self.data['Law Violated'] != 'N/A']['Law Violated'].unique()
        for violation in violations:
            if pd.notna(violation):
                summary += f"• {violation}\n"
        
        summary += f"""

CASE STATUS: READY FOR JUSTICE
==============================
This comprehensive evidence package demonstrates systematic failures,
misconduct, and violations requiring immediate legal intervention.

Truth will prevail. Justice for Jace and Josh.

"Let justice roll down like waters, and righteousness like an ever-flowing stream." - Amos 5:24
"""
        
        return summary
    
    def backup_system(self):
        """Create a complete backup of the justice file system"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = Path(f"justice_backup_{timestamp}")
        backup_dir.mkdir(exist_ok=True)
        
        # Backup main files
        files_to_backup = [
            "MASTER_JUSTICE_FILE_SUPREME.py",
            "MASTER_JUSTICE_FILE_SUPREME_v1.xlsx",
            "JUSTICE_FILE_IMPORTER.py",
            "JUSTICE_FILE_MANAGER.py"
        ]
        
        for file in files_to_backup:
            if os.path.exists(file):
                import shutil
                shutil.copy2(file, backup_dir / file)
        
        print(f"💾 Complete backup created: {backup_dir}")
        return backup_dir

def main():
    """Interactive Justice File Manager"""
    manager = JusticeFileManager()
    
    print("⚖️ JUSTICE FILE MANAGER & VALIDATOR ⚖️")
    print("🔥 Maintaining truth and integrity in the fight for justice 🔥\n")
    
    while True:
        print("\nChoose an option:")
        print("1. Validate data integrity")
        print("2. Generate cross-reference map")
        print("3. Export for legal review")
        print("4. Generate case summary")
        print("5. Create system backup")
        print("6. Exit")
        
        choice = input("\nEnter choice (1-6): ").strip()
        
        if choice == "1":
            manager.validate_data_integrity()
        
        elif choice == "2":
            manager.generate_cross_reference_map()
        
        elif choice == "3":
            output_dir = input("Export directory (default: legal_export): ").strip()
            if not output_dir:
                output_dir = "legal_export"
            manager.export_for_legal_review(output_dir)
        
        elif choice == "4":
            summary = manager.generate_case_summary()
            print(summary)
            
            save = input("\nSave summary to file? (y/n): ").strip().lower()
            if save == 'y':
                with open('case_summary.txt', 'w') as f:
                    f.write(summary)
                print("✅ Summary saved to case_summary.txt")
        
        elif choice == "5":
            manager.backup_system()
        
        elif choice == "6":
            print("🙏 May God grant justice and protection. Amen.")
            break
        
        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
