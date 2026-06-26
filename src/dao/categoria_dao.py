#Operacoes CRUD da entidade Categoria.

from src.database.conexao import conectar


def incluir(nome):
    con = conectar()
    con.execute("INSERT INTO categoria (nome) VALUES (?)", (nome,))
    con.commit()
    con.close()


def listar(filtro=""):
    con = conectar()
    dados = con.execute(
        "SELECT * FROM categoria WHERE nome LIKE ? ORDER BY nome",
        (f"%{filtro}%",),
    ).fetchall()
    con.close()
    return dados


def alterar(id_categoria, nome, ativo):
    con = conectar()
    con.execute(
        "UPDATE categoria SET nome = ?, ativo = ? WHERE id_categoria = ?",
        (nome, ativo, id_categoria),
    )
    con.commit()
    con.close()


def remover(id_categoria):
    con = conectar()
    con.execute("DELETE FROM categoria WHERE id_categoria = ?", (id_categoria,))
    con.commit()
    con.close()
