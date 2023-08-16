import willowgmail as wg
import willowspreadsheet as ws

def get_emails():
    drive_client = ws.get_drive_client()
    clients = ws.get_clients()
    active_clients = ws.filter_active_clients(clients)
    emails = ws.get_clients_emails(active_clients)
    return emails

def send_emails():
    message_text = "Chegou aquele momento mensal de colaborar para nosso servidor não sair do ar!\nPIX: 34510394861\nBruno Antunes Magrini\nQuando fizer a colaboração manda o comprovante na resposta desse email por favor."
    emails = get_emails()
    emails_str = ','.join(emails)
    service = wg.get_gmail_service()
    message = wg.create_message("me", emails_str,"Teste de cobrança",message_text  )
    wg.send_message(service=service,user_id="me",message=message)
