# controller/cliente.py
import tkinter as tk
from tkinter import messagebox
import threading
import time
import rpyc

# Importa telas da view
from view.prejogo.nome_jogador import Toplevel1 as TelaNome
from view.prejogo.aguardando_jogadores import Toplevel1 as TelaAguardando
from view.interface import Toplevel1 as TelaJogo


class ClienteApp:
    """Controller principal do cliente — gerencia telas e comunicação RPyC."""

    def __init__(self):
        # Cria a janela raiz do Tkinter e a esconde imediatamente
        self.root = tk.Tk()
        self.root.withdraw()  # evita exibir a janela "tk"

        self.conn = None
        self.servico = None
        self.jogador = None

        self.conectar_servidor()
        if self.servico:
            self.mostrar_tela_nome()
            self.root.mainloop()

    # ========================
    # Conexão com o servidor
    # ========================
    def conectar_servidor(self):
        try:
            self.conn = rpyc.connect("localhost", 18812)
            self.servico = self.conn.root
            print("[Cliente] Conectado ao servidor RPyC.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao conectar no servidor:\n{e}")
            self.root.destroy()

    # ========================
    # Tela de Nome do Jogador
    # ========================
    def mostrar_tela_nome(self):
        self.janela_nome = tk.Toplevel(self.root)
        self.tela_nome = TelaNome(self.janela_nome)
        self.janela_nome.title("Escolha seu nome")
        self.tela_nome.TBtnEntrar.config(command=self.confirmar_nome)

    def confirmar_nome(self):
        nome = self.tela_nome.TNomeJogador.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Por favor, insira um nome válido.")
            return

        self.jogador = nome
        resposta = self.servico.entrar_no_jogo(self.jogador)
        messagebox.showinfo("Conectado", resposta)
        self.janela_nome.destroy()
        self.mostrar_tela_aguardando()

    # ========================
    # Tela de Espera
    # ========================
    def mostrar_tela_aguardando(self):
        self.janela_aguardando = tk.Toplevel(self.root)
        self.tela_aguardando = TelaAguardando(self.janela_aguardando)
        self.janela_aguardando.title("Aguardando jogadores...")

        self.label_status = tk.Label(
            self.tela_aguardando.Frame1,
            text="Jogadores conectados: 1/4",
            background="#d9d9d9",
            font=("Arial", 10)
        )
        self.label_status.place(relx=0.18, rely=0.7)

        threading.Thread(target=self.loop_aguardando, daemon=True).start()

    def loop_aguardando(self):
        """Atualiza a tela de espera até que o jogo comece."""
        while True:
            try:
                jogadores = self.servico.obter_jogadores()
                total = len(jogadores)
                self.label_status.config(text=f"Jogadores conectados: {total}/4")

                # Verifica com o servidor se o jogo já começou (>= 4 jogadores)
                jogo_iniciado = self.servico.obter_jogo_iniciado()
                if jogo_iniciado:
                    print("[Cliente] Jogo iniciado!")
                    # Usa after() para garantir que a GUI feche no thread correto
                    self.janela_aguardando.after(0, self.janela_aguardando.destroy)
                    self.root.after(200, self.iniciar_jogo)
                    break

            except Exception as e:
                print("Erro ao verificar jogadores:", e)
                break

            time.sleep(1)

    # ========================
    # Tela do Jogo Principal
    # ========================
    def iniciar_jogo(self):
        self.janela_jogo = tk.Toplevel(self.root)
        self.tela_jogo = TelaJogo(self.janela_jogo)
        self.janela_jogo.title(f"Jogo - {self.jogador}")

        # Liga botões da interface
        self.tela_jogo.btnChatEnviarMensagem.config(command=self.enviar_chat)
        self.tela_jogo.btnVotOpcao1.config(command=lambda: self.votar(1))
        self.tela_jogo.btnVotOpcao2.config(command=lambda: self.votar(2))
        self.tela_jogo.btnVotOpcao3.config(command=lambda: self.votar(3))
        self.tela_jogo.btnVotOpcao4.config(command=lambda: self.votar(4))

        # Thread de atualização da interface
        threading.Thread(target=self.loop_atualizacao, daemon=True).start()

    def loop_atualizacao(self):
        while True:
            try:
                self.atualizar_historia()
                self.atualizar_chat()
                self.atualizar_opcoes()
            except Exception as e:
                print("Erro ao atualizar interface:", e)
            time.sleep(1)

    def atualizar_historia(self):
        trecho = self.servico.obter_trecho()
        self.tela_jogo.Scrolledtext1.config(state="normal")
        self.tela_jogo.Scrolledtext1.delete("1.0", tk.END)
        self.tela_jogo.Scrolledtext1.insert(tk.END, trecho)
        self.tela_jogo.Scrolledtext1.config(state="disabled")

    def atualizar_chat(self):
        chat = self.servico.obter_chat()
        self.tela_jogo.Scrolledtext2.config(state="normal")
        self.tela_jogo.Scrolledtext2.delete("1.0", tk.END)
        self.tela_jogo.Scrolledtext2.insert(tk.END, chat)
        self.tela_jogo.Scrolledtext2.config(state="disabled")

    def atualizar_opcoes(self):
        opcoes = self.servico.obter_opcoes()
        botoes = [
            self.tela_jogo.btnVotOpcao1,
            self.tela_jogo.btnVotOpcao2,
            self.tela_jogo.btnVotOpcao3,
            self.tela_jogo.btnVotOpcao4
        ]

        for i, botao in enumerate(botoes, start=1):
            if str(i) in opcoes:
                botao.config(text=f"{i}: {opcoes[str(i)]}", state="normal")
            else:
                botao.config(text=f"Opção {i}", state="disabled")

    def votar(self, opcao):
        try:
            resultado = self.servico.registrar_voto(self.jogador, str(opcao))
            messagebox.showinfo("Voto", resultado)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível votar: {e}")

    def enviar_chat(self):
        msg = self.tela_jogo.TEntryChat.get().strip()
        if not msg:
            return
        try:
            self.servico.enviar_mensagem(self.jogador, msg)
            self.tela_jogo.TEntryChat.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível enviar mensagem: {e}")
