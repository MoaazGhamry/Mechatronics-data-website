import os
import re
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = 'credentials.json'

def get_drive_service():
    """Authenticates and returns the Drive API service."""
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        raise FileNotFoundError(f"Credentials file '{SERVICE_ACCOUNT_FILE}' not found.")
    
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    return service

def extract_folder_id(url):
    """Extracts Folder ID from a Drive URL."""
    # Pattern: /folders/FOLDER_ID or id=FOLDER_ID
    match = re.search(r'/folders/([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    match = re.search(r'id=([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    # If raw ID is passed
    if re.match(r'^[a-zA-Z0-9_-]+$', url):
        return url
    return None

def list_files_in_folder(folder_url):
    """
    Lists all non-folder files in a Google Drive folder.
    Returns a list of dicts: {'id': '...', 'name': '...', 'size': '...'}
    """
    if not folder_url:
        return []

    folder_id = extract_folder_id(folder_url)
    if not folder_id:
        raise ValueError("Invalid Google Drive Folder URL")

    service = get_drive_service()
    
    # Query: inside parent folder ID and NOT a folder (mimeType != folder) and not trashed
    query = f"'{folder_id}' in parents and mimeType != 'application/vnd.google-apps.folder' and trashed = false"
    
    results = service.files().list(
        q=query,
        pageSize=1000,
        fields="nextPageToken, files(id, name, size, mimeType)"
    ).execute()
    
    files = results.get('files', [])
    return files
