# 🧭 Roadmap de Desenvolvimento — Jogo de Aventura Cooperativo (RPyC)

Este documento organiza as próximas etapas de desenvolvimento do projeto **Prática 1 - Sistemas Distribuídos (CC5SDT)**.  
Cada fase representa um conjunto de tarefas que devem ser concluídas antes de avançar para a próxima.

---

## 🧱 Fase 1 — Revisão e Estabilização do Código Atual
**Objetivo:** Garantir que a base atual (motor, servidor e cliente) funcione sem erros e com comunicação estável.

- [ ] Testar a conexão entre servidor e múltiplos clientes (mínimo 2).
- [ ] Corrigir erro `'int' object is not subscriptable'` (provável retorno incorreto do servidor).
- [ ] Corrigir erro `'Jogo' object has no attribute 'obter_trecho_atual'`.
- [ ] Garantir que o YAML da história é carregado sem falhas.
- [ ] Confirmar que o chat funciona para todos os jogadores conectados.
- [ ] Centralizar a lógica de votação e avanço de história **no servidor** (clientes só enviam votos).

---

## 🏗️ Fase 2 — Sistema de Pré-Jogo (Servidor)
**Objetivo:** Criar uma camada de “espera” antes do início da história, garantindo que todos os jogadores estejam prontos.

- [ ] Criar o módulo `prejogo.py` com a classe `PreJogo`.
- [ ] Adicionar atributos:
  - `jogadores_conectados: dict`
  - `max_jogadores: int` (ex.: 4)
  - `historia_validada: bool`
- [ ] Implementar métodos:
  - `registrar_jogador(nome, conn)`
  - `validar_historia(caminho)`
  - `todos_conectados() -> bool`
  - `iniciar_jogo() -> MotorJogo`
- [ ] Fazer o servidor criar e usar `PreJogo` antes do `MotorJogo`.
- [ ] Enviar atualizações do tipo “Aguardando jogadores (2/4)” para os clientes conectados.
- [ ] Iniciar o jogo automaticamente quando `todos_conectados()` for verdadeiro.

---

## 🖥️ Fase 3 — Telas de Pré-Jogo (Cliente GUI)
**Objetivo:** Criar a interface gráfica para o fluxo de entrada e espera.

- [ ] Criar tela de **inserção de nome**.
- [ ] Enviar o nome ao servidor via `exposed_registrar_jogador(nome)`.
- [ ] Criar tela de **espera**, mostrando quantos jogadores já estão conectados.
- [ ] Atualizar automaticamente conforme o servidor envia notificações.
- [ ] Quando o servidor enviar o sinal de “início”, trocar para a interface principal do jogo.

---

## ⚙️ Fase 4 — Integração do Pré-Jogo com o Motor
**Objetivo:** Garantir a transição suave entre o pré-jogo e o início da narrativa.

- [ ] Integrar `PreJogo` e `MotorJogo` no servidor.
- [ ] Validar o arquivo YAML antes de iniciar o motor.
- [ ] Enviar o trecho inicial e opções para todos os jogadores quando o jogo começar.
- [ ] Testar a inicialização completa com 2, 3 e 4 jogadores conectados.

---

## 🧩 Fase 5 — Refino da Lógica do Jogo
**Objetivo:** Corrigir e refinar o comportamento de votação, empate e sincronização.

- [ ] Corrigir avanço automático do cliente após votar (aguardar todos).
- [ ] Implementar verificação de empate no `MotorJogo`.
- [ ] Criar método de broadcast no servidor para enviar:
  - novo trecho,
  - resultado da votação,
  - estado de empate.
- [ ] Adicionar logs no servidor (quem entrou, votou, etc.).
- [ ] Testar estabilidade com múltiplos clientes simultâneos.

---

## 📊 Fase 6 — Testes e Entrega Final
**Objetivo:** Validar todo o sistema e preparar os arquivos exigidos pelo professor.

- [ ] Testar com 4 clientes conectados (simultaneamente).
- [ ] Confirmar que o chat continua ativo durante o jogo.
- [ ] Testar troca de YAML da história e reinício do servidor.
- [ ] Criar log simples de eventos do servidor.
- [ ] Testar comportamento quando um cliente desconecta no pré-jogo.
- [ ] Criar relatório final em PDF (tecnologia + capturas de tela + instruções).

---

## 🌟 Fase Extra (Melhorias Opcionais)
**Objetivo:** Adicionar valor e refinamento ao projeto.

- [ ] Persistir histórico do chat ou estado do jogo (SQLite ou arquivo texto).
- [ ] Adicionar botão **“Sair do jogo”** na GUI.
- [ ] Criar executável do cliente com **PyInstaller**.
- [ ] Melhorar design da GUI (cores, fontes, espaçamento).

---

## 🔗 Referências
- [Guia de Projeto - UTFPR](./Guia%20de%20Projeto%20Jogo%20de%20Aventura%20Co.txt)
- [Documentação RPyC](https://rpyc.readthedocs.io/en/latest/)
- [Relatório do Trabalho - CC5SDT](./trabalho-1-cc5sdt-2025-2.pdf)

---

> 💡 **Dica:** Use a aba *Projects* do GitHub para importar esta lista como um quadro Kanban  
> (Settings → Projects → Create project → Import from markdown).
