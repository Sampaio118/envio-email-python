import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class DisparadorEmail:

    def __init__(self, host, port, user, password):
        self.smtp_host = host
        self.smtp_port = port
        self.smtp_user = user
        self.smtp_pass = password

    def enviar_mensagem(self, destinatario, assunto, corpo=""):
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