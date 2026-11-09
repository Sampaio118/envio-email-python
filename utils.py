import datetime
import time


def registrar_log(destinatario, status):
    """Função auxiliar que registra cada tentativa de envio de e-mail

    em um arquivo de texto de log, salvando a data, a hora e o status.
    """
    data_hora_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    linha_log = (
        f"[{data_hora_atual}] - Destinatário: {destinatario} | Status: {status}\n"
    )

    # Salva no arquivo historico.txt de forma segura
    with open("historico.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(linha_log)

    print(f"[LOG SALVO] {linha_log.strip()}")


# ==========================================
#      -----SUA LISTA REAL DE CLIENTES-----
# ==========================================

EMAILS_CADASTRADOS = [
    "cliente1@seuemail.com",
    "cliente2@seuemail.com",
    "cliente3@seuemail.com",
    "cliente4@seuemail.com",
    "cliente5@seuemail.com",
    "cliente6@seuemail.com",
]


def disparar_email_simulado(destinatario):
    """Substitua esta lógica pelo envio real via smtplib / API de e-mail."""
    # Simulação de sucesso
    return True


def enviar_em_lotes(
    lista_emails, tamanho_lote=2, tempo_espera_segundos=5
):
    """Processa a lista de e-mails em blocos/lotes menores.

    :param lista_emails: Lista completa de destinatários :param tamanho_lote:
    Quantidade de e-mails enviados por bloco :param tempo_espera_segundos: Pausa
    em segundos entre cada lote
    """
    total_emails = len(lista_emails)
    print(
        f"--- Iniciando envio total de {total_emails} e-mails (Lotes de {tamanho_lote}) ---\n"
    )

    # Percorre a lista em saltos do tamanho do lote
    for i in range(0, total_emails, tamanho_lote):
        lote_atual = lista_emails[i : i + tamanho_lote]
        numero_lote = (i // tamanho_lote) + 1

        print(
            f"\n--- Processando Lote #{numero_lote} ({len(lote_atual)} destinatários) ---"
        )

        for email in lote_atual:
            sucesso = disparar_email_simulado(email)

            if sucesso:
                registrar_log(email, "SUCESSO")
            else:
                registrar_log(email, "FALHA")

        # Se ainda houver mais e-mails para enviar, faz a pausa técnica
        if i + tamanho_lote < total_emails:
            print(
                f"Aguardando {tempo_espera_segundos} segundos antes do próximo lote..."
            )
            time.sleep(tempo_espera_segundos)

    print("\n--- Processamento de todos os lotes finalizado com sucesso! ---")


# Execução do envio
if __name__ == "__main__":
    # Configuração dos parâmetros de batching
    TAMANHO_DO_LOTE = 2  # Quantos e-mails saem por vez
    INTERVALO_SEGUNDOS = 3  # Tempo de espera entre os blocos

    enviar_em_lotes(
        EMAILS_CADASTRADOS,
        tamanho_lote=TAMANHO_DO_LOTE,
        tempo_espera_segundos=INTERVALO_SEGUNDOS,
    )