#conexao.py
#Funcoes utilitarias de acesso ao banco SQLite3.

import sqlite3
import hashlib

from src.config import DB_PATH


def conectar():
    #Abre uma conexao com o banco, com chaves estrangeiras ativadas.
    conexao = sqlite3.connect(DB_PATH)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def hash_senha(senha):
    #Gera o hash SHA-256 da senha
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()
