from email.mime.multipart import MIMEMultipart  # formata o texto, cabeçalho( From, To, Subject)
from email.mime.text import MIMEText            # e Corpo do e-mail no padrão exigido pela internet.
import smtplib       # É a biblioteca que conversa com o servidor de Email(envia os pacotes pela rede).

# Configuração do servidor STMP do Ethereal
smtp_host = "smtp.ethereal.email"
smtp_port = 587
smtp_user = "brandyn77@ethereal.email"
smtp_pass = "vXqSXWV8u21fkHhez9"

# Construção da MSG

msg = MIMEMultipart()
msg["From"] = smtp_user
msg["To"] = "destinatario_teste@empresa.com" #Email de destino(fictício até a conclusão do codigo)
msg["Subject"] = "Teste de Envio Automático"

corpo_email = """
Olá!

Este E-mail é apenas um teste em python.
Se voce está lendo essa msg na cx de entrada do Ethereal, o envio funcionou perfeitamente!

Atenciosamente,
Lucas Sampaio
"""
msg.attach(MIMEText(corpo_email, "plain"))

# Conexão de Envio
try:

    print("Conectando ao servidor SMTP...") #Garante que a comunicação com a porta 587 seja criptografada e segura.
    servidor = smtplib.SMTP(smtp_host, smtp_port)
    servidor.starttls() # Ativa a segurança / criptografia

    print("Autenticando Usuario...") 
    servidor.login(smtp_user, smtp_pass)
   
    print("Enviando e-mail...")
    servidor.sendmail(msg["From"], msg["To"], msg.as_string())

    servidor.quit() # ENCERRAR A CONEXÃO COM O SERVIDOR
    print("E-mail enviado com sucesso!")

except Exception as erro:
    print(f"Ocorreu um erro no envio: {erro}")