#schema.py
#Criacao das tabelas e insercao de dados ficticios de demonstracao.

from src.database.conexao import conectar, hash_senha


def criar_tabelas():
    #Cria todas as tabelas do sistema caso ainda nao existam.
    con = conectar()
    con.executescript(
        """
        CREATE TABLE IF NOT EXISTS categoria (
            id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
            nome         TEXT NOT NULL,
            ativo        INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS cliente (
            id_cliente   INTEGER PRIMARY KEY AUTOINCREMENT,
            nome         TEXT NOT NULL,
            email        TEXT NOT NULL UNIQUE,
            telefone     TEXT NOT NULL,
            senha        TEXT NOT NULL,
            data_criacao TEXT NOT NULL DEFAULT (datetime('now','localtime'))
        );

        CREATE TABLE IF NOT EXISTS produto (
            id_produto   INTEGER PRIMARY KEY AUTOINCREMENT,
            nome         TEXT NOT NULL,
            descricao    TEXT,
            preco        REAL NOT NULL,
            id_categoria INTEGER,
            ativo        INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (id_categoria) REFERENCES categoria (id_categoria)
        );

        CREATE TABLE IF NOT EXISTS pedido (
            id_pedido        INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente       INTEGER NOT NULL,
            data_hora        TEXT NOT NULL DEFAULT (datetime('now','localtime')),
            valor_total      REAL NOT NULL DEFAULT 0,
            status_pedido    TEXT NOT NULL DEFAULT 'Aguardando Pagamento',
            forma_pagamento  TEXT NOT NULL DEFAULT 'PIX',
            endereco_entrega TEXT,
            FOREIGN KEY (id_cliente) REFERENCES cliente (id_cliente)
        );

        CREATE TABLE IF NOT EXISTS item_pedido (
            id_item        INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pedido      INTEGER NOT NULL,
            id_produto     INTEGER NOT NULL,
            quantidade     INTEGER NOT NULL,
            preco_unitario REAL NOT NULL,
            FOREIGN KEY (id_pedido)  REFERENCES pedido (id_pedido) ON DELETE CASCADE,
            FOREIGN KEY (id_produto) REFERENCES produto (id_produto)
        );
        """
    )
    con.commit()
    con.close()


def popular_dados_ficticios():
    #Insere registros de exemplo apenas se o banco estiver vazio.
    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT COUNT(*) FROM categoria")
    if cur.fetchone()[0] > 0:
        con.close()
        return

    categorias = [("Bolos",), ("Brigadeiros",), ("Tortas",), ("Salgados",), ("Bebidas",)]
    cur.executemany("INSERT INTO categoria (nome) VALUES (?)", categorias)

    clientes = [
        ("Ana Silva", "ana.silva@email.com", "(21) 98765-4321", hash_senha("123456")),
        ("Bruno Costa", "bruno.costa@email.com", "(11) 91234-5678", hash_senha("123456")),
        ("Carla Oliveira", "carla.o@email.com", "(31) 95555-4445", hash_senha("123456")),
    ]
    cur.executemany(
        "INSERT INTO cliente (nome, email, telefone, senha) VALUES (?, ?, ?, ?)", clientes
    )

    produtos = [
        ("Bolo de Pote", "Bolo de pote cremoso, varios sabores", 18.00, 1),
        ("Brigadeiro Gourmet", "Caixa com 6 brigadeiros gourmet", 24.00, 2),
        ("Torta de Limao", "Torta de limao fatia individual", 12.50, 3),
        ("Coxinha de Frango", "Coxinha tradicional de frango", 7.00, 4),
        ("Suco de Laranja", "Suco natural 500ml", 9.00, 5),
        ("Brownie de Chocolate", "Brownie com chocolate meio amargo", 8.00, 1),
    ]
    cur.executemany(
        "INSERT INTO produto (nome, descricao, preco, id_categoria) VALUES (?, ?, ?, ?)",
        produtos,
    )

    cur.execute(
        """INSERT INTO pedido (id_cliente, valor_total, status_pedido, forma_pagamento, endereco_entrega)
           VALUES (?, ?, ?, ?, ?)""",
        (1, 0, "Entregue", "PIX", "Rua das Flores, 123 - Rio de Janeiro/RJ"),
    )
    id_pedido = cur.lastrowid
    itens = [(id_pedido, 1, 2, 18.00), (id_pedido, 2, 1, 24.00)]
    cur.executemany(
        "INSERT INTO item_pedido (id_pedido, id_produto, quantidade, preco_unitario) VALUES (?, ?, ?, ?)",
        itens,
    )
    total = sum(q * p for (_, _, q, p) in itens)
    cur.execute("UPDATE pedido SET valor_total = ? WHERE id_pedido = ?", (total, id_pedido))

    con.commit()
    con.close()


def inicializar_banco():
    #Cria as tabelas e popula os dados de exemplo. Chamado no inicio do app.
    criar_tabelas()
    popular_dados_ficticios()
