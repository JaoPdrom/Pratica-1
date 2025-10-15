# servidor_run.py

import sys
import os

# Adiciona o diretório raiz ao path para garantir que 'service' seja encontrado
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rpyc.utils.server import ThreadedServer
from service.JogoService import JogoService # Importação corrigida

print("Iniciando Servidor RPyC...")
# Cria uma instância do servidor
t = ThreadedServer(JogoService, port=18812)
# Roda o servidor
t.start()