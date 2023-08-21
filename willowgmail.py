from __future__ import print_function
import base64
import os.path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import utils

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

    def create_message(self, sender, to, bcc,subject, message_text):
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        message['bcc'] = bcc
        return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

    def send_message(self, user_id, message,labels=[]):
        try:
            message = (self.service.users().messages().send(userId=user_id, body=message).execute())
            print('Message Id: %s' % message['id'])
            if labels:
                self.add_label(user_id, message['id'], labels)
            return message
        except Exception as error:
            print(error)

    def get_messages_from_subject(self, user_id, subject):
        query = f'subject:"{subject}"'
        results = self.service.users().messages().list(userId=user_id, q=query).execute()
        messages = results.get('messages', [])
        return messages
    
    
    def list_labels(self, user_id):
        try:
            response = self.service.users().labels().list(userId=user_id).execute()
            labels = response['labels']
            return labels
        except Exception as error:
            print('An error occurred: %s' % error)


    def get_label_id_by_name(self, user_id, label_name):
        labels = self.list_labels(user_id)
        if labels is not None:
            for label in labels:
                if label['name'] == label_name:
                    return label['id']
        return None
    
    def add_label(self, user_id, msg_id, label_ids):
        try:
            message = self.service.users().messages().modify(userId=user_id, id=msg_id,
                                                        body={'addLabelIds': label_ids}).execute()
            print('Label added to Message ID: %s' % message['id'])
        except Exception as error:
            print('An error occurred: %s' % error)

    def get_thread_id(self, message_id):
        """Pega o ID da thread de uma mensagem."""
        message = self.service.users().messages().get(userId='me', id=message_id).execute()
        return message['threadId']

    def get_messages_in_thread(self, thread_id):
        """Pega todas as mensagens em uma thread."""
        thread = self.service.users().threads().get(userId='me', id=thread_id).execute()
        return thread['messages']

    def get_from_address(self, message):
        """Pega o endereço do remetente de uma mensagem."""
        for header in message['payload']['headers']:
            if header['name'] == 'From':
                return header['value']
        return None

    def get_reply_senders(self, sent_message_id):
        """Pega os remetentes de todas as respostas a um e-mail enviado."""
        thread_id = self.get_thread_id(sent_message_id)
        messages_in_thread = self.get_messages_in_thread(thread_id)
        reply_senders = []
        for message in messages_in_thread:
            if message['id'] != sent_message_id:
                from_address = self.get_from_address(message)
                if from_address:
                    reply_senders.append(from_address)
        return reply_senders
    
    def search_messages(self, query):
        """Procura mensagens que correspondem a um critério de pesquisa e retorna os IDs das mensagens."""
        try:
            response = self.service.users().messages().list(userId='me', q=query).execute()
            if 'messages' in response:
                return [msg['id'] for msg in response['messages']]
            else:
                return []
        except Exception as error:
            print('An error occurred: %s' % error)
            return []
    def get_message(self, msg_id):
        try:
            message = self.service.users().messages().get(userId='me', id=msg_id).execute()
            return message
        except Exception as error:
            print('An error occurred: %s' % error)
            return None
    
    def get_replies_message_by_subject(self,subject):
        original_messages = self.search_messages('subject:"'+subject+'"')
        original_message_id = original_messages[0]
        senders = self.get_reply_senders(original_message_id)
        return senders  
    
    def get_messages_with_subject_and_label(self, subject, label_name):
        query = f'subject:"{subject}" label:{label_name}'
        messages = self.search_messages(query)
        return messages
    
    def email_already_sent_this_month(self):
        """
        Verifica se o e-mail já foi enviado neste mês.
        
        Retorna:
        - True se o e-mail já foi enviado.
        - False caso contrário.
        """
        
        # Pega o mês e ano atual usando a função existente em utils
        date = utils.Utils().get_current_month_year()
        
        # Formata o assunto para a busca
        query = f'subject:"Colaboração para o servidor [{date}]"'
        
        # Busca por e-mails que atendam ao critério
        results = self.service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])
        
        # Se houver e-mails que atendam ao critério, isso significa que um e-mail já foi enviado neste mês
        return len(messages) > 0
    

    def get_email_content(self,filename):
        with open(filename, 'r') as file:
            return file.read()