# api_cli/index.py
import sys
import os

# Adiciona a raiz do projeto ao path para conseguir importar os módulos principais
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse
from utils import enviar_em_lotes, EMAILS_CADASTRADOS

def main():
    parser = argparse.ArgumentParser(
        description="Sistema Modular de Disparo de E-mails em Lotes - CLI"
    )
    
    parser.add_argument(
        "--enviar", 
        action="store_true", 
        help="Inicia o processo de disparo de e-mails em lotes em segundo plano."
    )
    
    parser.add_argument(
        "--lote", 
        type=int, 
        default=2, 
        help="Define a quantidade de e-mails por lote (padrão: 2)."
    )

    # Lê os argumentos passados no terminal
    args = parser.parse_args()

    # Se o usuário mandou o argumento --enviar, executa os lotes
    if args.enviar:
        print("Iniciando disparos através da CLI...")
        enviar_em_lotes(EMAILS_CADASTRADOS, tamanho_lote=args.lote)
    else:
        # Se nenhum argumento de ação foi passado, mostra o help automaticamente
        parser.print_help()

if __name__ == "__main__":
    main()