from email_service import DisparadorEmail
import os
from dotenv import load_dotenv

load_dotenv()




if __name__ == "__main__":
    # Sua lista de clientes/destinatários
    clientes = [
        "cliente1@email.com",
        "cliente2@email.com",
        "cliente3@email.com",
        "cliente4@email.com",
        "cliente5@email.com",
        "cliente6@email.com",
        "cliente7@email.com",
        "cliente8@email.com",
        "cliente9@email.com",
    ]

    assunto = "Atualização de Sistema e Rotas"
    corpo = "Olá! Segue o informativo gerado pelo sistema de automação."

    # Instancia o disparador (ele vai ler o .env atual automaticamente)
    disparador = DisparadorEmail(os.getenv("SMTP_HOST"), os.getenv("SMTP_PORT"), os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))

    disparador2 = DisparadorEmail(os.getenv("SMTP_HOST"), os.getenv("SMTP_PORT"), os.getenv("SMTP_USER2"), os.getenv("SMTP_PASS"))
    
    # Executa o disparo para a lista
    disparador.enviar_para_lista(clientes, assunto, corpo)