import willowgmail as wg
import willowspreadsheet as ws
import utils

def get_emails():
    sheet_client = ws.WillowGoogleSheetClient()
    clients = sheet_client.get_clients()
    active_clients = sheet_client.filter_active_clients(clients)
    clients_emails = sheet_client.get_clients_emails(active_clients)
    return clients_emails

def send_emails():
    message_text = "Chegou aquele momento mensal de colaborar para nosso servidor não sair do ar!\nPIX: 34510394861\nBruno Antunes Magrini\nQuando fizer a colaboração manda o comprovante na resposta desse email por favor."
    emails = get_emails()
    emails_str = ','.join(emails)
    gmail_client = wg.WillowGmailClient()
    label = gmail_client.get_label_id_by_name("me","Desenvolvimento/hospedagem")   
    message = gmail_client.create_message("me", "brmagrini@gmail.com", emails_str,"Teste de cobrança",message_text )
    gmail_client.send_message(user_id="me",message=message, labels=[label])