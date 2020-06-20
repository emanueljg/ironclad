"""Module for getting all events from a Google Calendar.

Uses the Google Api. Almost all of the code taken from https://developers.google.com/calendar/quickstart/python."""


import time
from datetime import datetime, timezone
import pickle
import os.path
from config import load_config
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

cfg = load_config()


def get_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service


def get_events(service):
    # Call the Calendar API
    now = datetime.now(tz=timezone.utc)
    calendars = service.calendarList().list(maxResults=cfg['max_read_calendars'],
                                            showHidden=True).execute()['items']
    all_events = []
    for calendar in calendars:
        events_result = service.events().list(calendarId=calendar['id'],
                                              timeMin=str(now.isoformat()),
                                              maxResults=cfg['max_read_events'],
                                              singleEvents=True,
                                              orderBy='startTime').execute()['items']
        all_events.extend(events_result)

    returned_events = []
    for event in all_events:
        if all(('start' in event,
                'dateTime' in event['start'],
                'description' in event,
                '.ironclad' in event['description'])):
            returned_events.append(event)

    return returned_events


def search_for_rules(events):
    for event in events:
        start = datetime.fromisoformat(event['start']['dateTime'])
        end = datetime.fromisoformat(event['end']['dateTime'])

        if start < datetime.now(tz=timezone.utc) < end:
            rules = event['description'].split('.ironclad\n')[1]
            return rules


def main():
    service = get_service()
    events = get_events(service)
    refreshed_events_at = 0
    while True:
        now = time.time()
        if now - refreshed_events_at > cfg['refresh_events']:
            events = get_events(service)
            refreshed_events_at = now

        rules = search_for_rules(events)

        if rules is not None:
            pass  # TODO insert logic here


