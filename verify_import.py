import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mechatronics_hub.settings')
django.setup()

from hub.models import Level, Subject, SubjectResource

print("=" * 70)
print("RESOURCE IMPORT VERIFICATION")
print("=" * 70)

# Count resources by level and subject
levels_to_check = ["000", "100", "200"]

for level_id in levels_to_check:
    level_obj = Level.objects.filter(level_id=level_id).first()
    if not level_obj:
        print(f"\n❌ Level {level_id} NOT FOUND")
        continue
    
    print(f"\n{'='*70}")
    print(f"Level {level_id}: {level_obj.title}")
    print(f"{'='*70}")
    
    subjects = Subject.objects.filter(level=level_obj).order_by('semester', 'name')
    
    if not subjects:
        print("  ⚠️  No subjects found")
        continue
    
    total_resources = 0
    
    for semester in [1, 2]:
        sem_subjects = subjects.filter(semester=semester)
        if not sem_subjects:
            continue
            
        print(f"\n  Semester {semester}:")
        
        for subject in sem_subjects:
            resource_count = SubjectResource.objects.filter(subject=subject).count()
            total_resources += resource_count
            
            if resource_count > 0:
                print(f"    ✓ {subject.name}: {resource_count} resources")
            else:
                print(f"    ○ {subject.name}: 0 resources (empty)")
    
    print(f"\n  TOTAL for Level {level_id}: {total_resources} resources")

# Overall statistics
print(f"\n{'='*70}")
print("OVERALL STATISTICS")
print(f"{'='*70}")

total_all = SubjectResource.objects.count()
level_000_count = SubjectResource.objects.filter(subject__level__level_id="000").count()
level_100_count = SubjectResource.objects.filter(subject__level__level_id="100").count()
level_200_count = SubjectResource.objects.filter(subject__level__level_id="200").count()

print(f"Total Resources: {total_all}")
print(f"  - Level 000: {level_000_count}")
print(f"  - Level 100: {level_100_count}")
print(f"  - Level 200: {level_200_count}")
print(f"{'='*70}")
