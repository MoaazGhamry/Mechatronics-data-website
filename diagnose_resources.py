import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mechatronics_hub.settings')
django.setup()

from hub.models import SubjectResource

total = SubjectResource.objects.count()
broken = []

print(f"Checking {total} resources...")

for r in SubjectResource.objects.all():
    file_path = os.path.join(settings.MEDIA_ROOT, r.file.name)
    if not os.path.exists(file_path):
        broken.append((r.pk, r.file.name, r.subject.name))

print(f"Found {len(broken)} broken resources.")

with open('broken_resources.txt', 'w', encoding='utf-8') as f:
    for pk, path, subject in broken:
        f.write(f"{pk}|{path}|{subject}\n")

if broken:
    print("Broken resources saved to broken_resources.txt")
