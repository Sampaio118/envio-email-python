import datetime

def registrar_log(destinatario, status):
    """
    Função auxiliar que registra cada tentativa de envio de e-mail 
    em um arquivo de texto de log, salvando a data, a hora e o status.
    """
    data_hora_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    linha_log = f"[{data_hora_atual}] - Destinatário: {destinatario} - Status: {status}\n"
    
    # Salva no arquivo historico.txt de forma segura
    with open("historico.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(linha_log)
    
    print(f"[LOG SALVO] {linha_log.strip()}")