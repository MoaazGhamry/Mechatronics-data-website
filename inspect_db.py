import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mechatronics_hub.settings')
django.setup()

from hub.models import Level, Subject

print("--- Levels ---")
for l in Level.objects.all():
    print(f"ID: '{l.level_id}', Title: '{l.title}'")

print("\n--- Subjects ---")
for s in Subject.objects.all().order_by('level__level_id', 'semester', 'name'):
    print(f"Level: {s.level.level_id}, Sem: {s.semester}, Name: '{s.name}'")
