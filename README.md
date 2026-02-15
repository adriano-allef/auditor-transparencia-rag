# Auditor de Transparência Autônomo (RAG + Agentic AI) 🕵️‍♂️🏛️

Este projeto utiliza Inteligência Artificial Generativa e arquiteturas modernas de **RAG** (Retrieval-Augmented Generation) e **Agentic AI** para auditar gastos públicos usando dados do Portal da Transparência. 

Ele **age de forma autônoma**, analisando planilhas complexas e utilizando ferramentas locais para salvar relatórios de auditoria no sistema operacional de forma segura.

> **⚠️ Nota de Escopo:** Atualmente, o sistema está calibrado para ler exclusivamente os dados da seção **"CARTÃO DE PAGAMENTOS -> Cartão de Pagamento do Governo Federal (CPGF)"** (disponíveis no [Portal da Transparência](https://portaldatransparencia.gov.br/download-de-dados/cpgf)). Em breve, a pipeline de dados será expandida para processar outras categorias de despesas públicas.

## 🛠️ Pré-requisitos e Setup (Windows)

Antes de começar, certifique-se de seguir estes requisitos de infraestrutura:

1. **Python 3.12+**: 
   - *Atenção:* Evite versões Alpha/Preview (como 3.13 ou 3.14) devido a incompatibilidades de bibliotecas de IA.
   - *Importante:* Marque a opção **"Add Python to PATH"** durante a instalação.
2. **Microsoft Visual C++ Redistributable (x64)**: 
   - Essencial para rodar o PyTorch (motor local de embeddings) no Windows.
   - [Download Oficial aqui](https://aka.ms/vs/17/release/vc_redist.x64.exe).

## 🚀 Instalação e Configuração

1. **Clone o repositório** (ou baixe a pasta do projeto).
2. **Crie o Ambiente Virtual**:
   ```bash
   python -m venv .venv
   ```

3. Ative o Ambiente:
No VS Code, abra um novo terminal (o prefixo (.venv) deve aparecer em verde).

4. Instale as Dependências:
O arquivo requirements.txt já está otimizado para a versão CPU e inclui o ecossistema atualizado do LangChain v1.0 e LangGraph.
   ```bash
   pip install -U -r requirements.txt
   ```

**🔐 Configurando a Chave de IA (Google Gemini)
O "cérebro" do auditor funciona através da API do Google Gemini.**

1. Obtenha sua chave gratuita no Google AI Studio.
2. Na raiz do projeto, crie um arquivo chamado .env.
3. Adicione sua chave no arquivo:

   ```bash
   GOOGLE_API_KEY=SUA_CHAVE_AQUI_SEM_ASPAS
   ```

- *Nota de Segurança:* O arquivo .env está listado no .gitignore e nunca deve ser versionado.

**🏃‍♂️ Como Usar o Auditor Autônomo:**

O sistema funciona em um fluxo de dois passos:


- Passo 1: Ingestão de Dados em Lote (Pipeline)
Você pode colocar múltiplos arquivos .csv do Portal da Transparência dentro da pasta dados/. O sistema varre a pasta, processa tudo em lote e recria a memória vetorial para evitar duplicatas. Rode sempre que adicionar ou remover arquivos:
   ```bash
   python banco_vetorial.py
   ```

- Passo 2: Iniciar a Sessão de Auditoria
Inicia o Agente de IA interativo no terminal:
   ```bash
   python app.py
   ```

*Teste sugerido; Peça ao auditor para: "Encontrar os 3 maiores gastos e salvar um relatório detalhado no computador."*

## 🧠 Diário de Bordo: O Mapa da Arquitetura (Para o Adriano do Futuro)

Esta seção documenta a evolução arquitetural do projeto, saindo de um simples Chatbot para um Agente Autônomo.

## 📖 O que é RAG + Tool Calling?

- A IA (Gemini) não tem acesso nativo aos dados do Portal da Transparência nem ao nosso disco rígido.

- O RAG (Retrieval-Augmented Generation) dá à IA a capacidade de "ler" os nossos documentos de forma semântica.

- O Tool Calling (Uso de Ferramentas) dá à IA "braços", permitindo que ela decida, por conta própria, executar as funções escritas em Python (como gravar um arquivo) baseada no que ela leu.

### 🏗️ A Arquitetura em 3 Camadas
1. **banco_vetorial.py** (A Ingestão e Memória)

- Processamento em Lote: Usa glob para varrer a pasta dados/ e processar múltiplos CSVs automaticamente.

- Fonte Única da Verdade: Usa shutil para apagar o banco antigo antes de criar um novo, garantindo que não existam dados duplicados (Idempotência).
- Usa a biblioteca pandas para ler e higienizar o CSV bruto do governo.

- Transforma cada linha (gasto) em uma string semântica.

- Usa o modelo local sentence-transformers para converter os textos em Embeddings (vetores matemáticos).

- Armazena os embeddings no ChromaDB local. Isso permite buscas por significado (ex: "fraude", "exagero"), não apenas por palavras-chave exatas.

2. **As Ferramentas** (@tool) (Os Braços Seguros)

Implementamos funções Python que a IA pode acionar sob demanda:

- **buscar_dados_transparencia:** Uma ferramenta de Retriever que permite à IA pesquisar no ChromaDB.

- **guardar_relatorio:** Uma função com Sandboxing (isolamento) que obriga a IA a salvar arquivos .txt apenas dentro da pasta protegida relatorios/.

3. **app.py** (O Cérebro Autônomo - LangChain v1.0)

A aplicação evoluiu do obsoleto RetrievalQA para a arquitetura estado da arte baseada em grafos do LangChain v1.0.

Utilizei a função create_agent para instanciar o Gemini.

O Agente recebe um **System Prompt** rigoroso (comportamento de Auditor) e a lista de Ferramentas disponíveis.

- **Fluxo de Decisão:** A IA recebe a pergunta em formato de lista de mensagens, decide sozinha se precisa buscar dados no banco, lê o contexto retornado e, se encontrar anomalias, aciona a ferramenta de gravação local de forma 100% autônoma antes de responder ao usuário.

## 🐛 Troubleshooting e Lições Aprendidas
Erro [WinError 1114] ou c10.dll: O sistema tentou usar aceleração de GPU sem suporte no Windows.
Solução de Infra: Forçar a instalação da versão CPU do PyTorch:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

Erro ImportError: cannot import name 'AgentExecutor': A arquitetura do LangChain mudou radicalmente na versão 1.0, depreciando o AgentExecutor em favor do ecossistema LangGraph.
Solução Arquitetural: Refatorar o código para usar o novo padrão enxuto create_agent importado de langchain.agents, que gerencia o estado da IA nativamente.

Respostas Sujas do Gemini (com 'signature' e chaves de dicionário): As novas políticas de segurança da API retornam blocos de dados estruturados e assinados ao usar ferramentas.
Solução de Código: Implementar um parser no output **(resposta['messages'][-1].content)** para extrair apenas o valor da chave text quando a API retornar uma lista.

## 🛡️ Princípios de Infraestrutura Aplicados
- Isolamento de Ambiente (.venv): Prevenção de conflito de dependências no SO.

- Gestão de Segredos (.env e .gitignore): Prevenção de vazamento de credenciais.

- Infraestrutura como Código (requirements.txt): Garantia de reprodutibilidade do ambiente especificando o ecossistema completo do LangChain para evitar quebras de versão entre submódulos.

## ⚖️ Licença e Isenção de Responsabilidade

Este projeto é distribuído sob a **Licença Apache 2.0**. Ele foi desenvolvido com fins estritamente **didáticos** e para demonstração técnica de arquiteturas de **IA Agêntica**, **RAG** e **MCP**. 

O software é fornecido "como está" (*as is*), sem garantias de qualquer tipo, expressas ou implícitas. Dado que a ferramenta utiliza modelos probabilísticos (LLMs), o autor não se responsabiliza por eventuais alucinações, erros de análise ou pelo uso indevido das informações extraídas. A responsabilidade pelo uso ético dos dados e pela conformidade com as normas do Portal da Transparência é inteiramente do usuário.