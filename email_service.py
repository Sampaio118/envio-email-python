
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# Carrega as variáveis do arquivo .env


class DisparadorEmail:

    def __init__(self, host, port, user, password):
        self.smtp_host = host
        self.smtp_port = port
        # Ele sempre vai pegar o remetente que estiver ativo no .env
        self.smtp_user = user
        self.smtp_pass = password

    def enviar_para_lista(self, lista_destinatarios, assunto, corpo_email):
        """Envia a mesma mensagem para uma lista usando o remetente ativo no .env"""
        try:
            print(f"Conectando ao servidor SMTP com o remetente: {self.smtp_user}")
            servidor = smtplib.SMTP(self.smtp_host, self.smtp_port)
            servidor.starttls()
            servidor.login(self.smtp_user, self.smtp_pass)

            print(f"Iniciando disparos para {len(lista_destinatarios)} destinatários...")

            for destinatario in lista_destinatarios:
                msg = MIMEMultipart()
                msg["From"] = self.smtp_user
                msg["To"] = destinatario
                msg["Subject"] = assunto

                msg.attach(MIMEText(corpo_email, "plain"))

                servidor.sendmail(msg["From"], msg["To"], msg.as_string())
                print(f"-> E-mail enviado com sucesso para: {destinatario}")

            servidor.quit()
            print("Disparos finalizados com sucesso!")

        except Exception as erro:
            print(f"Ocorreu um erro no envio: {erro}")