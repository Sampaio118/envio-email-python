from email_service import DisparadorEmail

def main():
    print("🚀 Iniciando pipeline de disparo de e-mails...")
    
    # Instancia o serviço
    disparador = DisparadorEmail()

    # Lista oficial de destinatários
    lista_emails = [
        "cliente1_teste@empresa.com",
        "cliente2_teste@empresa.com",
        "gerencia_teste@empresa.com"
    ]

    assunto = "Alinhamento Estratégico - Reunião Geral"
    corpo = """Olá, equipe!

Este é o envio oficial automatizado via pipeline estruturado.
Atenciosamente,
Lucas Sampaio
"""

    # Executa a função da classe
    disparador.enviar_em_lote(
        lista_destinatarios=lista_emails,
        assunto=assunto,
        corpo_email=corpo
    )

if __name__ == "__main__":
    main()