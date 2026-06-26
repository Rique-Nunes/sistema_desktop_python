"""
config.py
---------
Constantes globais do sistema: caminho do banco, paleta de cores e
listas de dominio (status de pedido e formas de pagamento).
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(BASE_DIR, "zabeths.db")

COR_FUNDO = "#FFF5F7"
COR_PRIMARIA = "#C2185B"
COR_TEXTO = "#3A2A2F"

STATUS_PEDIDO = [
    "Aguardando Pagamento",
    "Em Preparo",
    "Enviado",
    "Entregue",
    "Cancelado",
]
FORMAS_PAGAMENTO = ["PIX", "Credito", "Debito"]
