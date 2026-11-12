# email_service.py (ou disparador.py)
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class DisparadorEmail:
    def __init__(self, host=None, port=None, user=None, password=None):
        self.smtp_host = host or os.getenv("SMTP_SERVER", "smtp.ethereal.email")
        self.smtp_port = port or int(os.getenv("SMTP_PORT", 587))
        self.smtp_user = user or os.getenv("EMAIL_USER")
        self.smtp_pass = password or os.getenv("EMAIL_PASS")

    def enviar_mensagem(self, destinatario, assunto, corpo=""):
        """Executa puramente a conexão SMTP e o envio da mensagem."""
        if not self.smtp_user or not self.smtp_pass:
            raise Exception("Credenciais de e-mail não configuradas no ambiente ou arquivo .env")

        msg = MIMEMultipart()
        msg["From"] = self.smtp_user
        msg["To"] = destinatario
        msg["Subject"] = assunto
        msg.attach(MIMEText(corpo, "plain"))

        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            server.starttls()
            server.login(self.smtp_user, self.smtp_pass)
            server.sendmail(self.smtp_user, destinatario, msg.as_string())
            
        return True
        """Método que recebe destinatario, assunto e o corpo da mensagem"""
        try:
            print(f"Conectando ao servidor SMTP com o remetente: {self.smtp_user}")
            
            # Criando a estrutura da mensagem
            msg = MIMEMultipart()
            msg['From'] = self.smtp_user
            msg['To'] = destinatario if isinstance(destinatario, str) else ", ".join(destinatario)
            msg['Subject'] = assunto
            
            msg.attach(MIMEText(corpo, 'plain'))

            # Conectando e enviando
            servidor = smtplib.SMTP(self.smtp_host, self.smtp_port)
            servidor.starttls()
            servidor.login(self.smtp_user, self.smtp_pass)
            
            # Se for lista ou único
            destinatarios = [destinatario] if isinstance(destinatario, str) else destinatario
            servidor.sendmail(self.smtp_user, destinatarios, msg.as_string())
            servidor.quit()
            
            print("E-mail enviado com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")
            raise e