import os
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


class GoogleDriveService:
    def __init__(self):
        self._SCOPES=['https://www.googleapis.com/auth/drive']

    def build(self):
        creds = ServiceAccountCredentials.from_json_keyfile_name("/home/lucaslh/CSCE310_Final_Project/backend/google_drive_credentials.json", self._SCOPES)
        service = build('drive', 'v3', credentials=creds)

        return service