import os
import django
from hub.drive_service import get_drive_service

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mechatronics_hub.settings')
django.setup()

def text_auth():
    print("Testing Google Drive Authentication...")
    try:
        service = get_drive_service()
        print("SUCCESS: Authentication worked!")
        print("Service object created:", service)
    except Exception as e:
        print("ERROR: Authentication failed.")
        print(e)

if __name__ == "__main__":
    text_auth()
