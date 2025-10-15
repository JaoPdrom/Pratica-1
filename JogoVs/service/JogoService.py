# JogoService.py
import rpyc
from Jogo import Jogo

class JogoService(rpyc.Service):
    def __init__(self):
        self.jogo = Jogo()

    def on_connect(self, conn):
        print("[+] Novo cliente conectado.")

    # --- História ---
    def exposed_obter_trecho(self):
        return self.jogo.obter_trecho()

    # --- Jogadores ---
    def exposed_entrar_no_jogo(self, jogador):
        return self.jogo.entrar_no_jogo(jogador)

    def exposed_obter_jogadores(self):
        return self.jogo.obter_jogadores()

    # --- Votação ---
    def exposed_registrar_voto(self, jogador, opcao):
        return self.jogo.registrar_voto(jogador, opcao)

    # --- Chat ---
    def exposed_enviar_mensagem(self, jogador, mensagem):
        return self.jogo.enviar_mensagem(jogador, mensagem)

    def exposed_obter_chat(self):
        return self.jogo.obter_chat()

    def exposed_obter_opcoes(self):
        return self.jogo.obter_opcoes()
