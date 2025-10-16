# service/JogoService.py
import os
import rpyc
from model.motor_jogo import MotorJogo  # importa o motor do jogo

# 🔹 Cria uma única instância global do jogo (compartilhada entre todos os clientes)
motor_global = MotorJogo("historia.yaml")

class JogoService(rpyc.Service):
    def on_connect(self, conn):
        print("[+] Novo cliente conectado.")

    # --- Jogadores ---
    def exposed_entrar_no_jogo(self, jogador):
        return motor_global.adicionar_jogador(jogador)

    def exposed_obter_jogadores(self):
        return list(motor_global.jogadores_conectados.keys())

    # --- História ---
    def exposed_obter_trecho(self):
        return motor_global.obter_trecho_atual()

    def exposed_obter_opcoes(self):
        trecho = motor_global.obter_trecho_atual(formatado=False)
        if isinstance(trecho, dict):
            opcoes = trecho.get("opcoes", [])
            return {str(i + 1): o["texto"] for i, o in enumerate(opcoes)}
        return {}

    # --- Votação ---
    def exposed_registrar_voto(self, jogador, opcao):
        try:
            return motor_global.registrar_voto(jogador, int(opcao))
        except Exception as e:
            return f"Erro ao registrar voto: {e}"

    # --- Chat ---
    def exposed_enviar_mensagem(self, jogador, mensagem):
        return motor_global.enviar_mensagem_chat(jogador, mensagem)

    def exposed_obter_chat(self):
        return motor_global.obter_chat()

    # --- Status do jogo ---
    def exposed_obter_jogo_iniciado(self):
        return motor_global.jogo_iniciado
