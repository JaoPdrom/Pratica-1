import yaml

class MotorJogo:

    def __init__(self, arquivo_historia: str): #construtor da classe
        self.historia = self.carregar_historia(arquivo_historia) #armazena o arquivo yaml da historia
        self.trecho_atual = None #armazena o trecho atual da historia
        self.votos = {} #dicionario para armazenar os votos dos jogadores
        self.chat = [] #lista para armazenar as mensagens do chat

    def carregar_historia(self, arquivo: str) -> dict: #converte o arquivo yaml em dicionario
        try:
            with open(arquivo, 'r', encoding='utf-8') as arq_historia:
                return yaml.safe_load(arq_historia) #faz a conversao do arquivo yaml para dicionario
            
            if not isinstance(historia, dict): #verifica se o arquivo é um dicionario
                raise ValueError("O arquivo de história deve conter um dicionário YAML.")
            return historia
        
        except FileNotFoundError:   
            print(f"Erro: O arquivo {arquivo} não foi encontrado.")
            return {}
        except yaml.YAMLError as e:
            print(f"Erro ao carregar o arquivo YAML: {e}")
            return {}
        
    def iniciar_jogo(self):
        if not self.historia: #verifica se a historia foi carregada corretamente
            raise RuntimeError("História não carregada corretamente.")
        
        try:
            self.trecho_atual = next(iter(self.historia)) #pega o primeiro trecho da historia
        except StopIteration:
            raise RuntimeError("A história está vazia.")
        
        self.votos.clear() #limpa os votos
        self.chat.clear() #limpa o chat

    def obter_trecho_atual(self, formatado=True):
        if self.trecho_atual is None: #verifica se o jogo foi iniciado
            return "O jogo não foi iniciado."
        
        trecho = self.historia[self.trecho_atual] #pega o trecho atual da historia
        
        #define quais opções mostrar (todas ou só as empatadas)
        if hasattr(self, "opcoes_empate") and self.opcoes_empate: #verifica se tem empate
            opcoes_exibir = [] 
            for indice in self.opcoes_empate: #reinicia a votacao mostrando apenas as opcoes empatadas
                opcoes_exibir.append(trecho["opcoes"][indice - 1])
            modo_empate = True
        else:
            opcoes_exibir = trecho.get("opcoes", []) #mostra todas as opcoes normais sem empate
            modo_empate = False
            
            if not formatado:
                return {
                    "texto": trecho["texto"],
                    "opcoes": opcoes_exibir
                }
        
        texto = f"\n🧭 Trecho atual: {self.trecho_atual}\n"
        texto += f"{trecho['texto']}\n"

        if not opcoes_exibir: #finaliza a historia por nao ter opcoes
            texto += "\nFim da história\n"
            return texto

        if modo_empate: #se estiver em modo empate, avisa o jogador
            texto += "\nEmpate detectado! Vote novamente entre as opções abaixo:\n"
        else:
            texto += "\nOpções disponíveis:\n"

        contador = 1
        for opcao in opcoes_exibir:
            texto += f"  {contador}. {opcao['texto']}\n"
            contador += 1

        return texto
    
    def registrar_voto(self, jogador: str, opcao: int):
        if self.trecho_atual is None: #verifica se o jogo foi iniciado
            return "O jogo não foi iniciado."
        
        trecho = self.historia[self.trecho_atual] #pega o trecho atual
        if not trecho.get("opcoes"): #verifica se há opções
            return "Não há opções disponíveis neste trecho."

        if opcao < 1 or opcao > len(trecho["opcoes"]): #verifica se a opção é válida
            return "Opção inválida."

        self.votos[jogador] = opcao #registra o voto
        return f"Voto registrado: {jogador} votou na opção {opcao}." 
    
    def calcular_resultados(self):
        if not self.votos: #verifica se há votos registrados
            return "Nenhum voto registrado."

        contagem_votos = {}
        for voto in self.votos.values(): #conta os votos
            contagem_votos[voto] = contagem_votos.get(voto, 0) + 1 

        max_votos = max(contagem_votos.values()) #determina o número máximo de votos

        opcao_mais_votada = []
        for opcao, votos in contagem_votos.items(): #verifica se há empate
            if votos == max_votos:
                opcao_mais_votada.append(opcao)

        if len(opcao_mais_votada) > 1: #se houver empate, escolhe a primeira opção
            self.opcoes_empate = opcao_mais_votada
            trecho = self.historia[self.trecho_atual]

            texto_empate = "Houve um empate entre as opções:\n"
            texto_empate += "As opções mais votadas foram:\n"
            for i in self.opcoes_empate:
                texto_empate += f"  {i}. {trecho['opcoes'][i-1]['texto']}\n"
            self.votos.clear()
            return texto_empate

        opcao_vencedora = opcao_mais_votada[0] #se não houver empate, pega a opção vencedora
        trecho = self.historia[self.trecho_atual] #pega o trecho atual
        proximo_trecho = trecho["opcoes"][opcao_vencedora - 1]["proximo"] #determina o próximo trecho

        return self.avancar_historia(proximo_trecho)
    
    def avancar_historia(self, proximo_trecho: str):
        if proximo_trecho not in self.historia:
            return "Trecho inválido."

        self.trecho_atual = proximo_trecho
        self.votos.clear() #limpa os votos para o próximo trecho
        return f"Próximo trecho: {self.trecho_atual}"    
    
    def enviar_mensagem_chat(self, jogador: str, mensagem: str):
        if not mensagem.strip():
            return "Mensagem vazia não pode ser enviada."

        mensagem = f"{jogador}: {mensagem.strip()}"
        self.chat.append((jogador, mensagem))
        return f"{jogador} disse: {mensagem}"
    
    def obter_chat(self, formatado=True):
        if not self.chat:
            return "Nenhuma mensagem no chat"
        
        if formatado:
            texto = "\nChat atual:\n"
            for msg in self.chat:
                texto += f"  {msg}\n"
            return texto
        
        return self.chat