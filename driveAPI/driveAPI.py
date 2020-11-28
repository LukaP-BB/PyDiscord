from __future__ import print_function
import pickle
import os.path
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import io
import shutil

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

RANKS = {
    "file" : "rangs.json",
    "id" : "1yI6U6pkY-fA1OSvsMKVk_alE52lYYb_UBnmymVi2MUo"
    }
REACTIONS = {
    "file" : "reactions.json", 
    "id" : "1nopFqfCugxT5698FhEBLfE5pIqWS5eSg7Y0vlIVTF00"
    }

def connect():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('driveAPI/token.pickle'):
        with open('driveAPI/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'driveAPI/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('driveAPI/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    return service

def download(loc_file) :
    service = connect()
    # Call the Drive v3 API
    request = service.files().export(fileId=loc_file["id"], mimeType="text/plain")
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

    fh.seek(0)
    with open(loc_file["file"], 'wb') as f:
        shutil.copyfileobj(fh, f)

def upload(loc_file): 
    service = connect()
    with open(loc_file["file"], "r", encoding="utf-8-sig)") as fh :
        media_body = MediaIoBaseUpload(fh, mimetype="text/plain")
        body = {
            "title" : loc_file["file"]
        }
        service.files().update(fileId=loc_file["id"], body=body, media_body=media_body).execute()


if __name__ == '__main__':
    download(RANKS)
