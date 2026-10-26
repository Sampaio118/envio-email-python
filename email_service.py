import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

class DisparadorEmail:
    def __init__(self, host=None, port=None, user=None, password=None):
        self.smtp_host = host or os.getenv("SMTP_HOST", "smtp.ethereal.email")
        self.smtp_port = int(port or os.getenv("SMTP_PORT", 587))
        self.smtp_user = user or os.getenv("SMTP_USER")
        self.smtp_pass = password or os.getenv("SMTP_PASS")

    def enviar_em_lote(self, lista_destinatarios, assunto, corpo_email):
        """Dispara e-mails em lote utilizando uma única conexão SMTP."""
        try:
            servidor = smtplib.SMTP(self.smtp_host, self.smtp_port)
            servidor.starttls()
            servidor.login(self.smtp_user, self.smtp_pass)

            for destinatario in lista_destinatarios:
                msg = MIMEMultipart()
                msg["From"] = self.smtp_user
                msg["To"] = destinatario
                msg["Subject"] = assunto
                msg.attach(MIMEText(corpo_email, "plain"))

                servidor.sendmail(msg["From"], msg["To"], msg.as_string())
                print(f" -> 🚀 Enviado com sucesso para: {destinatario}")

            servidor.quit()
            print("\n🎉 Lote de e-mails processado com sucesso!")
        except Exception as erro:
            print(f"❌ Erro no envio: {erro}")
