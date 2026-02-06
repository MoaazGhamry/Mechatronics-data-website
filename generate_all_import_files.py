import os
import django
import shutil

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mechatronics_hub.settings')
django.setup()

from hub.models import Subject

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
    subjects = Subject.objects.all().order_by('level__level_id', 'name')
    print(f"Found {subjects.count()} subjects.")
    
    for subject in subjects:
        # Sanitize filename
        safe_name = "".join([c if c.isalnum() or c in (' ', '-', '_') else '' for c in subject.name]).strip()
        safe_name = safe_name.replace(' ', '_')
        
        filename = f"{safe_name}.txt"
        file_path = os.path.join(BASE_DIR, filename)
        
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(TEMPLATE.format(subject_name=subject.name))
            print(f"Created {filename}")
        else:
            print(f"Skipped {filename} (already exists)")

    print(f"\nAll files are ready in '{BASE_DIR}/'.")

if __name__ == "__main__":
    generate_files()
