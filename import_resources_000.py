import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mechatronics_hub.settings')
django.setup()

from hub.models import Subject, SubjectResource

# Map sections to DB choices
CATEGORY_MAP = {
    'LECTURES': 'Lectures',
    'SHEETS': 'Sheets',
    'MIDTERM': 'Midterm',
    'FINAL': 'Final',
    'REVISION': 'Revision',
    'EXPLANATION': 'Explanation'
}

def get_drive_id(url):
    """Extracts File ID from Google Drive URL."""
    # pattern for /file/d/ID/view or /uc?id=ID
    match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    match = re.search(r'id=([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    return None

def import_resources():
    base_dir = "resource_import_000"
    if not os.path.exists(base_dir):
        print(f"Directory {base_dir} not found.")
        return

    files = [f for f in os.listdir(base_dir) if f.endswith(".txt")]

    for filename in files:
        subject_name = filename.replace(".txt", "").replace("_", " ")
        file_path = os.path.join(base_dir, filename)
        
        subject = Subject.objects.filter(name__iexact=subject_name).first()
        if not subject:
            print(f"Skipping {filename}: Subject '{subject_name}' not found.")
            continue

        print(f"Processing {subject.name}...")
        
        # Clear existing resources for this subject?
        # User might want to append. But for now, let's just append and check dupes.
        
        current_category = None
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if line.startswith("[") and line.endswith("]"):
                    section = line[1:-1]
                    current_category = CATEGORY_MAP.get(section)
                    continue

                if current_category:
                    # Parse Line: "Name | URL" or "Name - URL"
                    title = ""
                    url = ""
                    
                    if " | " in line:
                        parts = line.split(" | ", 1)
                        title = parts[0].strip()
                        url = parts[1].strip()
                    elif " - " in line:
                        # Be careful if title has hyphen, but usually separator is surrounded by spaces
                        parts = line.split(" - ", 1)
                        title = parts[0].strip()
                        url = parts[1].strip()
                    else:
                        # Assume just URL if valid url, else Name?
                        if "http" in line:
                            url = line
                            title = f"{current_category} Resource" 
                        else:
                            continue # Skip invalid line

                    # Clean URL and Generate Drive Links
                    drive_id = get_drive_id(url)
                    if drive_id:
                        preview_url = f"https://drive.google.com/file/d/{drive_id}/preview"
                        download_url = f"https://drive.google.com/uc?id={drive_id}&export=download"
                    else:
                        # Fallback for non-drive or folder links (though user promised file links)
                        preview_url = url
                        download_url = url
                    
                    if not title:
                        title = current_category

                    # Check for existence
                    exists = SubjectResource.objects.filter(
                        subject=subject,
                        category=current_category,
                        download_url=download_url
                    ).exists()

                    if not exists:
                        SubjectResource.objects.create(
                            subject=subject,
                            category=current_category,
                            title=title,
                            preview_url=preview_url,
                            download_url=download_url
                        )
                        print(f"  + Added '{title}' ({current_category})")
                    else:
                        print(f"  . Skipped duplicate '{title}'")

if __name__ == "__main__":
    import_resources()
