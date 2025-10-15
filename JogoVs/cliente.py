import rpyc
import os
import time

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

def exibir_menu():
    print("\n=== MENU PRINCIPAL ===")
    print("1. Ver trecho atual")
    print("2. Votar em uma opção")
    print("3. Calcular resultado da votação")
    print("4. Ver chat")
    print("5. Enviar mensagem")
    print("6. Reiniciar jogo (admin/teste)")
    print("0. Sair")
    print("=======================")

def main():
    limpar_tela()
    print("🎮 Conectando ao servidor RPyC...")

    try:
        conn = rpyc.connect("localhost", 18861)
        jogo = conn.root
        print("✅ Conexão estabelecida com sucesso!")
    except Exception as e:
        print(f"❌ Falha ao conectar ao servidor: {e}")
        return

    jogador = input("\nDigite seu nome de jogador: ").strip()
    if not jogador:
        jogador = "JogadorAnonimo"

    # Entrar no jogo
    mensagem_inicial = jogo.entrar_no_jogo(jogador)
    print(mensagem_inicial)
    input("\nPressione ENTER para continuar...")

    while True:
        limpar_tela()
        print("=== JOGO DE AVENTURA COOPERATIVO ===\n")
        trecho = jogo.obter_trecho()
        print(trecho)
        jogo.confirmar_leitura(jogador)  # confirma que jogador leu o trecho
        print("\n====================================")
        exibir_menu()

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            limpar_tela()
            trecho = jogo.obter_trecho()
            print(trecho)
            jogo.confirmar_leitura(jogador)
            input("\nPressione ENTER para continuar...")

        elif opcao == "2":
            limpar_tela()
            print(jogo.obter_trecho())
            try:
                num_opcao = int(input("\nDigite o número da opção escolhida: "))
                resposta = jogo.registrar_voto(jogador, num_opcao)
                print(resposta)
            except ValueError:
                print("Entrada inválida. Digite um número.")
            input("\nPressione ENTER para continuar...")

        elif opcao == "3":
            limpar_tela()
            print("🗳️ Calculando resultado da votação...\n")
            print(jogo.calcular_resultados())
            input("\nPressione ENTER para continuar...")

        elif opcao == "4":
            limpar_tela()
            print(jogo.obter_chat())
            input("\nPressione ENTER para continuar...")

        elif opcao == "5":
            limpar_tela()
            msg = input("Digite sua mensagem: ").strip()
            if msg:
                print(jogo.enviar_mensagem(jogador, msg))
            else:
                print("Mensagem vazia não enviada.")
            input("\nPressione ENTER para continuar...")

        elif opcao == "6":
            limpar_tela()
            confirmar = input("Tem certeza que deseja reiniciar o jogo? (s/n): ").lower()
            if confirmar == "s":
                print(jogo.reiniciar_jogo())
            input("\nPressione ENTER para continuar...")

        elif opcao == "0":
            print("👋 Saindo do jogo...")
            break

        else:
            print("Opção inválida. Tente novamente.")
            time.sleep(1)

    conn.close()

if __name__ == "__main__":
    main()
