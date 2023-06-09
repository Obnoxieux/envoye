from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from envoye.classes.message import *

class API:
    def __init__(self) -> None:
        # If modifying these scopes, delete the file token.json.
        self.scopes = ['https://www.googleapis.com/auth/gmail.modify']

    def get_credentials(self, scopes) -> Credentials:
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds

    def load_and_print_labels(self):
        """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """

        creds = self.get_credentials(scopes=self.scopes)

        try:
            # Call the Gmail API
            service = build('gmail', 'v1', credentials=creds)
            results = service.users().labels().list(userId='me').execute()
            labels = results.get('labels', [])

            if not labels:
                print('No labels found.')
                return
            print('Labels:')
            for label in labels:
                print(f"{label['name']} - ID {label['id']} of type {label['type']}")

        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f'An error occurred: {error}')

    def load_labels(self) -> any:
        creds = self.get_credentials(scopes=self.scopes)

        try:
            service = build('gmail', 'v1', credentials=creds)
            results = service.users().labels().list(userId='me').execute()
            labels = results.get('labels', [])

            if not labels:
                print('No labels found.')
                return
            else:
                return labels

        except HttpError as error:
            print(f'An error occurred: {error}')

    def load_messages_for_label(self, labelIds) -> list[Message]:
        creds = self.get_credentials(scopes=self.scopes)
    
        try:
            service = build('gmail', 'v1', credentials=creds)
            results = service.users().messages().list(userId='me', labelIds=labelIds).execute()
            message_responses = results.get('messages', [])
            messages = []

            if not message_responses:
                print('No messages found.')
                return
            else:
                for response in message_responses:
                    messages.append(self.get_single_message(id=response['id'], service=service))

                return messages

        except HttpError as error:
            print(f'An error occurred: {error}')

    
    def get_single_message(self, id, service) -> Message:
        """
        Retrieves data for single message. Needed because messages().list() only yields id and threadId.
        """
        try:
            result = service.users().messages().get(userId='me', id=id, format='full').execute()
            #print(result)
            payload = result.get('payload')
            #print(payload)
            message_headers  = payload['headers']
            headers = []
            for header in message_headers:
                headers.append(header)

            print(message_headers[1])
            payload = Payload(headers=headers)
            snippet = result.get('snippet')
            thread_id = result.get('thread_id')
            # TODO: do label ids
            return Message(id, [], payload, snippet, thread_id)

        except HttpError as error:
            print(f'An error occurred: {error}')