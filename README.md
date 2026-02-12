# Auditor de Transparência (RAG) 🕵️‍♂️🏛️

Este projeto utiliza IA Generativa e RAG (Retrieval-Augmented Generation) para auditar gastos públicos usando dados do Portal da Transparência.

## 🛠️ Pré-requisitos (Windows)

Antes de começar, certifique-se de ter instalado:

1.  **Python 3.12+** (Evite versões Alpha/Preview como 3.13/3.14 por incompatibilidade de bibliotecas).
    * *Importante:* Marcar "Add Python to PATH" na instalação.
2.  **Microsoft Visual C++ Redistributable (x64)**
    * Necessário para rodar o PyTorch/TensorFlow no Windows.
    * [Download Oficial](https://aka.ms/vs/17/release/vc_redist.x64.exe)

## 🚀 Instalação e Configuração

1.  **Clone o repositório** (ou baixe a pasta).
2.  **Crie o Ambiente Virtual**:
    ```bash
    python -m venv .venv
    ```
3.  **Ative o Ambiente**:
    * No VS Code, abra um novo terminal (o `.venv` deve aparecer verde).
4.  **Instale as Dependências**:
    * *Nota:* O arquivo `requirements.txt` já está configurado para baixar a versão CPU do PyTorch (mais leve).
    ```bash
    python -m pip install -r requirements.txt
    ```

## 🐛 Troubleshooting (Erros Comuns)

### Erro: `[WinError 1114] DLL load failed` ou `OSError: ... c10.dll`
Isso acontece quando o PyTorch tenta carregar bibliotecas de GPU ou faltam dependências do Windows.
**Solução:**
1.  Instale o Visual C++ Redistributable (link acima).
2.  Force a reinstalação da versão CPU do PyTorch:
    ```bash
    pip uninstall torch torchvision torchaudio -y
    pip install torch torchvision torchaudio --index-url [https://download.pytorch.org/whl/cpu](https://download.pytorch.org/whl/cpu)
    ```

### Erro: `UnicodeDecodeError` ao ler CSV
Os dados do governo brasileiro geralmente usam encoding `Latin-1` (ISO-8859-1) e separador `;`.
**Solução:**
Use sempre: `pd.read_csv(arquivo, encoding='latin-1', sep=';')`