# cliente_run.py

import sys
import os
import tkinter as tk

# Adiciona o diretório raiz ao path para garantir que 'controller' seja encontrado
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controller.cliente import ClienteApp # Importa a classe do Controller

if __name__ == "__main__":
    root = tk.Tk()
    # O Controller é instanciado, iniciando a conexão e o loop de atualização
    app = ClienteApp()
    root.mainloop()