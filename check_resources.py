import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mechatronics_hub.settings')
django.setup()

from hub.models import Level, Subject, SubjectResource

level_000 = Level.objects.filter(level_id='000').first()
if not level_000:
    print("Level 000 not found in database.")
else:
    print(f"Found Level: {level_000}")
    subjects = Subject.objects.filter(level=level_000)
    for sub in subjects:
        resources = SubjectResource.objects.filter(subject=sub)
        print(f"Subject: {sub.name} (Semester {sub.semester}) - {resources.count()} resources")
        # for res in resources:
        #     print(f"  - {res.category}: {res.file.name}")
