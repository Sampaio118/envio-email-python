from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
import threading
import webbrowser
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

import sys

# ==========================================
# --- SISTEMA DE AJUDA POR LINHA DE COMANDO ---
# ==========================================

if "--help" in sys.argv or "-h" in sys.argv:
    print("==================================================")
    print("     MANUAL DO DISPARADOR DE E-MAILS (FLASK)      ")
    print("==================================================")
    print(" Uso: python app.py [opções]")
    print("")
    print(" Opções disponíveis:")
    print("   --help, -h    Exibe este manual de ajuda e sai.")
    print("")
    print(" Descrição:")
    print("   Inicia a aplicação web Flask conectada ao SQLite")
    print("   via ORM para gerenciar o envio de e-mails individuais")
    print("   e em lote, registrando o histórico de envios.")
    print("==================================================")
    sys.exit(0)
# ==========================================
# --- CONFIGURAÇÃO INICIAL DO APP E BANCO ---
# Projeto: Disparadores de E-mails
# ==========================================

load_dotenv()
load_dotenv()

# --- ADICIONE ESTAS LINHAS PARA TESTAR ---
print("DEBUG EMAIL_USER:", os.getenv("EMAIL_USER"))
print("DEBUG EMAIL_PASS:", os.getenv("EMAIL_PASS"))
# ----------------------------------------

app = Flask(__name__)
CORS(app)

# Configuração do banco SQLite local com SQLAlchemy (ORM)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///disparador.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Configurações do Servidor SMTP (Ethereal)
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.ethereal.email")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")


# ==========================================
# --- MODELO ORM (TABELA NO BANCO) ---
# ==========================================
class HistoricoEnvio(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  destinatario = db.Column(db.String(120), nullable=False)
  status = db.Column(db.String(50), nullable=False)


# Cria o banco e a tabela automaticamente ao iniciar
with app.app_context():
  db.create_all()


def abrir_navegador():
  webbrowser.open("http://127.0.0.1:5000/")


# ==========================================
# --- ROTAS DO SISTEMA ---
# ==========================================


@app.route("/")
def index():
  return render_template("index.html")


@app.route("/teste", methods=["GET"])
def teste_conexao():
  return (
      jsonify({
          "status": "sucesso",
          "mensagem": "Servidor Python conectado com sucesso!",
      }),
      200,
  )


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
    return (
        jsonify({
            "status": "sucesso",
            "total": len(lista_emails_extraidos),
            "emails": lista_emails_extraidos,
        }),
        200,
    )
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
    # 1. Lógica de Envio SMTP
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = destinatario
    msg["Subject"] = assunto
    msg.attach(MIMEText(mensagem_corpo, "plain"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
      server.starttls()
      server.login(EMAIL_USER, EMAIL_PASS)
      server.sendmail(EMAIL_USER, destinatario, msg.as_string())

    # 2. Salvando o registro no banco usando o ORM (Só executa se deu certo!)
    novo_registro = HistoricoEnvio(
        destinatario=destinatario, status="Enviado com Sucesso"
    )
    db.session.add(novo_registro)
    db.session.commit()

    return (
        jsonify({
            "mensagem": f"E-mail enviado com sucesso para {destinatario} e registrado no banco!"
        }),
        200,
    )

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
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
      server.starttls()
      server.login(EMAIL_USER, EMAIL_PASS)

      for dest in destinatarios:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = dest
        msg["Subject"] = assunto
        msg.attach(MIMEText(mensagem_corpo, "plain"))
        server.sendmail(EMAIL_USER, dest, msg.as_string())

        # Registrando cada envio do lote no banco via ORM
        novo_registro = HistoricoEnvio(
            destinatario=dest, status="Enviado em Lote com Sucesso"
        )
        db.session.add(novo_registro)

        enviados += 1

      # Confirma todas as inserções de uma vez no banco
      db.session.commit()

    return (
        jsonify({
            "status": "sucesso",
            "mensagem": f"Lote disparado com sucesso para {enviados} destinatários e salvos no banco!",
        }),
        200,
    )
  except Exception as e:
    return jsonify({"status": "erro", "mensagem": str(e)}), 500


# ==========================================
# --- INICIALIZAÇÃO DO SERVIDOR ---
# ==========================================
if __name__ == "__main__":
  threading.Timer(1.5, abrir_navegador).start()
  print("🚀 Servidor Flask rodando! Abrindo painel web...")
  app.run(debug=True, port=5000)