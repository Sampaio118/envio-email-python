import os
import requests
from dotenv import load_dotenv
from email_service import DisparadorEmail

# Carrega as configurações de ambiente
load_dotenv()

def disparar_para_base_clientes():
    print(">>> Iniciando rotina de disparo para clientes...")
    
    # Busca o endereço da API guardado de forma segura no .env
    endpoint_clientes = os.getenv("API_JSONPLACEHOLDER_URL")
    
    try:
        requisicao = requests.get(endpoint_clientes)
        
        if requisicao.status_code == 200:
            clientes = requisicao.json()
            print(f">>> Total de clientes encontrados: {len(clientes)}")
            
            # Lista para acumular os e-mails que receberão o informe
            destinatarios = []
            
            for cliente in clientes:
                nome_cliente = cliente.get('name')
                email_cliente = cliente.get('email')
                
                destinatarios.append(email_cliente)
                print(f"    - Alvo mapeado: {nome_cliente} ({email_cliente})")
            
            # Configurações da mensagem de envio
                assunto_msg = "Informativo Oficial: Novidades e Atualizações"
                corpo_msg = "Olá! Esta é uma mensagem automática enviada pelo nosso sistema integrado."
            
            # Disparando usando a sua classe oficial
            servico_email = DisparadorEmail(
                host=os.getenv("SMTP_HOST"),
                port=int(os.getenv("SMTP_PORT", 587)),
                user=os.getenv("SMTP_USER"),
                password=os.getenv("SMTP_PASS")
            )
            
            # Executa o envio em lote
            servico_email.enviar_para_lista(destinatarios, assunto_msg, corpo_msg)
            print(">>> Rotina finalizada com sucesso!")
            
        else:
            print(f"❌ Falha ao consultar a API. Código: {requisicao.status_code}")
            
    except Exception as erro:
        print(f"❌ Erro crítico na execução: {erro}")

if __name__ == "__main__":
    disparar_para_base_clientes()