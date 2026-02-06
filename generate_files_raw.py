import os
import sqlite3

BASE_DIR = "resource_import_files"
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

TEMPLATE = """# INSTRUCTIONS:
# Please paste the link for EACH file you want to appear on the site for {subject_name}.
# Format:   Name | URL (or just URL)
# Example:  Lecture 1 | https://drive.google.com/file/d/...

[LECTURES]

[SHEETS]

[MIDTERM]

[FINAL]

[REVISION]

[EXPLANATION]
"""

def generate_files():
    try:
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM hub_subject ORDER BY name')
        subjects = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        print(f"Found {len(subjects)} subjects from DB.")
        
        for name in subjects:
            # Sanitize filename
            safe_name = "".join([c if c.isalnum() or c in (' ', '-', '_') else '' for c in name]).strip()
            safe_name = safe_name.replace(' ', '_')
            
            filename = f"{safe_name}.txt"
            file_path = os.path.join(BASE_DIR, filename)
            
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(TEMPLATE.format(subject_name=name))
                # print(f"Created {filename}") # Reduce junk output
            
        print(f"Successfully created import files in '{BASE_DIR}/'.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_files()
