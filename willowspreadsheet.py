import gspread
from oauth2client.service_account import ServiceAccountCredentials

class GoogleSheetClient:
    
    def __init__(self):
        self.client = self.get_drive_client()
    
    def get_drive_client(self):
        """
        Autentica usando as credenciais e retorna um cliente autorizado.
        """
        scope_spreadsheet = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        try:
            creds = ServiceAccountCredentials.from_json_keyfile_name('credentials-spreadsheet.json', scope_spreadsheet)
            client = gspread.authorize(creds)
            return client
        except Exception as e:
            print("Erro ao criar cliente: ", e)
            return None
    
    def get_sheet(self, name):
        """
        Abre a planilha pelo nome e retorna a primeira aba da planilha.
        """
        try:
            sheet = self.client.open(name)
            sheet_instance = sheet.get_worksheet(0)
            return sheet_instance
        except Exception as e:
            print("Erro ao acessar a planilha: ", e)
            return None
    
    def get_clients(self):
        """
        Retorna todos os registros da planilha 'Clientes hospedagem'.
        """
        sheet_instance = self.get_sheet('Clientes hospedagem')
        if sheet_instance:
            return sheet_instance.get_all_records()
        else:
            return []
    
    def filter_active_clients(self, clients):
        """
        Filtra os clientes com Status igual a 1.
        """
        return [item for item in clients if item['Status'] == 1]
    
    def get_client_email(self, client):
        """
        Retorna o campo de e-mail de um cliente.
        """
        return client.get('email', '')

    def get_clients_emails(self, clients):
        """
        Retorna uma lista com os e-mails de uma lista de clientes.
        """
        return [client['email'] for client in clients if 'email' in client]


# Exemplo de uso da classe:
if __name__ == '__main__':
    sheet_client = GoogleSheetClient()
    clients_data = sheet_client.get_clients()
    active_clients = sheet_client.filter_active_clients(clients_data)
    clients_emails = sheet_client.get_clients_emails(active_clients)
    print(clients_emails)
