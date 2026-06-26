#Operacoes CRUD da entidade Cliente.

from src.database.conexao import conectar, hash_senha


def incluir(nome, email, telefone, senha):
    con = conectar()
    con.execute(
        "INSERT INTO cliente (nome, email, telefone, senha) VALUES (?, ?, ?, ?)",
        (nome, email, telefone, hash_senha(senha)),
    )
    con.commit()
    con.close()


def listar(filtro=""):
    con = conectar()
    dados = con.execute(
        """SELECT * FROM cliente
           WHERE nome LIKE ? OR email LIKE ?
           ORDER BY nome""",
        (f"%{filtro}%", f"%{filtro}%"),
    ).fetchall()
    con.close()
    return dados


def alterar(id_cliente, nome, email, telefone):
    con = conectar()
    con.execute(
        "UPDATE cliente SET nome = ?, email = ?, telefone = ? WHERE id_cliente = ?",
        (nome, email, telefone, id_cliente),
    )
    con.commit()
    con.close()


def remover(id_cliente):
    con = conectar()
    con.execute("DELETE FROM cliente WHERE id_cliente = ?", (id_cliente,))
    con.commit()
    con.close()
