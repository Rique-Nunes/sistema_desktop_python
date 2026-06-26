#Aba de CRUD de Produtos. 


import tkinter as tk
from tkinter import ttk, messagebox

from src.dao import produto_dao, categoria_dao


class AbaProdutos(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=12)
        self.id_selecionado = None
        self.mapa_categorias = {}
        self._montar()
        self.carregar_categorias()
        self.atualizar_lista()

    def _montar(self):
        form = ttk.LabelFrame(self, text="Dados do Produto", padding=10)
        form.pack(fill="x")

        ttk.Label(form, text="Nome:").grid(row=0, column=0, sticky="w", pady=4)
        self.ent_nome = ttk.Entry(form, width=35)
        self.ent_nome.grid(row=0, column=1, padx=6, pady=4)

        ttk.Label(form, text="Preco (R$):").grid(row=0, column=2, sticky="w")
        self.ent_preco = ttk.Entry(form, width=15)
        self.ent_preco.grid(row=0, column=3, padx=6, pady=4, sticky="w")

        ttk.Label(form, text="Categoria:").grid(row=1, column=0, sticky="w", pady=4)
        self.cmb_categoria = ttk.Combobox(form, width=32, state="readonly")
        self.cmb_categoria.grid(row=1, column=1, padx=6, pady=4)

        ttk.Label(form, text="Ativo:").grid(row=1, column=2, sticky="w")
        self.var_ativo = tk.IntVar(value=1)
        ttk.Checkbutton(form, variable=self.var_ativo).grid(row=1, column=3, sticky="w")

        ttk.Label(form, text="Descricao:").grid(row=2, column=0, sticky="nw", pady=4)
        self.txt_desc = tk.Text(form, width=60, height=3)
        self.txt_desc.grid(row=2, column=1, columnspan=3, padx=6, pady=4, sticky="w")

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

        cols = ("id", "nome", "preco", "categoria", "ativo")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=10)
        for c, t, w in [
            ("id", "ID", 45), ("nome", "Nome", 210), ("preco", "Preco", 90),
            ("categoria", "Categoria", 140), ("ativo", "Ativo", 70),
        ]:
            self.tree.heading(c, text=t)
            self.tree.column(c, width=w, anchor="w" if c in ("nome", "categoria") else "center")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.selecionar)

    def carregar_categorias(self):
        self.mapa_categorias = {}
        nomes = []
        for cat in categoria_dao.listar():
            self.mapa_categorias[cat["nome"]] = cat["id_categoria"]
            nomes.append(cat["nome"])
        self.cmb_categoria["values"] = nomes

    def atualizar_lista(self):
        self.tree.delete(*self.tree.get_children())
        for p in produto_dao.listar(self.ent_busca.get()):
            self.tree.insert(
                "", "end",
                values=(
                    p["id_produto"], p["nome"], f"R$ {p['preco']:.2f}",
                    p["categoria_nome"] or "-", "Sim" if p["ativo"] else "Nao",
                ),
            )

    def selecionar(self, _evento):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0])["values"]
        self.id_selecionado = vals[0]
        for p in produto_dao.listar():
            if p["id_produto"] == vals[0]:
                self.ent_nome.delete(0, "end"); self.ent_nome.insert(0, p["nome"])
                self.ent_preco.delete(0, "end"); self.ent_preco.insert(0, f"{p['preco']:.2f}")
                self.cmb_categoria.set(p["categoria_nome"] or "")
                self.var_ativo.set(p["ativo"])
                self.txt_desc.delete("1.0", "end")
                self.txt_desc.insert("1.0", p["descricao"] or "")
                break

    def limpar(self):
        self.id_selecionado = None
        self.ent_nome.delete(0, "end")
        self.ent_preco.delete(0, "end")
        self.cmb_categoria.set("")
        self.var_ativo.set(1)
        self.txt_desc.delete("1.0", "end")
        self.tree.selection_remove(self.tree.selection())

    def _ler_form(self):
        nome = self.ent_nome.get().strip()
        desc = self.txt_desc.get("1.0", "end").strip()
        cat_nome = self.cmb_categoria.get()
        if not nome or not self.ent_preco.get().strip():
            messagebox.showwarning("Atencao", "Informe nome e preco.")
            return None
        try:
            preco = float(self.ent_preco.get().replace(",", "."))
        except ValueError:
            messagebox.showwarning("Atencao", "Preco invalido. Use numeros (ex: 18.50).")
            return None
        id_cat = self.mapa_categorias.get(cat_nome)
        return nome, desc, preco, id_cat

    def incluir(self):
        dados = self._ler_form()
        if not dados:
            return
        produto_dao.incluir(*dados)
        self.limpar()
        self.atualizar_lista()
        messagebox.showinfo("Sucesso", "Produto incluido com sucesso.")

    def alterar(self):
        if not self.id_selecionado:
            messagebox.showwarning("Atencao", "Selecione um produto na lista.")
            return
        dados = self._ler_form()
        if not dados:
            return
        nome, desc, preco, id_cat = dados
        produto_dao.alterar(self.id_selecionado, nome, desc, preco, id_cat, self.var_ativo.get())
        self.limpar()
        self.atualizar_lista()
        messagebox.showinfo("Sucesso", "Produto alterado com sucesso.")

    def remover(self):
        if not self.id_selecionado:
            messagebox.showwarning("Atencao", "Selecione um produto na lista.")
            return
        if messagebox.askyesno(
            "Confirmar", "Deseja remover este produto permanentemente do banco de dados?"
        ):
            try:
                produto_dao.excluir_definitivo(self.id_selecionado)
                self.limpar()
                self.atualizar_lista()
                messagebox.showinfo("Sucesso", "Produto removido com sucesso.")
            except Exception:
                messagebox.showerror(
                    "Erro",
                    "Nao foi possivel remover este produto permanentemente porque ele possui historico de vendas.\n"
                    "Caso queira desativa-lo, desmarque a caixa 'Ativo' e clique em 'Alterar'.",
                )
