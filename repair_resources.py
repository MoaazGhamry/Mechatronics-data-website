import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mechatronics_hub.settings')
django.setup()

from hub.models import SubjectResource

broken_file = 'broken_resources.txt'
if not os.path.exists(broken_file):
    print(f"{broken_file} not found.")
    exit(1)

with open(broken_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

repaired_count = 0
not_found_count = 0

print(f"Attempting to repair {len(lines)} resources...")

for line in lines:
    if not line.strip():
        continue
    parts = line.strip().split('|')
    pk = int(parts[0])
    old_path = parts[1]
    
    filename = os.path.basename(old_path)
    found_path = None
    
    # Search for the file under media/resources
    resources_root = os.path.join(settings.MEDIA_ROOT, 'resources')
    for root, dirs, files in os.walk(resources_root):
        if filename in files:
            found_path = os.path.join(root, filename)
            break
            
    if found_path:
        # Standardize path for DB
        rel_path = os.path.relpath(found_path, settings.MEDIA_ROOT)
        rel_path = rel_path.replace('\\', '/')
        
        try:
            res = SubjectResource.objects.get(pk=pk)
            res.file = rel_path
            res.save()
            print(f"FIXED {pk}: {filename} -> {rel_path}")
            repaired_count += 1
        except SubjectResource.DoesNotExist:
            print(f"ERROR {pk}: Resource not found in DB anymore.")
    else:
        print(f"NOT FOUND: {filename}")
        not_found_count += 1

print(f"\nRepair complete. Repaired: {repaired_count}, Still broken: {not_found_count}")
