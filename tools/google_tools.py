import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
import base64
from email.message import EmailMessage

class GoogleWorkspaceManager:
    def __init__(self, service_account_file: str = "./service-account.json"):
        self.service_account_file = service_account_file
        self.credentials = None
        if os.path.exists(service_account_file):
            self.credentials = service_account.Credentials.from_service_account_file(
                service_account_file,
                scopes=[
                    'https://www.googleapis.com/auth/gmail.readonly',
                    'https://www.googleapis.com/auth/gmail.send',
                    'https://www.googleapis.com/auth/drive.readonly',
                    'https://www.googleapis.com/auth/documents.readonly'
                ]
            )

    def _ensure_creds(self):
        if not self.credentials:
            raise Exception("Google credentials file 'service-account.json' not found.")

    def list_gmail_messages(self, user_id='me', max_results=5):
        self._ensure_creds()
        # Note: 'me' might not work with service accounts unless delegated.
        # This will work if service account is used for its own identity or delegated.
        service = build('gmail', 'v1', credentials=self.credentials)
        results = service.users().messages().list(userId=user_id, maxResults=max_results).execute()
        return results.get('messages', [])

    def list_drive_files(self, max_results=5):
        self._ensure_creds()
        service = build('drive', 'v3', credentials=self.credentials)
        results = service.files().list(pageSize=max_results, fields="nextPageToken, files(id, name)").execute()
        return results.get('files', [])

    def read_google_doc(self, document_id: str):
        self._ensure_creds()
        service = build('docs', 'v1', credentials=self.credentials)
        doc = service.documents().get(documentId=document_id).execute()
        return doc.get('title', 'Untitled') + "\n" + str(doc.get('body'))
