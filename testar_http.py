import os
import requests
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def testar_requisicao_http():
    print("Iniciando requisição HTTP para a API...")
    
    # Pega a URL de forma dinâmica e segura direto do arquivo .env
    url = os.getenv("API_CEP_URL")
    print(f"URL utilizada: {url}")
    
    try:
        resposta = requests.get(url)
        print(f"Status Code da Resposta: {resposta.status_code}")
        
        if resposta.status_code == 200:
            print("Requisição bem-sucedida! Dados recebidos com sucesso:\n")
            
            # Mostra o dicionário/JSON completo recebido da web
            dados_json = resposta.json()
            print(f"Logradouro: {dados_json.get('logradouro')}")
            print(f"Bairro: {dados_json.get('bairro')}")
            print(f"Cidade/UF: {dados_json.get('localidade')}/{dados_json.get('uf')}")
        else:
            print(f"O servidor respondeu, mas com erro. Código: {resposta.status_code}")
            
    except Exception as erro:
        print(f"Ocorreu um erro de conexão: {erro}")

if __name__ == "__main__":
    testar_requisicao_http()