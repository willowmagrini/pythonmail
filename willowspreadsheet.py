import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

def get_drive_client():
    scope_spreadsheet = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials-spreadsheet.json', scope_spreadsheet)
    client = gspread.authorize(creds)
    return client

def get_sheet(client, name):
    sheet = client.open(name)
    sheet_instance = sheet.get_worksheet(0)
    return sheet_instance

def get_clients(client):
    sheet_instance = get_sheet(client, 'Clientes hospedagem')
    records_data = sheet_instance.get_all_records()
    return records_data

def filter_active_clients(clients):
    filtered_data = [item for item in clients if item['Status'] == 1]
    return filtered_data

def get_client_email(client):
    return client['email']

def get_clients_emails(clients):
    emails = []
    for client in clients:
        emails.append(client['email'])
    return emails
