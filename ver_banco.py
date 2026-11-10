from app import app, db, HistoricoEnvio

# Abre o contexto da aplicação Flask para acessar o banco
with app.app_context():
    # Busca todos os registros do banco ordenados do mais recente para o antigo
    registros = HistoricoEnvio.query.all()

    print("=" * 65)
    print(f"{'ID':<5} | {'DESTINATÁRIO':<30} | {'STATUS':<20}")
    print("=" * 65)

    for reg in registros:
        print(f"{reg.id:<5} | {reg.destinatario:<30} | {reg.status:<20}")

    print("=" * 65)
    print(f"Total de registros salvos: {len(registros)}")