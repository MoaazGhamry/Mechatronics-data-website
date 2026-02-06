import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mechatronics_hub.settings')
django.setup()

from hub.models import StudentProfile, Subject

def populate_registrations():
    print("Starting course registration population...")
    profiles = StudentProfile.objects.filter(level__isnull=False)
    
    total_added = 0
    for profile in profiles:
        subjects = Subject.objects.filter(level=profile.level)
        for subject in subjects:
            if not profile.registered_subjects.filter(id=subject.id).exists():
                profile.registered_subjects.add(subject)
                total_added += 1
        print(f"Populated {subjects.count()} subjects for student: {profile.user.username}")
    
    print(f"Population finished. Total registration entries added: {total_added}")

if __name__ == '__main__':
    populate_registrations()
