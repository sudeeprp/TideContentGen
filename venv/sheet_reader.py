import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def get_sheetreader():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret_265657056700-kli99a48p226qvrcovcqusdrjtngck01.apps.googleusercontent.com.json',
                SCOPES)
            creds = flow.run_local_server()
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('sheets', 'v4', credentials=creds)
    return service.spreadsheets()

def read_range(sheetreader, spreadsheet_id, cell_range):
    result = sheetreader.values().get(spreadsheetId=spreadsheet_id,
                                      range=cell_range).execute()
    return result.get('values', [])
