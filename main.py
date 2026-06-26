#Ponto de entrada do sistema desktop da Zabeth's Gourmet.

from src.database.schema import inicializar_banco
from src.ui.janela_principal import Aplicacao


def main():
    inicializar_banco()      
    app = Aplicacao()
    app.mainloop()


if __name__ == "__main__":
    main()
