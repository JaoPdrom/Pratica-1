# Jogo Aventura Cooperativo

Aplicação em Python para uma **história interativa cooperativa** (choose-your-own-adventure) com votação e chat em tempo real.
Este repositório contém a versão local / de desenvolvimento (rodando no Windows). A versão final do trabalho deve ser enviada em um `.zip` contendo o código e o relatório em PDF.

---

## Estrutura sugerida do projeto

```
JogoAventuraCooperativo/
│
├── motor_jogo.py        # Lógica central do jogo (sem rede)
├── servidor.py          # Exporá a lógica via RPyC (mais tarde)
├── cliente.py           # Cliente TUI (mais tarde)
├── historia.yaml        # Arquivo da história interativa (YAML)
├── requirements.txt     # Dependências do projeto
├── README.md
└── .gitignore
```

---

## Pré-requisitos (Windows)

* Python 3.8+ instalado (recomendado 3.10 ou 3.11).
  Verifique com:

  ```powershell
  python --version
  ```
* Git (para versionamento / GitHub).
  Verifique com:

  ```powershell
  git --version
  ```
* VS Code (recomendado) e extensões úteis: *Python*, *Pylance*, *YAML*, *GitLens* (opcional).

---

## Passo a passo — configurar o projeto no Windows

1. **Clonar / criar o repositório**

   * Se já criou o repositório no GitHub:

     ```powershell
     git clone https://github.com/SEU_USUARIO/SEU_REPO.git
     cd SEU_REPO
     ```
   * Ou criar localmente:

     ```powershell
     mkdir JogoAventuraCooperativo
     cd JogoAventuraCooperativo
     git init
     ```

2. **Criar ambiente virtual**

   ```powershell
   python -m venv venv
   ```

3. **Ativar o ambiente virtual**

   * **PowerShell (recomendado no Windows):**

     ```powershell
     .\venv\Scripts\Activate.ps1
     ```

     Se der erro de execução, você pode:

     * usar o terminal `cmd.exe` (abaixo), ou
     * ajustar temporariamente a política de execução:

       ```powershell
       Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
       ```

       > Atenção: esse comando altera a política de execução para o usuário atual. Se preferir não alterar, rode o `activate` no `cmd` (próximo item).
   * **CMD (Prompt de Comando):**

     ```cmd
     venv\Scripts\activate.bat
     ```
   * **Git Bash / WSL** (se preferir bash):

     ```bash
     source venv/Scripts/activate
     ```

   Ao ativar, o prompt mostrará `(venv)`.

4. **Atualizar pip (opcional, recomendado)**

   ```powershell
   python -m pip install --upgrade pip
   ```

5. **Criar / verificar `requirements.txt`**
   Exemplo mínimo para começar:

   ```text
   rpyc
   pyyaml
   ```

   Instale as dependências:

   ```powershell
   pip install -r requirements.txt
   ```

---

## Configurar VS Code para o projeto

1. Abra a pasta no VS Code (`File → Open Folder...`).
2. Selecione o interpretador Python do `venv`:

   * `Ctrl+Shift+P` → `Python: Select Interpreter` → selecione `.\venv\Scripts\python.exe`.
3. Ative a opção de ativar o ambiente no terminal (geralmente o VS Code faz isso automaticamente).
4. (Opcional) criar `.vscode/settings.json` com:

   ```json
   {
     "python.defaultInterpreterPath": "${workspaceFolder}/venv/Scripts/python.exe",
     "python.terminal.activateEnvironment": true
   }
   ```
5. Extensões recomendadas: *Python*, *Pylance*, *YAML*, *GitLens*.

---

Se quiser, eu já crio os arquivos iniciais (stubs + `historia.yaml` + `.gitignore` + `requirements.txt`) e mostro os comandos para testar localmente. Quer que eu gere esses arquivos agora?
