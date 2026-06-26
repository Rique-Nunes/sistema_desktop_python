#Operacoes CRUD da entidade Pedido (e seus itens).

from src.database.conexao import conectar


def incluir(id_cliente, forma_pagamento, status, endereco, itens):
    """
    Inclui um pedido e seus itens.
    itens = lista de tuplas (id_produto, quantidade, preco_unitario).
    O valor_total e calculado automaticamente.
    """
    con = conectar()
    cur = con.cursor()
    total = sum(q * p for (_, q, p) in itens)
    cur.execute(
        """INSERT INTO pedido (id_cliente, valor_total, status_pedido, forma_pagamento, endereco_entrega)
           VALUES (?, ?, ?, ?, ?)""",
        (id_cliente, total, status, forma_pagamento, endereco),
    )
    id_pedido = cur.lastrowid
    for (id_produto, qtd, preco) in itens:
        cur.execute(
            """INSERT INTO item_pedido (id_pedido, id_produto, quantidade, preco_unitario)
               VALUES (?, ?, ?, ?)""",
            (id_pedido, id_produto, qtd, preco),
        )
    con.commit()
    con.close()
    return id_pedido


def listar(filtro=""):
    con = conectar()
    dados = con.execute(
        """SELECT pe.*, c.nome AS cliente_nome
           FROM pedido pe
           JOIN cliente c ON c.id_cliente = pe.id_cliente
           WHERE c.nome LIKE ?
           ORDER BY pe.data_hora DESC""",
        (f"%{filtro}%",),
    ).fetchall()
    con.close()
    return dados


def listar_itens(id_pedido):
    con = conectar()
    dados = con.execute(
        """SELECT i.*, p.nome AS produto_nome
           FROM item_pedido i
           JOIN produto p ON p.id_produto = i.id_produto
           WHERE i.id_pedido = ?""",
        (id_pedido,),
    ).fetchall()
    con.close()
    return dados


def alterar_status(id_pedido, status):
    con = conectar()
    con.execute(
        "UPDATE pedido SET status_pedido = ? WHERE id_pedido = ?", (status, id_pedido)
    )
    con.commit()
    con.close()


def remover(id_pedido):
    con = conectar()
    con.execute("DELETE FROM item_pedido WHERE id_pedido = ?", (id_pedido,))
    con.execute("DELETE FROM pedido WHERE id_pedido = ?", (id_pedido,))
    con.commit()
    con.close()


def obter_por_id(id_pedido):
    con = conectar()
    dado = con.execute(
        """SELECT pe.*, c.nome AS cliente_nome
           FROM pedido pe
           JOIN cliente c ON c.id_cliente = pe.id_cliente
           WHERE pe.id_pedido = ?""",
        (id_pedido,),
    ).fetchone()
    con.close()
    return dado

