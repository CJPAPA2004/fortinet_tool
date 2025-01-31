from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

def authenticate_google_drive():
    credentials = Credentials.from_service_account_file(
        "client_secret.json",
        scopes=["https://www.googleapis.com/auth/drive.file"]
    )
    return build('drive', 'v3', credentials=credentials)

def upload_file_to_drive(file_data, file_name, mime_type, folder_id):
    service = authenticate_google_drive()
    file_metadata = {"name": file_name, "parents": [folder_id]}
    media = MediaIoBaseUpload(io.BytesIO(file_data), mimetype=mime_type, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    return file.get('id')
