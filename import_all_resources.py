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
    if not url: return None
    match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', url)
    if match: return match.group(1)
    match = re.search(r'id=([a-zA-Z0-9_-]+)', url)
    if match: return match.group(1)
    return None

def import_resources():
    # Updated to look in the new massive folder
    base_dir = "resource_import_files"
    if not os.path.exists(base_dir):
        # Fallback to old one if user puts them there, but better to stick to one
        if os.path.exists("resource_import_000"):
            base_dir = "resource_import_000"
        else:
            print(f"Directory {base_dir} not found.")
            return

    files = [f for f in os.listdir(base_dir) if f.endswith(".txt")]
    print(f"Found {len(files)} files in {base_dir}")

    for filename in files:
        # Revert filename to subject name: Engineering_History.txt -> Engineering History
        # But we need to match it robustly.
        # The generate script replaced spaces with underscores.
        subject_name_search = filename.replace(".txt", "").replace("_", " ")
        
        # Try exact match first
        subject = Subject.objects.filter(name__iexact=subject_name_search).first()
        
        # If not found, try replacing underscores with spaces in DB name?
        # or simplified matching.
        if not subject:
            # Try to find by partial? No, dangerous.
            print(f"Skipping {filename}: Subject '{subject_name_search}' not found.")
            continue

        # Check if file has any content besides headers
        has_content = False
        with open(os.path.join(base_dir, filename), 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip() and not line.startswith("#") and not line.startswith("["):
                    has_content = True
                    break
        
        if not has_content:
            continue

        print(f"Processing {subject.name}...")
        
        current_category = None
        count_added = 0
        
        with open(os.path.join(base_dir, filename), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if line.startswith("[") and line.endswith("]"):
                    section = line[1:-1]
                    current_category = CATEGORY_MAP.get(section)
                    continue

                if current_category:
                    # Parse Line
                    title = ""
                    url = ""
                    
                    if " | " in line:
                        parts = line.split(" | ", 1)
                        title = parts[0].strip()
                        url = parts[1].strip()
                    elif " - " in line:
                        parts = line.split(" - ", 1)
                        title = parts[0].strip()
                        url = parts[1].strip()
                    else:
                        if "http" in line:
                            url = line
                            title = f"{current_category} Resource" 
                        else:
                            continue 

                    drive_id = get_drive_id(url)
                    if drive_id:
                        preview_url = f"https://drive.google.com/file/d/{drive_id}/preview"
                        download_url = f"https://drive.google.com/uc?id={drive_id}&export=download"
                        
                        # Use Name from line if available, else generic
                        # If user pasted just URL, title is "Lecture Resource".
                        # If they pasted "Lecture 1 | URL", title is "Lecture 1".
                    else:
                        preview_url = url
                        download_url = url
                    
                    if not title:
                        title = current_category

                    # Check existence
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
                        print(f"  + Added '{title}'")
                        count_added += 1
                    else:
                        pass # Silent skip
                        
        if count_added == 0:
            print("  (No new resources found)")

if __name__ == "__main__":
    import_resources()
