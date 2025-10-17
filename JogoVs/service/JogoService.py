# service/JogoService.py
import os
import rpyc
import logging
from datetime import datetime
from model.motor_jogo import MotorJogo  # importa o motor do jogo

# === Configuração de Logs ===
os.makedirs("logs", exist_ok=True)  # garante que a pasta exista

log_path = os.path.join("logs", "log_servidor.txt")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_path, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

log = logging.getLogger("ServidorRPyC")

# === Instância global do motor do jogo ===
motor_global = MotorJogo("historia.yaml")


class JogoService(rpyc.Service):
    # --- Conexão ---
    def on_connect(self, conn):
        """Chamado quando um cliente se conecta ao servidor."""
        self.conn = conn  # ✅ guarda a conexão para uso posterior
        log.info(f"Novo cliente conectado: {conn}")

    def on_disconnect(self, conn):
        """Chamado quando o cliente se desconecta."""
        jogador = getattr(conn, "jogador", None)
        if jogador:
            log.info(f"Jogador '{jogador}' se desconectou.")
        else:
            log.info("Cliente desconectado (não identificado).")

    # --- Jogadores ---
    def exposed_entrar_no_jogo(self, jogador):
        """Registra a entrada de um novo jogador."""
        conn = self.conn  # ✅ agora existe
        conn.jogador = jogador
        log.info(f"Jogador '{jogador}' entrou no jogo.")
        return motor_global.adicionar_jogador(jogador)

    def exposed_obter_jogadores(self):
        jogadores = list(motor_global.jogadores_conectados.keys())
        log.info(f"Lista de jogadores conectados: {jogadores}")
        return jogadores

    # --- História ---
    def exposed_obter_trecho(self):
        trecho = motor_global.obter_trecho_atual()
        log.info("Trecho atual solicitado pelo cliente.")
        return trecho

    def exposed_obter_opcoes(self):
        trecho = motor_global.obter_trecho_atual(formatado=False)
        if isinstance(trecho, dict):
            opcoes = trecho.get("opcoes", [])
            log.info(f"Opções enviadas: {[o['texto'] for o in opcoes]}")
            return {str(i + 1): o["texto"] for i, o in enumerate(opcoes)}
        log.info("Nenhuma opção disponível para este trecho.")
        return {}

    # --- Votação ---
    def exposed_registrar_voto(self, jogador, opcao):
        try:
            log.info(f"Jogador '{jogador}' votou na opção {opcao}.")
            resultado = motor_global.registrar_voto(jogador, int(opcao))
            log.info(f"Resultado parcial da votação: {motor_global.votos}")
            return resultado
        except Exception as e:
            log.error(f"Falha ao registrar voto de {jogador}: {e}")
            return f"Erro ao registrar voto: {e}"

    # --- Chat ---
    def exposed_enviar_mensagem(self, jogador, mensagem):
        log.info(f"Mensagem de '{jogador}': {mensagem}")
        return motor_global.enviar_mensagem_chat(jogador, mensagem)

    def exposed_obter_chat(self):
        log.info("Chat solicitado por cliente.")
        return motor_global.obter_chat()

    # --- Status do jogo ---
    def exposed_obter_jogo_iniciado(self):
        status = motor_global.jogo_iniciado
        log.info(f"Estado do jogo solicitado: {'Iniciado' if status else 'Aguardando jogadores'}.")
        return status
