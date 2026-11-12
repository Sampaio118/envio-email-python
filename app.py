# app.py
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import webbrowser

load_dotenv()

# 1. Configuração do Flask e Banco de Dados (Compatível com ver_banco.py)
app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///disparador.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# 2. Define o Modelo ORM oficial
class HistoricoEnvio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destinatario = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

# Importa o disparador isolado após a criação da base (Sem referenciar o utils)
from email_service import DisparadorEmail
disparador = DisparadorEmail()

# ==========================================
# --- ROTAS DA APLICAÇÃO ---
# ==========================================

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/teste", methods=["GET"])
def teste_conexao():
    return jsonify({"status": "sucesso", "mensagem": "Servidor Python conectado!"}), 200

@app.route("/api/obter-contatos", methods=["GET"])
def api_obter_contatos():
    try:
        contatos_mock = [
            {"nome": "Lucas Sampaio", "email": "lucas.teste1@ethereal.email"},
            {"nome": "Gabrielle Alves", "email": "gabrielle.teste2@ethereal.email"},
            {"nome": "Ana Carolina", "email": "ana.teste3@ethereal.email"},
            {"nome": "Cliente VIP", "email": "cliente4.teste@ethereal.email"},
        ]
        lista_emails_extraidos = [c["email"] for c in contatos_mock]
        return jsonify({"status": "sucesso", "total": len(lista_emails_extraidos), "emails": lista_emails_extraidos}), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

@app.route("/enviar-email", methods=["POST"])
def enviar_email():
    dados = request.get_json()
    destinatario = dados.get("destinatario")
    assunto = dados.get("assunto")
    mensagem_corpo = dados.get("mensagem")

    if not destinatario or not assunto or not mensagem_corpo:
        return jsonify({"mensagem": "Preencha todos os campos obrigatórios!"}), 400

    try:
        disparador.enviar_mensagem(destinatario, assunto, mensagem_corpo)

        # Registra no banco SQLite via ORM
        novo_registro = HistoricoEnvio(destinatario=destinatario, status="Enviado com Sucesso")
        db.session.add(novo_registro)
        db.session.commit()

        return jsonify({"mensagem": f"E-mail enviado com sucesso para {destinatario}!"}), 200

    except Exception as e:
        return jsonify({"mensagem": f"Erro ao enviar e-mail: {str(e)}"}), 500

@app.route("/enviar-lote-manual", methods=["POST"])
def enviar_lote_manual():
    dados = request.get_json()
    destinatarios = dados.get("destinatarios", [])
    assunto = dados.get("assunto")
    mensagem_corpo = dados.get("mensagem")

    if not destinatarios or not assunto or not mensagem_corpo:
        return jsonify({"mensagem": "Dados incompletos para o disparo em lote!"}), 400

    enviados = 0
    try:
        for dest in destinatarios:
            disparador.enviar_mensagem(dest, assunto, mensagem_corpo)

            novo_registro = HistoricoEnvio(destinatario=dest, status="Enviado em Lote com Sucesso")
            db.session.add(novo_registro)
            enviados += 1

        db.session.commit()

        return jsonify({"status": "sucesso", "mensagem": f"Lote disparado para {enviados} destinatários!"}), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

# ==========================================
# --- INICIALIZAÇÃO DO SERVIDOR ---
# ==========================================
if __name__ == "__main__":
    url = "http://127.0.0.1:5000/"
    print(f"Servidor Flask rodando! Abrindo painel em: {url}")
    webbrowser.open(url)
    app.run(debug=True, port=5000)