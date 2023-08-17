from __future__ import print_function
import base64
import os.path
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

class WillowGmailClient:
    def __init__(self):
        self.service = self.get_gmail_service()
        
    def get_gmail_service(self):
        SCOPES = ['https://mail.google.com/']
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        service = build('gmail', 'v1', credentials=creds)
        return service

    def create_message(self, sender, to, subject, message_text):
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

    def send_message(self, user_id, message):
        try:
            message = (self.service.users().messages().send(userId=user_id, body=message).execute())
            print('Message Id: %s' % message['id'])
            return message
        except Exception as error:
            print(error)

    def get_messages_from_subject(self, user_id, subject):
        query = f'subject:"{subject}"'
        results = self.service.users().messages().list(userId=user_id, q=query).execute()
        messages = results.get('messages', [])
        return messages
