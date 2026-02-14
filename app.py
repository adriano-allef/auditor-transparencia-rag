import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# =======================================================================
# NOVOS IMPORTS: O PADRÃO LANGCHAIN V1.0
# =======================================================================
from langchain_core.tools import tool, create_retriever_tool
# 🚨 A grande mudança está aqui: Usamos o novo 'create_agent'
from langchain.agents import create_agent

load_dotenv()

#1. Configura o "Cérebro"
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

#2. Conecta ao "Conhecimento" (Banco Vetorial)
modelo_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_db = Chroma(persist_directory="BANCO_VETORIAL", embedding_function=modelo_embeddings)
retriever = vector_db.as_retriever(search_kwargs={"k": 5})

# =======================================================================
# CRIAÇÃO DAS FERRAMENTAS (OS "BRAÇOS" DA IA)
# =======================================================================

#FERRAMENTA 1: A Lupa
ferramenta_busca = create_retriever_tool(
    retriever,
    name="buscar_dados_transparencia",
    description="Busca informações financeiras e gastos públicos no banco de dados. Use esta ferramenta ANTES de responder qualquer pergunta sobre os dados."
)

# FERRAMENTA 2: A Impressora
@tool
def guardar_relatorio(nome_arquivo: str, conteudo: str) -> str:
    """
    Salva um relatório no disco local do computador.
    Parâmetros:
    - nome_arquivo: O nome do arquivo a ser salvo (ex: fraude_cafe.txt). IMPORTANTE: inclua a extensão .txt.
    - conteudo: O texto completo do relatório detalhando o problema.
    """
    pasta_segura = "relatorios"
    caminho_final = os.path.join(pasta_segura, nome_arquivo)
    
    os.makedirs(pasta_segura, exist_ok=True)
    
    with open(caminho_final, 'w', encoding='utf-8') as ficheiro:
        ficheiro.write(conteudo)
        
    return f"SUCESSO: Arquivo {nome_arquivo} foi salvo fisicamente na pasta {pasta_segura}!"

ferramentas = [ferramenta_busca, guardar_relatorio]

# =======================================================================
# CONFIGURAÇÃO DO AGENTE (O NOVO MOTOR V1.0)
# =======================================================================

regras_sistema = """Você é um Auditor Sênior de Contas Públicas. 
Você tem ferramentas para buscar dados e para salvar relatórios.
REGRA 1: SEMPRE use a ferramenta 'buscar_dados_transparencia' antes de responder.
REGRA 2: Se encontrar anomalias ou gastos excessivos, crie um resumo técnico e SEMPRE use a ferramenta 'guardar_relatorio' para salvá-lo."""

# 🚨 Criamos o robô com a sintaxe super limpa da versão v1.0
auditor_autonomo = create_agent(
    model=llm, 
    tools=ferramentas, 
    system_prompt=regras_sistema
)

# =======================================================================
# EXECUÇÃO DO PROGRAMA (O CHAT)
# =======================================================================

print("\n🕵️‍♂️ Auditor Autônomo ativo! (Digite 'sair' para encerrar)")

while True:
    pergunta = input("\nVocê: ")

    if pergunta.lower() == 'sair': 
        print("Encerrando sistema. Até logo!")
        break

    print("🧐 Analisando e tomando decisões...\n")
    
    # O padrão do LangChain agora é receber uma lista de mensagens
    resposta = auditor_autonomo.invoke({"messages": [("user", pergunta)]})

    # A resposta final da IA é a última mensagem do histórico
    # Pegamos a resposta bruta
    conteudo_bruto = resposta['messages'][-1].content
    
    # Se a API do Gemini devolver uma lista com assinaturas de segurança, extraímos só o texto
    if isinstance(conteudo_bruto, list):
        texto_limpo = conteudo_bruto[0].get('text', '')
    else:
        texto_limpo = conteudo_bruto # Se já for texto puro, segue o jogo

    print(f"\n🤖 Auditor: {texto_limpo}")