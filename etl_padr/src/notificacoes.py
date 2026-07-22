import smtplib
from email.mime.text import MIMEText

def enviar_alerta(assunto, corpo, email_destino):
    """
    FUNÇÃO AUXILIAR: Envia e-mails de alerta sobre a execução do ETL.
    """
    # ALTERE AQUI: Dados do servidor SMTP da empresa (ex: Outlook, Gmail, etc)
    SMTP_SERVER = "smtp.office365.com"
    SMTP_PORT = 587
    SEU_EMAIL = "seu_email@empresa.com"
    SUA_SENHA = "sua_senha_aqui"

    # Prepara a estrutura do e-mail
    msg = MIMEText(corpo)
    msg['Subject'] = assunto
    msg['From'] = SEU_EMAIL
    msg['To'] = email_destino

    try:
        # Conecta no servidor de e-mail de forma segura
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SEU_EMAIL, SUA_SENHA)
        
        # Envia o e-mail
        server.sendmail(SEU_EMAIL, email_destino, msg.as_string())
        server.quit()
        print("📧 Alerta enviado por e-mail!")
    except Exception as e:
        print(f"❌ Não foi possível enviar o e-mail: {e}")