#Aba de CRUD de Categorias.

import tkinter as tk
from tkinter import ttk, messagebox

from src.dao import categoria_dao


class AbaCategorias(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=12)
        self.id_selecionado = None
        self._montar()
        self.atualizar_lista()

    def _montar(self):
        form = ttk.LabelFrame(self, text="Dados da Categoria", padding=10)
        form.pack(fill="x")

        ttk.Label(form, text="Nome:").grid(row=0, column=0, sticky="w", pady=4)
        self.ent_nome = ttk.Entry(form, width=40)
        self.ent_nome.grid(row=0, column=1, padx=6, pady=4)

        ttk.Label(form, text="Ativo:").grid(row=0, column=2, sticky="w", padx=(12, 0))
        self.var_ativo = tk.IntVar(value=1)
        ttk.Checkbutton(form, variable=self.var_ativo).grid(row=0, column=3, sticky="w")

        botoes = ttk.Frame(self)
        botoes.pack(fill="x", pady=8)
        ttk.Button(botoes, text="Incluir", command=self.incluir).pack(side="left")
        ttk.Button(botoes, text="Alterar", command=self.alterar).pack(side="left", padx=6)
        ttk.Button(botoes, text="Remover (Permanente)", command=self.remover).pack(side="left")
        ttk.Button(botoes, text="Limpar Textos", command=self.limpar).pack(side="left", padx=6)

        busca = ttk.Frame(self)
        busca.pack(fill="x", pady=(0, 6))
        ttk.Label(busca, text="Consultar:").pack(side="left")
        self.ent_busca = ttk.Entry(busca, width=30)
        self.ent_busca.pack(side="left", padx=6)
        self.ent_busca.bind("<KeyRelease>", lambda e: self.atualizar_lista())

        cols = ("id", "nome", "ativo")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=12)
        for c, t, w in [("id", "ID", 50), ("nome", "Nome", 300), ("ativo", "Ativo", 80)]:
            self.tree.heading(c, text=t)
            self.tree.column(c, width=w, anchor="center" if c != "nome" else "w")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.selecionar)

    def atualizar_lista(self):
        self.tree.delete(*self.tree.get_children())
        for cat in categoria_dao.listar(self.ent_busca.get()):
            self.tree.insert(
                "", "end",
                values=(cat["id_categoria"], cat["nome"], "Sim" if cat["ativo"] else "Nao"),
            )

    def selecionar(self, _evento):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0])["values"]
        self.id_selecionado = vals[0]
        self.ent_nome.delete(0, "end")
        self.ent_nome.insert(0, vals[1])
        self.var_ativo.set(1 if vals[2] == "Sim" else 0)

    def limpar(self):
        self.id_selecionado = None
        self.ent_nome.delete(0, "end")
        self.var_ativo.set(1)
        self.tree.selection_remove(self.tree.selection())

    def incluir(self):
        nome = self.ent_nome.get().strip()
        if not nome:
            messagebox.showwarning("Atencao", "Informe o nome da categoria.")
            return
        categoria_dao.incluir(nome)
        self.limpar()
        self.atualizar_lista()
        messagebox.showinfo("Sucesso", "Categoria incluida com sucesso.")

    def alterar(self):
        if not self.id_selecionado:
            messagebox.showwarning("Atencao", "Selecione uma categoria na lista.")
            return
        nome = self.ent_nome.get().strip()
        if not nome:
            messagebox.showwarning("Atencao", "Informe o nome da categoria.")
            return
        categoria_dao.alterar(self.id_selecionado, nome, self.var_ativo.get())
        self.limpar()
        self.atualizar_lista()
        messagebox.showinfo("Sucesso", "Categoria alterada com sucesso.")

    def remover(self):
        if not self.id_selecionado:
            messagebox.showwarning("Atencao", "Selecione uma categoria na lista.")
            return
        if messagebox.askyesno("Confirmar", "Deseja remover esta categoria?"):
            try:
                categoria_dao.remover(self.id_selecionado)
            except Exception:
                messagebox.showerror(
                    "Erro", "Nao foi possivel remover: existem produtos nesta categoria."
                )
                return
            self.limpar()
            self.atualizar_lista()
