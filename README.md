# Auditor de Transparência (RAG) 🕵️‍♂️🏛️

Este projeto utiliza IA Generativa e RAG (Retrieval-Augmented Generation) para auditar gastos públicos usando dados do Portal da Transparência. Ele transforma planilhas complexas em um chat inteligente.

## 🛠️ Pré-requisitos e Setup (Windows)

Antes de começar, certifique-se de seguir estes requisitos de infraestrutura:

1. **Python 3.12+**: 
   - *Atenção:* Evite versões Alpha/Preview (como 3.13 ou 3.14) devido a incompatibilidades de bibliotecas de IA.
   - *Importante:* Marque a opção **"Add Python to PATH"** durante a instalação.
2. **Microsoft Visual C++ Redistributable (x64)**: 
   - Essencial para rodar o PyTorch (motor da IA) no Windows.
   - [Download Oficial aqui](https://aka.ms/vs/17/release/vc_redist.x64.exe).

## 🚀 Instalação e Configuração

1. **Clone o repositório** (ou baixe a pasta do projeto).
2. **Crie o Ambiente Virtual**:
   ```bash
   python -m venv .venv
*Ative o Ambiente:*

No VS Code, abra um novo terminal (o prefixo (.venv) deve aparecer em verde).

*Instale as Dependências:*

O arquivo requirements.txt já está otimizado para a versão CPU (mais estável e leve).
    
    python -m pip install -r requirements.txt

**🔐 Configurando a Chave de IA (Google Gemini)
O "cérebro" do auditor funciona através da API do Google.**

Obtenha sua chave gratuita no Google AI Studio.

Na raiz do projeto, crie um arquivo chamado .env.

Adicione sua chave no arquivo:

    GOOGLE_API_KEY=SUA_CHAVE_AQUI_SEM_ASPAS
Nota: O arquivo .env está no .gitignore e nunca deve ser compartilhado.

**🏃‍♂️ Como Usar o Auditor:**

*O sistema funciona em um fluxo de dois passos:*

**Passo 1:** Ingestão de Dados
Converte o arquivo dados/despesas.csv em "conhecimento" para a IA. Rode sempre que atualizar os dados:

    python banco_vetorial.py
Passo 2: Conversar com o Auditor
Inicia o chat interativo no terminal:

    python app.py

**🐛 Troubleshooting (Erros Comuns)**

*Erro [WinError 1114] ou c10.dll: O sistema tentou usar a GPU sem suporte.*

Solução: Reinstale a versão CPU: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

*Erro UnicodeDecodeError: Dados do governo costumam usar encoding Latin-1.*

Solução: O código já trata isso, mas certifique-se de usar encoding='latin-1' no read_csv.

*Erro ModuleNotFoundError: No module named 'langchain.chains':*

Solução: Nas versões novas, use from langchain_classic.chains import RetrievalQA.


## 🧠 Diário de Bordo: O Mapa da Mina (Para o Adriano do Futuro)

Esta seção do documento explica como as peças desse quebra-cabeça se encaixam.

## 📖 O que diabos é RAG?
A IA (Gemini) é muito inteligente, mas ela não conhece os seus dados do Portal da Transparência. O **RAG** (Retrieval-Augmented Generation) resolve isso: em vez de pedir para a IA "adivinhar", a gente dá os documentos certos para ela ler e depois perguntamos sobre eles.

## 🏗️ A Arquitetura (O Caminho do Dado)

### 1. `main.py` (A Limpeza)
O primeiro passo. Ele usa a biblioteca `pandas` para ler o CSV bruto do governo. Ele limpa os dados, remove sujeira e garante que o Python consiga ler os valores de dinheiro e datas corretamente.

### 2. `banco_vetorial.py` (A Memória)
**Aqui é onde a mágica acontece.** - Ele transforma cada linha do CSV em uma frase legível.

- Ele usa um modelo local (`sentence-transformers`) para transformar essas frases em **Vetores** (listas de números que representam o significado da frase).
- Ele salva esses números na pasta `BANCO_VETORIAL` usando o **ChromaDB**. 
- *Por que vetores?* Porque é assim que a IA faz buscas por assunto e não apenas por palavras exatas.

### 3. `app.py` (O Cérebro)
É o programa final que você usa.
1. Você faz uma pergunta.
2. O programa busca no `BANCO_VETORIAL` os 5 trechos mais relevantes.
3. Ele envia esses 5 trechos + sua pergunta para o **Gemini** (Google).
4. O Gemini analisa tudo e te responde como se fosse um auditor humano.

## 🛡️ Regras de Ouro de Infraestrutura
- **Isolamento (`.venv`)**: Sempre use o ambiente virtual para as bibliotecas não bagunçarem seu Windows.
- **Segurança (`.env`)**: Suas chaves de API são secretas. Elas ficam no `.env` e o Git foi ensinado a ignorar esse arquivo.
- **Versão CPU**: IA pesada gosta de placa de vídeo (GPU), mas como estamos no notebook, forçamos tudo para rodar no processador (CPU) para evitar erros de DLL.

## ⚖️ Licença e Isenção de Responsabilidade

Este projeto é distribuído sob a **Licença Apache 2.0**. Ele foi desenvolvido com fins estritamente **didáticos** e para demonstração técnica de arquiteturas de **IA Agêntica**, **RAG** e **MCP**. 

O software é fornecido "como está" (*as is*), sem garantias de qualquer tipo, expressas ou implícitas. Dado que a ferramenta utiliza modelos probabilísticos (LLMs), o autor não se responsabiliza por eventuais alucinações, erros de análise ou pelo uso indevido das informações extraídas. A responsabilidade pelo uso ético dos dados e pela conformidade com as normas do Portal da Transparência é inteiramente do usuário.