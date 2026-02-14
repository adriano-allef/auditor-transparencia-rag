import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_classic.chains import RetrievalQA
# 1. Novos Imports do MCP
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

#Carrega as variáveis de ambiente (Sua chave de API)
load_dotenv()

# =======================================================================
# CONFIGURAÇÕES DO SERVIDOR LOCAL (MCP)
# =======================================================================
# Aqui o app.py prepara o comando para ligar os "braços" (servidor_mcp.py)

paramentros_servidor = StdioServerParameters(
    command="python",
    args=["servidor_mcp.py"]
)

regras_auditor = """Você é um Auditor Sênior de Contas Públicas.
Sempre que encontrar algo suspeito ou uma anomalia de gastos, crie um resumo técnico detalhando o problema e use a ferramenta 'guardar_relatorio' para salvar esse resumo no disco local."""

# =======================================================================
# CONFIGURAÇÕES DA IA E BANCO VETORIAL
# =======================================================================

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)#temperatura baixa, queremos precisão técnica

#Carrega o modelo embeddings
modelo_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

#Conecta ao "conhecimento (O banco de dados vetorial que já foi criado)"
vector_db = Chroma(persist_directory="BANCO_VETORIAL", embedding_function=modelo_embeddings)

# Cria a "Corrente de Auditoria" (RAG Chain)
auditor = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_db.as_retriever(search_kwargs={"k": 5})
)

# =======================================================================
# EXECUÇÃO DO PROGRAMA (CHAMADA E RESPOSTA)
# =======================================================================

print("🕵️‍♂️ Auditor de Transparência ativo! (Digite 'sair' para encerrar)")
print("🔌 Conectando aos dados e preparando ferramentas locais...\n")

while True:
    pergunta = input("\nVocê: ")

    if pergunta.lower() == 'sair':
        print("Encerrando sistema. Até logo!")
        break

    print("🧐 Analisando dados no banco vetorial...")
    
    # INJEÇÃO: Juntamos as regras do auditor com a pergunta que você digitou

    pergunta_com_regras = f"{regras_auditor}\n\nPergunta do usuário: {pergunta}"

    # Executamos a análise
    resposta = auditor.run(pergunta)

    print(f"\n🤖 Auditor: {resposta}")