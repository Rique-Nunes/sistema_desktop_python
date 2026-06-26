#Janela principal: monta o cabecalho e o Notebook com todas as abas.

import tkinter as tk
from tkinter import ttk

from src.config import COR_FUNDO, COR_PRIMARIA
from src.ui.aba_produtos import AbaProdutos
from src.ui.aba_categorias import AbaCategorias
from src.ui.aba_clientes import AbaClientes
from src.ui.aba_pedidos import AbaPedidos
from src.ui.aba_relatorios import AbaRelatorios


class Aplicacao(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Zabeth's Gourmet - Sistema de Gestao (RAD)")
        self.geometry("900x640")
        self.configure(bg=COR_FUNDO)

        estilo = ttk.Style(self)
        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass
        estilo.configure("TButton", padding=6)

        cabecalho = tk.Label(
            self, text="\U0001F370  Zabeth's Gourmet - Painel de Gestao",
            bg=COR_PRIMARIA, fg="white", font=("Segoe UI", 15, "bold"), pady=12,
        )
        cabecalho.pack(fill="x")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.aba_produtos = AbaProdutos(notebook)
        self.aba_categorias = AbaCategorias(notebook)
        self.aba_clientes = AbaClientes(notebook)
        self.aba_pedidos = AbaPedidos(notebook)
        self.aba_relatorios = AbaRelatorios(notebook)

        notebook.add(self.aba_produtos, text="Produtos")
        notebook.add(self.aba_categorias, text="Categorias")
        notebook.add(self.aba_clientes, text="Clientes")
        notebook.add(self.aba_pedidos, text="Pedidos")
        notebook.add(self.aba_relatorios, text="Relatorios")

        def ao_trocar_aba(_e):
            aba = notebook.tab(notebook.select(), "text")
            if aba == "Produtos":
                self.aba_produtos.carregar_categorias()
            elif aba == "Pedidos":
                self.aba_pedidos.carregar_combos()
                self.aba_pedidos.atualizar_lista()
            elif aba == "Relatorios":
                self.aba_relatorios.gerar()

        notebook.bind("<<NotebookTabChanged>>", ao_trocar_aba)
