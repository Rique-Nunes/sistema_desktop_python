# Zabeth's Gourmet — Sistema Desktop (RAD)

Sistema de gestão desktop para a doceria **Zabeth's Gourmet**, desenvolvido como
projeto da disciplina 4ADS - Tarde (FAETERJ).

Dupla: Esther Quarterolli dos Santos, Henrique da Costa Nunes

Arquitetura:

- **Linguagem:** Python
- **GUI:** Tkinter (interface gráfica nativa)
- **Banco de dados:** SQLite3
- **Métodos:** CRUDs básicos — Inclusão, Consulta, Alteração, Remoção e Relatório

## Como executar

Requer apenas **Python 3.14** (Tkinter e SQLite3 já vêm na instalação padrão).

```bash
cd sistema_desktop_python
python main.py
```

Na primeira execução o arquivo `zabeths.db` é criado automaticamente e populado
com dados fictícios. Para recriar o banco do zero, apague `zabeths.db` e rode de novo.

## Estrutura do projeto

O código é organizado em camadas (separação de responsabilidades):

```
sistema_desktop_python/
├── main.py                  # Ponto de entrada (inicializa o banco e abre a janela)
├── README.md
└── src/
    ├── config.py            # Constantes: caminho do banco, cores, status, pagamentos
    ├── database/            # Camada de banco de dados
    │   ├── conexao.py       #   conexao SQLite3 + hash de senha
    │   └── schema.py        #   criacao das tabelas + dados de exemplo
    ├── dao/                 # Camada de acesso a dados (CRUD por entidade)
    │   ├── categoria_dao.py
    │   ├── cliente_dao.py
    │   ├── produto_dao.py
    │   ├── pedido_dao.py
    │   └── relatorio_dao.py #   consultas agregadas dos relatorios
    └── ui/                  # Camada de interface (Tkinter)
        ├── janela_principal.py  # Janela + abas (Notebook)
        ├── aba_categorias.py
        ├── aba_clientes.py
        ├── aba_produtos.py
        ├── aba_pedidos.py
        └── aba_relatorios.py
```

**Como as camadas se comunicam:** a interface (`ui`) chama as funções do `dao`,
que por sua vez usam a conexão de `database`. Nenhuma tela acessa o banco
diretamente — isso deixa o código mais limpo e fácil de manter.

## Funcionalidades (CRUDs)

O sistema é organizado em abas, com botões padronizados para **Incluir, Alterar, Remover (Permanente)** e **Limpar Textos**:

- **Produtos** — nome, descrição, preço, categoria e checkbox de status ativo/inativo. A remoção é permanente (`DELETE` físico), mas protegida por restrição de chave estrangeira caso o produto possua histórico de vendas (neste caso, a inativação é feita marcando/desmarcando a caixa "Ativo" e clicando em "Alterar").
- **Categorias** — cadastro de categorias e checkbox de status ativo/inativo.
- **Clientes** — nome, e-mail (único), telefone e senha (armazenada de forma segura com hash SHA-256).
- **Pedidos** — seleciona cliente, monta carrinho com múltiplos produtos, calcula o valor total dinamicamente, define forma de pagamento, status de entrega e preenche um **endereço de entrega completo** com campos estruturados para CEP, Rua, Número, Bairro, Complemento e Cidade/UF.
- **Relatórios** — relatório de vendas com resumo geral (faturamento, ticket médio), vendas por produto e pedidos por status, com opção de exportar para `.txt`.


## Modelo de dados

`categoria` · `cliente` · `produto` · `pedido` · `item_pedido`

As tabelas seguem o mesmo minimundo do projeto de banco da Zabeth's Gourmet,
de forma simplificada para o sistema desktop.
