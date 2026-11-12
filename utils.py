# utils.py
import datetime
import time
from dotenv import load_dotenv
from email_service import DisparadorEmail
from app import app, db, HistoricoEnvio

# Carrega as variáveis do ambiente
load_dotenv()

def registrar_no_banco_e_log(destinatario, status):
    data_hora_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # 1. Salva no arquivo de texto de segurança (historico.txt)
    linha_log = f"[{data_hora_atual}] - Destinatário: {destinatario} | Status: {status}\n"
    with open("historico.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(linha_log)

    # 2. Salva oficialmente no Banco de Dados (disparador.db) via SQLAlchemy
    with app.app_context():
        try:
            # Enviando apenas os campos essenciais que o model do app.py espera
            novo_registro = HistoricoEnvio(
                destinatario=destinatario,
                status=status
            )
            db.session.add(novo_registro)
            db.session.commit()
        except Exception as e:
            print(f"[ERRO DE BANCO] Não foi possível salvar no SQLite: {e}")

# Lista de e-mails processada em off
EMAILS_CADASTRADOS = [
    "cliente1@seuemail.com",
    "cliente2@seuemail.com",
    "cliente3@seuemail.com",
    "cliente4@seuemail.com",
    "cliente5@seuemail.com",
    "cliente6@seuemail.com",
]

def enviar_em_lotes(lista_emails, tamanho_lote=2, tempo_espera_segundos=5):
    disparador = DisparadorEmail()
    total_emails = len(lista_emails)
    print(f"--- Iniciando disparo em lotes ({total_emails} destinatários na fila) ---\n")

    for i in range(0, total_emails, tamanho_lote):
        lote_atual = lista_emails[i : i + tamanho_lote]
        numero_lote = (i // tamanho_lote) + 1

        print(f"[PROCESSAMENTO] Executando Lote #{numero_lote} ({len(lote_atual)} mensagens em off)...")

        for email in lote_atual:
            try:
                disparador.enviar_mensagem(email, "Assunto do Lote", "Corpo da mensagem em lote.")
                registrar_no_banco_e_log(email, "SUCESSO")
            except Exception as e:
                registrar_no_banco_e_log(email, "FALHA")

        if i + tamanho_lote < total_emails:
            print(f"-> Pausa de {tempo_espera_segundos} segundos antes do próximo lote...\n")
            time.sleep(tempo_espera_segundos)

    print("\n--- Todos os lotes finalizados! O banco de dados foi atualizado. ---")

if __name__ == "__main__":
    TAMANHO_DO_LOTE = 2
    INTERVALO_SEGUNDOS = 3

    enviar_em_lotes(
        EMAILS_CADASTRADOS,
        tamanho_lote=TAMANHO_DO_LOTE,
        tempo_espera_segundos=INTERVALO_SEGUNDOS,
    )