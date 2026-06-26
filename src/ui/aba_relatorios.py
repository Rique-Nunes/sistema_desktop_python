#Aba de Relatorio de Informacoes (vendas)

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from src.dao import relatorio_dao


class AbaRelatorios(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=12)
        self._montar()
        self.gerar()

    def _montar(self):
        topo = ttk.Frame(self)
        topo.pack(fill="x")
        ttk.Label(topo, text="Relatorio de Vendas", font=("Segoe UI", 13, "bold")).pack(
            side="left"
        )
        ttk.Button(topo, text="Atualizar", command=self.gerar).pack(side="right")
        ttk.Button(topo, text="Exportar .txt", command=self.exportar).pack(side="right", padx=6)

        self.txt = tk.Text(self, height=26, font=("Consolas", 10), wrap="none")
        self.txt.pack(fill="both", expand=True, pady=8)

    def _conteudo(self):
        linhas = []
        linhas.append("=" * 58)
        linhas.append("        ZABETH'S GOURMET - RELATORIO DE VENDAS")
        linhas.append("=" * 58)

        resumo = relatorio_dao.resumo_geral()
        linhas.append("")
        linhas.append("RESUMO GERAL")
        linhas.append("-" * 58)
        linhas.append(f"Total de pedidos : {resumo['total_pedidos']}")
        linhas.append(f"Faturamento total: R$ {resumo['faturamento']:.2f}")
        linhas.append(f"Ticket medio     : R$ {resumo['ticket_medio']:.2f}")

        linhas.append("")
        linhas.append("VENDAS POR PRODUTO")
        linhas.append("-" * 58)
        linhas.append(f"{'Produto':<30}{'Qtd':>8}{'Total':>18}")
        for r in relatorio_dao.vendas_por_produto():
            linhas.append(
                f"{r['produto'][:29]:<30}{r['qtd_vendida']:>8}{('R$ %.2f' % r['total']):>18}"
            )

        linhas.append("")
        linhas.append("PEDIDOS POR STATUS")
        linhas.append("-" * 58)
        linhas.append(f"{'Status':<30}{'Qtd':>8}{'Total':>18}")
        for r in relatorio_dao.vendas_por_status():
            linhas.append(
                f"{r['status_pedido'][:29]:<30}{r['qtd_pedidos']:>8}{('R$ %.2f' % (r['total'] or 0)):>18}"
            )
        linhas.append("")
        linhas.append("=" * 58)
        return "\n".join(linhas)

    def gerar(self):
        self.txt.delete("1.0", "end")
        self.txt.insert("1.0", self._conteudo())

    def exportar(self):
        caminho = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Texto", "*.txt")],
            initialfile="relatorio_vendas.txt",
        )
        if caminho:
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(self._conteudo())
            messagebox.showinfo("Sucesso", f"Relatorio exportado para:\n{caminho}")
