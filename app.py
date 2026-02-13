import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_classic.chains import RetrievalQA

#1. Carrega as variáveis de ambiente (Sua chave de API)
load_dotenv()

#2. Configura o "Cérebro" (Gemini 1.5 Flash - rápido e gratuito)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)

#3. Carrega o "Conhecimento" (Seu banco vetorial que já criamos)
# CORREÇÃO 1: Faltou criar o modelo de embeddings antes de passar para o banco
modelo_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_db = Chroma(persist_directory="BANCO_VETORIAL", embedding_function=modelo_embeddings)

#4. Cria a "Corrente de Auditoria" (RAG Chain)
#O K=5 significa que ele vai buscar os 5 registros mais parecidos com sua pergunta
auditor = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_db.as_retriever(search_kwargs={"k": 5})
)

#5. Interface de chat no Terminal
print("🕵️‍♂️ Auditor de Transparência ativo! (Digite 'sair' para encerrar)")

while True:
    pergunta = input("\nVocê: ")

    # CORREÇÃO 2: Faltou comparar com a palavra 'sair'
    if pergunta.lower() == 'sair': #lower() transforma em minusculo
        break

    print("🧐 Analisando dados...")
    
    # CORREÇÃO 3: Era "run" com N no final
    resposta = auditor.run(pergunta)

    print(f"\n🤖 Auditor: {resposta}")