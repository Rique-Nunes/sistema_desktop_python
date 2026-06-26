#Aba de CRUD de Pedidos 

from tkinter import ttk, messagebox

from src.config import STATUS_PEDIDO, FORMAS_PAGAMENTO
from src.dao import pedido_dao, cliente_dao, produto_dao


class AbaPedidos(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=12)
        self.id_selecionado = None
        self.mapa_clientes = {}
        self.mapa_produtos = {}
        self.itens_carrinho = []
        self._montar()
        self.carregar_combos()
        self.atualizar_lista()

    def _montar(self):
        form = ttk.LabelFrame(self, text="Novo Pedido", padding=10)
        form.pack(fill="x")

        ttk.Label(form, text="Cliente:").grid(row=0, column=0, sticky="w", pady=4)
        self.cmb_cliente = ttk.Combobox(form, width=30, state="readonly")
        self.cmb_cliente.grid(row=0, column=1, padx=6, pady=4)

        ttk.Label(form, text="Pagamento:").grid(row=0, column=2, sticky="w")
        self.cmb_pag = ttk.Combobox(form, width=12, state="readonly", values=FORMAS_PAGAMENTO)
        self.cmb_pag.current(0)
        self.cmb_pag.grid(row=0, column=3, padx=6, pady=4)

        ttk.Label(form, text="Status:").grid(row=1, column=0, sticky="w", pady=4)
        self.cmb_status = ttk.Combobox(form, width=30, state="readonly", values=STATUS_PEDIDO)
        self.cmb_status.current(0)
        self.cmb_status.grid(row=1, column=1, padx=6, pady=4)

        ttk.Label(form, text="Endereco:").grid(row=1, column=2, sticky="w")
        self.ent_end = ttk.Entry(form, width=30)
        self.ent_end.grid(row=1, column=3, padx=6, pady=4)

        item_fr = ttk.LabelFrame(self, text="Itens do Pedido", padding=10)
        item_fr.pack(fill="x", pady=6)
        ttk.Label(item_fr, text="Produto:").grid(row=0, column=0, sticky="w")
        self.cmb_produto = ttk.Combobox(item_fr, width=28, state="readonly")
        self.cmb_produto.grid(row=0, column=1, padx=6)
        ttk.Label(item_fr, text="Qtd:").grid(row=0, column=2, sticky="w")
        self.ent_qtd = ttk.Entry(item_fr, width=6)
        self.ent_qtd.insert(0, "1")
        self.ent_qtd.grid(row=0, column=3, padx=6)
        ttk.Button(item_fr, text="Adicionar item", command=self.adicionar_item).grid(
            row=0, column=4, padx=6
        )
        ttk.Button(item_fr, text="Limpar itens", command=self.limpar_itens).grid(row=0, column=5)

        self.lst_itens = ttk.Treeview(
            item_fr, columns=("prod", "qtd", "preco", "sub"), show="headings", height=4
        )
        for c, t, w in [
            ("prod", "Produto", 230), ("qtd", "Qtd", 60),
            ("preco", "Preco", 90), ("sub", "Subtotal", 100),
        ]:
            self.lst_itens.heading(c, text=t)
            self.lst_itens.column(c, width=w, anchor="w" if c == "prod" else "center")
        self.lst_itens.grid(row=1, column=0, columnspan=6, pady=6, sticky="we")
        self.lbl_total = ttk.Label(item_fr, text="Total: R$ 0.00", font=("Segoe UI", 10, "bold"))
        self.lbl_total.grid(row=2, column=0, columnspan=6, sticky="e")

        botoes = ttk.Frame(self)
        botoes.pack(fill="x", pady=6)
        ttk.Button(botoes, text="Salvar Pedido", command=self.incluir).pack(side="left")
        ttk.Button(botoes, text="Alterar Status", command=self.alterar_status).pack(
            side="left", padx=6
        )
        ttk.Button(botoes, text="Remover Pedido", command=self.remover).pack(side="left")
        ttk.Button(botoes, text="Ver Itens", command=self.ver_itens).pack(side="left", padx=6)
        ttk.Button(botoes, text="Novo", command=self.limpar).pack(side="left")

        busca = ttk.Frame(self)
        busca.pack(fill="x", pady=(0, 6))
        ttk.Label(busca, text="Consultar (cliente):").pack(side="left")
        self.ent_busca = ttk.Entry(busca, width=25)
        self.ent_busca.pack(side="left", padx=6)
        self.ent_busca.bind("<KeyRelease>", lambda e: self.atualizar_lista())

        cols = ("id", "cliente", "data", "total", "status", "pag")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=8)
        for c, t, w in [
            ("id", "ID", 45), ("cliente", "Cliente", 160), ("data", "Data", 130),
            ("total", "Total", 90), ("status", "Status", 150), ("pag", "Pagamento", 90),
        ]:
            self.tree.heading(c, text=t)
            self.tree.column(c, width=w, anchor="w" if c == "cliente" else "center")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.selecionar)

    def carregar_combos(self):
        self.mapa_clientes = {}
        nomes_c = []
        for c in cliente_dao.listar():
            rotulo = f"{c['id_cliente']} - {c['nome']}"
            self.mapa_clientes[rotulo] = c["id_cliente"]
            nomes_c.append(rotulo)
        self.cmb_cliente["values"] = nomes_c

        self.mapa_produtos = {}
        nomes_p = []
        for p in produto_dao.listar():
            if p["ativo"]:
                self.mapa_produtos[p["nome"]] = (p["id_produto"], p["preco"])
                nomes_p.append(p["nome"])
        self.cmb_produto["values"] = nomes_p

    def adicionar_item(self):
        nome = self.cmb_produto.get()
        if not nome:
            messagebox.showwarning("Atencao", "Selecione um produto.")
            return
        try:
            qtd = int(self.ent_qtd.get())
            if qtd <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Atencao", "Quantidade invalida.")
            return
        id_prod, preco = self.mapa_produtos[nome]
        self.itens_carrinho.append((id_prod, nome, qtd, preco))
        self._render_itens()

    def _render_itens(self):
        self.lst_itens.delete(*self.lst_itens.get_children())
        total = 0
        for (_, nome, qtd, preco) in self.itens_carrinho:
            sub = qtd * preco
            total += sub
            self.lst_itens.insert(
                "", "end", values=(nome, qtd, f"R$ {preco:.2f}", f"R$ {sub:.2f}")
            )
        self.lbl_total.config(text=f"Total: R$ {total:.2f}")

    def limpar_itens(self):
        self.itens_carrinho = []
        self._render_itens()

    def atualizar_lista(self):
        self.tree.delete(*self.tree.get_children())
        for pe in pedido_dao.listar(self.ent_busca.get()):
            self.tree.insert(
                "", "end",
                values=(
                    pe["id_pedido"], pe["cliente_nome"], pe["data_hora"],
                    f"R$ {pe['valor_total']:.2f}", pe["status_pedido"], pe["forma_pagamento"],
                ),
            )

    def selecionar(self, _evento):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0])["values"]
        self.id_selecionado = vals[0]
        self.cmb_status.set(vals[4])

    def limpar(self):
        self.id_selecionado = None
        self.cmb_cliente.set("")
        self.cmb_pag.current(0)
        self.cmb_status.current(0)
        self.ent_end.delete(0, "end")
        self.limpar_itens()
        self.tree.selection_remove(self.tree.selection())

    def incluir(self):
        rotulo = self.cmb_cliente.get()
        if not rotulo:
            messagebox.showwarning("Atencao", "Selecione o cliente.")
            return
        if not self.itens_carrinho:
            messagebox.showwarning("Atencao", "Adicione ao menos um item ao pedido.")
            return
        id_cliente = self.mapa_clientes[rotulo]
        itens = [(idp, qtd, preco) for (idp, _, qtd, preco) in self.itens_carrinho]
        pedido_dao.incluir(
            id_cliente, self.cmb_pag.get(), self.cmb_status.get(),
            self.ent_end.get().strip(), itens,
        )
        self.limpar()
        self.atualizar_lista()
        messagebox.showinfo("Sucesso", "Pedido salvo com sucesso.")

    def alterar_status(self):
        if not self.id_selecionado:
            messagebox.showwarning("Atencao", "Selecione um pedido na lista.")
            return
        pedido_dao.alterar_status(self.id_selecionado, self.cmb_status.get())
        self.atualizar_lista()
        messagebox.showinfo("Sucesso", "Status do pedido atualizado.")

    def remover(self):
        if not self.id_selecionado:
            messagebox.showwarning("Atencao", "Selecione um pedido na lista.")
            return
        if messagebox.askyesno("Confirmar", "Deseja remover este pedido?"):
            pedido_dao.remover(self.id_selecionado)
            self.limpar()
            self.atualizar_lista()

    def ver_itens(self):
        if not self.id_selecionado:
            messagebox.showwarning("Atencao", "Selecione um pedido na lista.")
            return
        linhas = pedido_dao.listar_itens(self.id_selecionado)
        if not linhas:
            messagebox.showinfo("Itens", "Este pedido nao possui itens.")
            return
        texto = "\n".join(
            f"- {l['produto_nome']}: {l['quantidade']} x R$ {l['preco_unitario']:.2f}"
            for l in linhas
        )
        messagebox.showinfo(f"Itens do pedido #{self.id_selecionado}", texto)
