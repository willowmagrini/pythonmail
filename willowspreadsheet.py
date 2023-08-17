import gspread
from oauth2client.service_account import ServiceAccountCredentials

class WillowGoogleSheetClient:
    """
    A class that provides methods to interact with Google Sheets using the gspread library.
    
    Attributes:
        client: The authorized client for accessing Google Sheets.
    """
    
    def __init__(self):
        """
        Initializes the WillowGoogleSheetClient object and authenticates the client.
        """
        self.client = self.get_drive_client()
    
    def get_drive_client(self):
        """
        Authenticates the client using the credentials and returns an authorized client.
        
        Returns:
            The authorized client for accessing Google Sheets.
        """
        scope_spreadsheet = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        try:
            creds = ServiceAccountCredentials.from_json_keyfile_name('credentials-spreadsheet.json', scope_spreadsheet)
            client = gspread.authorize(creds)
            return client
        except Exception as e:
            print("Error creating client: ", e)
            return None
    
    def get_sheet(self, name):
        """
        Opens the specified sheet by name and returns the first worksheet of the sheet.
        
        Args:
            name: The name of the sheet to open.
        
        Returns:
            The first worksheet of the specified sheet.
        """
        try:
            sheet = self.client.open(name)
            sheet_instance = sheet.get_worksheet(0)
            return sheet_instance
        except Exception as e:
            print("Error accessing sheet: ", e)
            return None
    
    def get_clients(self):
        """
        Returns all the records from the 'Clientes hospedagem' sheet.
        
        Returns:
            A list of dictionaries representing the records from the sheet.
        """
        sheet_instance = self.get_sheet('Clientes hospedagem')
        if sheet_instance:
            return sheet_instance.get_all_records()
        else:
            return []
    
    def filter_active_clients(self, clients):
        """
        Filters the clients with Status equal to 1.
        
        Args:
            clients: A list of clients to filter.
        
        Returns:
            A new list of clients with Status equal to 1.
        """
        return [item for item in clients if item['Status'] == 1]
    
    def get_client_email(self, client):
        """
        Returns the email field of a client.
        
        Args:
            client: A dictionary representing a client.
        
        Returns:
            The email field of the client. If the email field is not present, returns an empty string.
        """
        return client.get('email', '')

    def get_clients_emails(self, clients):
        """
        Returns a list of emails from a list of clients.
        
        Args:
            clients: A list of clients.
        
        Returns:
            A list of emails extracted from the clients' dictionaries.
        """
        return [client['email'] for client in clients if 'email' in client]


# Exemplo de uso da classe:
if __name__ == '__main__':
    sheet_client = GoogleSheetClient()
    clients_data = sheet_client.get_clients()
    active_clients = sheet_client.filter_active_clients(clients_data)
    clients_emails = sheet_client.get_clients_emails(active_clients)
    print(clients_emails)
