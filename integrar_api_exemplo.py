import requests

def buscar_dados_e_simular_envio():
    print("1. Conectando à API via HTTP para buscar dados...")
    
    # Exemplo: Consultando dados de um CEP (poderia ser uma API de clientes da sua empresa)  

import os
from dotenv import load_dotenv

load_dotenv() # Garante que as variáveis do .env foram carregadas

# ... no lugar da URL fixa, coloque apenas isto:
url = os.getenv("API_JSONPLACEHOLDER_URL") 
# (ou API_CEP_URL, dependendo de qual estiver a usar)
try:
        resposta = requests.get(url)
        
        if resposta.status_code == 200:
            dados = resposta.json()
            
            # Extraindo informações úteis do JSON retornado pela web
            logradouro = dados.get('logradouro')
            bairro = dados.get('bairro')
            cidade = dados.get('localidade')
            uf = dados.get('uf')
            
            print(f"-> Dados obtidos com sucesso da web: {logradouro}, {bairro} - {cidade}/{uf}\n")
            
            # 2. Simulando como isso se encaixaria no seu disparador de e-mails
            print("2. Montando o e-mail personalizado com os dados da API...")
            assunto = f"Aviso de Rota para a região de {cidade}"
            corpo = f"Olá! Informamos que as entregas na região de {bairro} ({logradouro}) foram atualizadas."
            
            print(f"\n[SIMULAÇÃO DE DISPARO]")
            print(f"Assunto: {assunto}")
            print(f"Mensagem: {corpo}")
            print("-> E-mail pronto para ser passado para o seu DisparadorEmail!")
            
        else:
            print(f"Erro na requisição HTTP: {resposta.status_code}")
            
    except Exception as erro:
        print(f"Ocorreu um erro de conexão: {erro}")

if __name__ == "__main__":
    buscar_dados_e_simular_envio()