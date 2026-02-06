import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mechatronics_hub.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin():
    username = 'mohamed khaled'
    password = 'mido1234'
    
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, password=password, email='')
        print(f"Admin user '{username}' created successfully.")
    else:
        print(f"Admin user '{username}' already exists.")

if __name__ == "__main__":
    create_admin()
