#Operacoes CRUD da entidade Produto.

from src.database.conexao import conectar


def incluir(nome, descricao, preco, id_categoria):
    con = conectar()
    con.execute(
        "INSERT INTO produto (nome, descricao, preco, id_categoria) VALUES (?, ?, ?, ?)",
        (nome, descricao, preco, id_categoria),
    )
    con.commit()
    con.close()


def listar(filtro=""):
    con = conectar()
    dados = con.execute(
        """SELECT p.*, c.nome AS categoria_nome
           FROM produto p
           LEFT JOIN categoria c ON c.id_categoria = p.id_categoria
           WHERE p.nome LIKE ?
           ORDER BY p.nome""",
        (f"%{filtro}%",),
    ).fetchall()
    con.close()
    return dados


def alterar(id_produto, nome, descricao, preco, id_categoria, ativo):
    con = conectar()
    con.execute(
        """UPDATE produto
           SET nome = ?, descricao = ?, preco = ?, id_categoria = ?, ativo = ?
           WHERE id_produto = ?""",
        (nome, descricao, preco, id_categoria, ativo, id_produto),
    )
    con.commit()
    con.close()


def remover(id_produto):
    #Remocao logica: apenas inativa o produto.
    con = conectar()
    con.execute("UPDATE produto SET ativo = 0 WHERE id_produto = ?", (id_produto,))
    con.commit()
    con.close()


def excluir_definitivo(id_produto):
    #Remocao fisica: usar apenas quando o produto nunca foi vendido.
    con = conectar()
    con.execute("DELETE FROM produto WHERE id_produto = ?", (id_produto,))
    con.commit()
    con.close()
