import os
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


class GoogleDriveService:
    def __init__(self):
        self._SCOPES=['https://www.googleapis.com/auth/drive']

    def build(self):
        creds = ServiceAccountCredentials.from_json_keyfile_name(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"), self._SCOPES[0])
        service = build('drive', 'v3', credentials=creds)

        return service