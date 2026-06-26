#Aba de CRUD de Clientes.


from tkinter import ttk, messagebox

from src.dao import cliente_dao


class AbaClientes(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=12)
        self.id_selecionado = None
        self._montar()
        self.atualizar_lista()

    def _montar(self):
        form = ttk.LabelFrame(self, text="Dados do Cliente", padding=10)
        form.pack(fill="x")

        ttk.Label(form, text="Nome:").grid(row=0, column=0, sticky="w", pady=4)
        self.ent_nome = ttk.Entry(form, width=35)
        self.ent_nome.grid(row=0, column=1, padx=6, pady=4)

        ttk.Label(form, text="E-mail:").grid(row=0, column=2, sticky="w")
        self.ent_email = ttk.Entry(form, width=30)
        self.ent_email.grid(row=0, column=3, padx=6, pady=4)

        ttk.Label(form, text="Telefone:").grid(row=1, column=0, sticky="w", pady=4)
        self.ent_tel = ttk.Entry(form, width=35)
        self.ent_tel.grid(row=1, column=1, padx=6, pady=4)

        ttk.Label(form, text="Senha:").grid(row=1, column=2, sticky="w")
        self.ent_senha = ttk.Entry(form, width=30, show="*")
        self.ent_senha.grid(row=1, column=3, padx=6, pady=4)
        ttk.Label(form, text="(somente na inclusao)", foreground="#888").grid(
            row=2, column=3, sticky="w"
        )

        botoes = ttk.Frame(self)
        botoes.pack(fill="x", pady=8)
        ttk.Button(botoes, text="Incluir", command=self.incluir).pack(side="left")
        ttk.Button(botoes, text="Alterar", command=self.alterar).pack(side="left", padx=6)
        ttk.Button(botoes, text="Remover", command=self.remover).pack(side="left")
        ttk.Button(botoes, text="Limpar", command=self.limpar).pack(side="left", padx=6)

        busca = ttk.Frame(self)
        busca.pack(fill="x", pady=(0, 6))
        ttk.Label(busca, text="Consultar (nome/e-mail):").pack(side="left")
        self.ent_busca = ttk.Entry(busca, width=30)
        self.ent_busca.pack(side="left", padx=6)
        self.ent_busca.bind("<KeyRelease>", lambda e: self.atualizar_lista())

        cols = ("id", "nome", "email", "telefone")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=11)
        for c, t, w in [
            ("id", "ID", 50), ("nome", "Nome", 200),
            ("email", "E-mail", 230), ("telefone", "Telefone", 140),
        ]:
            self.tree.heading(c, text=t)
            self.tree.column(c, width=w, anchor="center" if c == "id" else "w")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.selecionar)

    def atualizar_lista(self):
        self.tree.delete(*self.tree.get_children())
        for c in cliente_dao.listar(self.ent_busca.get()):
            self.tree.insert(
                "", "end",
                values=(c["id_cliente"], c["nome"], c["email"], c["telefone"]),
            )

    def selecionar(self, _evento):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0])["values"]
        self.id_selecionado = vals[0]
        self.ent_nome.delete(0, "end"); self.ent_nome.insert(0, vals[1])
        self.ent_email.delete(0, "end"); self.ent_email.insert(0, vals[2])
        self.ent_tel.delete(0, "end"); self.ent_tel.insert(0, vals[3])
        self.ent_senha.delete(0, "end")

    def limpar(self):
        self.id_selecionado = None
        for e in (self.ent_nome, self.ent_email, self.ent_tel, self.ent_senha):
            e.delete(0, "end")
        self.tree.selection_remove(self.tree.selection())

    def incluir(self):
        nome, email = self.ent_nome.get().strip(), self.ent_email.get().strip()
        tel, senha = self.ent_tel.get().strip(), self.ent_senha.get().strip()
        if not (nome and email and tel and senha):
            messagebox.showwarning("Atencao", "Preencha nome, e-mail, telefone e senha.")
            return
        try:
            cliente_dao.incluir(nome, email, tel, senha)
        except Exception:
            messagebox.showerror("Erro", "E-mail ja cadastrado (deve ser unico).")
            return
        self.limpar()
        self.atualizar_lista()
        messagebox.showinfo("Sucesso", "Cliente incluido com sucesso.")

    def alterar(self):
        if not self.id_selecionado:
            messagebox.showwarning("Atencao", "Selecione um cliente na lista.")
            return
        nome, email, tel = (
            self.ent_nome.get().strip(),
            self.ent_email.get().strip(),
            self.ent_tel.get().strip(),
        )
        if not (nome and email and tel):
            messagebox.showwarning("Atencao", "Preencha nome, e-mail e telefone.")
            return
        try:
            cliente_dao.alterar(self.id_selecionado, nome, email, tel)
        except Exception:
            messagebox.showerror("Erro", "E-mail ja cadastrado em outro cliente.")
            return
        self.limpar()
        self.atualizar_lista()
        messagebox.showinfo("Sucesso", "Cliente alterado com sucesso.")

    def remover(self):
        if not self.id_selecionado:
            messagebox.showwarning("Atencao", "Selecione um cliente na lista.")
            return
        if messagebox.askyesno("Confirmar", "Deseja remover este cliente?"):
            try:
                cliente_dao.remover(self.id_selecionado)
            except Exception:
                messagebox.showerror(
                    "Erro", "Nao foi possivel remover: o cliente possui pedidos."
                )
                return
            self.limpar()
            self.atualizar_lista()
