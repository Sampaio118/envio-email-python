import os
import requests
import threading
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS  # Importa o CORS
from dotenv import load_dotenv
from utils import registrar_log

# Carrega as variáveis do arquivo .env
load_dotenv()

# 1. Inicializa o aplicativo web Flask
app = Flask(__name__)

# 2. Ativa o CORS no aplicativo Flask para aceitar requisições do frontend
CORS(app)

# Importa a sua classe de envio de e-mail
from email_service import DisparadorEmail


# Rota principal: Renderiza automaticamente o seu index.html ao abrir o navegador
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


# Rota de teste para verificar conexão
@app.route("/teste", methods=["GET"])
def teste_conexao():
    return "O Python está conectado e funcionando perfeitamente!"


# Rota HTTP POST: Recebe os dados enviados pelo botão do site
@app.route("/enviar-email", methods=["POST"])
def api_enviar_email():
    try:
        dados = request.json
        destinatario = dados.get("destinatario")
        assunto = dados.get("assunto")
        mensagem = dados.get("mensagem")

        if not destinatario or not assunto or not mensagem:
            return jsonify({
                "status": "erro",
                "mensagem": "Preencha todos os campos obrigatórios!",
            }), 400

        # Instancia a classe exigindo os dados do .env

        disparador = DisparadorEmail(
            host=os.getenv("SMTP_HOST"),
            port=int(os.getenv("SMTP_PORT", 587)),
            user=os.getenv("SMTP_USER"),
            password=os.getenv("SMTP_PASS"),
        )

        # Executa o disparo do e-mail (descomente quando quiser enviar de verdade)
        disparador.enviar_mensagem(destinatario=destinatario, assunto=assunto, corpo=mensagem)

        print(f"E-mail disparado com sucesso para: {destinatario}")

        return jsonify({
            "status": "sucesso",
            "mensagem": f"E-mail enviado com sucesso para {destinatario}!",
        }), 200

    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

@app.route("/enviar-email-lote", methods=["POST"])
def api_enviar_email_lote():
    try:
        dados = request.json
        emails = dados.get("emails")
        assunto = dados.get("assunto")
        mensagem = dados.get("mensagem")

        if not emails or not assunto or not mensagem:
            return jsonify({
                "status": "erro",
                "mensagem": "Preencha todos os campos obrigatórios!",
            }), 400

        # Instancia a classe exigindo os dados do .env
        disparador = DisparadorEmail(
            host=os.getenv("SMTP_HOST"),
            port=int(os.getenv("SMTP_PORT", 587)),
            user=os.getenv("SMTP_USER"),
            password=os.getenv("SMTP_PASS"),
        )

        # Executa o disparo do e-mail (descomente quando quiser enviar de verdade)
        for email in emails:
            disparador.enviar_mensagem(destinatario=email, assunto=assunto, corpo=mensagem)

        print(f"E-mails disparados com sucesso para: {', '.join(emails)}")

        return jsonify({
            "status": "sucesso",
            "mensagem": f"E-mails enviados com sucesso para {', '.join(emails)}!",
        }), 200

    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500


# Rota para o botão de automação via API do seu frontend
@app.route("/disparar-clientes-api", methods=["POST"])
def disparar_clientes_api():
    try:
        print("Buscando clientes na API e iniciando disparos em lote...")
        
        # 1. Pega a URL da API diretamente do .env (sem hardcode!)
        url_api = os.getenv("API_JSONPLACEHOLDER_URL")
        if not url_api:
            return jsonify({"status": "erro", "mensagem": "API_JSONPLACEHOLDER_URL não configurada no .env"}), 500

        resposta = requests.get(url_api)
        if resposta.status_code != 200:
            return jsonify({"status": "erro", "mensagem": "Falha ao conectar com a API externa de clientes."}), 500

        clientes = resposta.json()
    #  ADIÇÃO CIRÚRGICA: Registra no log que a API foi consultada com sucesso
        registrar_log("API Externa (Lote)", f"Sucesso - {len(clientes)} clientes carregados")

        # 2. Instancia o disparador usando as credenciais do .env
        disparador = DisparadorEmail(
            host=os.getenv("SMTP_HOST"),
            port=int(os.getenv("SMTP_PORT", 587)),
            user=os.getenv("SMTP_USER"),
            password=os.getenv("SMTP_PASS"),
        )

        contador = 0
        # 3. Percorre a lista obtida e dispara para cada cliente
        for cliente in clientes[:5]:  # Limitado aos 5 primeiros para teste seguro
            nome = cliente.get('name')
            email = cliente.get('email')
            assunto = "Atualização de Processos - Quality Parts"
            corpo = f"Olá {nome}, informamos que novos dados e rotas foram atualizados em nosso sistema."

            # disparador.enviar_mensagem(destinatario=email, assunto=assunto, corpo=corpo)
            print(f"-> E-mail processado para: {email} ({nome})")
            contador += 1

        return jsonify({
            "status": "sucesso",
            "mensagem": f"Automação concluída! {contador} e-mails disparados para os clientes da API."
        }), 200

    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": f"Erro ao processar automação: {str(e)}"
        }), 500


def abrir_navegador():
    # Força a abertura limpa no navegador padrão do Windows
    os.system('start http://127.0.0.1:5000/')


# Ponto de partida para rodar o servidor local
if __name__ == "__main__":
    # Inicia a abertura automática da aba do navegador com 1.5 segundos de atraso
    threading.Timer(1.5, abrir_navegador).start()
    
    print("🚀 Servidor Flask rodando! Abrindo painel web...")
    app.run(debug=True, port=5000)