import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google_calendar():
    creds = None
    token_path = 'token.pickle'
    credentials_path = 'credentials.json'
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(credentials_path):
                raise FileNotFoundError(f"Файл {credentials_path} не найден.")
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=8080)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    return creds

def create_google_calendar_event(event_data: dict):
    creds = authenticate_google_calendar()
    service = build('calendar', 'v3', credentials=creds)
    start_datetime = event_data['start_datetime']
    end_datetime = event_data['end_datetime']
    event = {
        'summary': event_data['title'],
        'description': event_data.get('description', ''),
        'start': {
            'dateTime': start_datetime,
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_datetime,
            'timeZone': 'UTC',
        },
        'attendees': [{'email': email} for email in event_data.get('attendees', [])],
    }
    try:
        event_result = service.events().insert(calendarId='primary', body=event).execute()
        return event_result
    except Exception as e:
        raise RuntimeError(f"Ошибка при создании события: {e}")
