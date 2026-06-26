#Consultas agregadas usadas no Relatorio de Informacoes (vendas).

from src.database.conexao import conectar


def vendas_por_produto():
    #Total vendido por produto (quantidade e valor).
    con = conectar()
    dados = con.execute(
        """SELECT p.nome AS produto,
                  SUM(i.quantidade)                    AS qtd_vendida,
                  SUM(i.quantidade * i.preco_unitario) AS total
           FROM item_pedido i
           JOIN produto p ON p.id_produto = i.id_produto
           GROUP BY p.id_produto
           ORDER BY total DESC"""
    ).fetchall()
    con.close()
    return dados


def vendas_por_status():
    #Quantidade de pedidos e valor por status.
    con = conectar()
    dados = con.execute(
        """SELECT status_pedido,
                  COUNT(*)         AS qtd_pedidos,
                  SUM(valor_total) AS total
           FROM pedido
           GROUP BY status_pedido
           ORDER BY total DESC"""
    ).fetchall()
    con.close()
    return dados


def resumo_geral():
    #Indicadores gerais: total de pedidos, faturamento e ticket medio.
    con = conectar()
    dados = con.execute(
        """SELECT COUNT(*)                      AS total_pedidos,
                  COALESCE(SUM(valor_total), 0) AS faturamento,
                  COALESCE(AVG(valor_total), 0) AS ticket_medio
           FROM pedido"""
    ).fetchone()
    con.close()
    return dados
