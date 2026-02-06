import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mechatronics_hub.settings')
django.setup()

from hub.models import Level, Subject

# Expected subjects for verification
expected_subjects = {
    "100": {
        1: ["C++", "Circuit Theory", "Engineering Materials", "Machine Mechanics", "Math 3", "Thermodynamics"],
        2: ["Electrical Systems", "Human Resources", "Introduction to Law", "Introduction to Mechatronics", 
            "Machine Drawing", "Numerical Techniques", "Stress Analysis"]
    },
    "200": {
        1: ["Electronics", "Fluid Mechanics", "Machine Theory", "Manufacturing Processes", 
            "Project Management", "Seminar", "Statistics"]
    }
}

print("=== Verifying Subjects in Database ===\n")

for level_id, semesters in expected_subjects.items():
    level_obj = Level.objects.filter(level_id=level_id).first()
    if not level_obj:
        print(f"❌ Level {level_id} NOT FOUND in DB")
        continue
    
    print(f"✓ Level {level_id}: {level_obj.title}")
    
    for sem, subject_names in semesters.items():
        print(f"\n  Semester {sem}:")
        for subj_name in subject_names:
            exists = Subject.objects.filter(level=level_obj, name=subj_name, semester=sem).exists()
            if exists:
                print(f"    ✓ {subj_name}")
            else:
                print(f"    ❌ {subj_name} - NOT FOUND")
                # Try to find similar
                all_subjects = Subject.objects.filter(level=level_obj, semester=sem)
                if all_subjects:
                    print(f"       Available: {[s.name for s in all_subjects]}")

print("\n=== All Subjects in DB ===")
for s in Subject.objects.filter(level__level_id__in=["100", "200"]).order_by('level__level_id', 'semester', 'name'):
    print(f"Level {s.level.level_id}, Sem {s.semester}: {s.name}")
