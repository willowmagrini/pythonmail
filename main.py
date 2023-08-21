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
    message_text = "Chegou aquele momento mensal de colaborar para nosso servidor não sair do ar!\nPIX: 34510394861\nBruno Antunes Magrini\nQuando fizer a colaboração manda o comprovante na resposta desse email por favor.\n\nAo efetuar o pagamento por favor responda neste mesmo e-mail com o comprovante.\nValeu!"
    emails = get_emails()
    emails_str = ','.join(emails)
    gmail_client = wg.WillowGmailClient()
    if not gmail_client.email_already_sent_this_month():
        label = gmail_client.get_label_id_by_name("me","Desenvolvimento/hospedagem")
        date = utils.Utils().get_current_month_year()
        subject = f"Colaboração para o servidor [{date}]"
        message = gmail_client.create_message("me", "brmagrini@gmail.com", emails_str,subject,message_text )
        gmail_client.send_message(user_id="me",message=message, labels=[label])