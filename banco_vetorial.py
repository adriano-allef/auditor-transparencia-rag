import pandas as pd
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
import os

#1. Configuração de Caminhos (Boas práticas de Infra)
ARQUIVOS_DADOS = "dados/despesas.csv"
PASTA_BANCO = "BANCO_VETORIAL" #Onde o Chroma vai salvar os arquivos

#2. Carregar e limpar os Dados (Reciclando a lógica do main.py)
print("📂 Lendo arquivo CSV...")
df = pd.read_csv(ARQUIVOS_DADOS, encoding='latin-1', sep=';')

#3. Engenharia de Prompt (Transformar tabela em Texto)
#A IA não lê tabelas bem. Ela lê texto. Vamos criar uma "história" para cada linha.
#Ex.: "O órgão Ministério da Defesa gastou R$ 1000 com a empresa X"
print("⚙️ Processando linhas para formato de IA...")

documentos = []
for index, linha in df.iterrows():
    #Criamos uma string única com todas as informações importantes
    conteudo = f"Defesa do orgão {linha['NOME ÓRGÃO SUPERIOR']} ({linha['NOME ÓRGÃO']})."\
        f"Data: {linha['DATA TRANSAÇÃO']}. " \
        f"Valor: R$ {linha['VALOR TRANSAÇÃO']}. " \
        f"Favorecido: {linha['NOME FAVORECIDO']}."
    
    #Criamos o objeto Document (O padrão que o LangChain aceita)
    #metadata serve para filtros futuros (ex: filtrar só ano 2024)
    doc = Document(
        page_content=conteudo,
        metadata={"origem": "portal_transparencia", "linha": index}
    )
    documentos.append(doc)

#Limitando para teste (Opcional: Se o PC for lendo, descomente a linha abaixo para testar apenas com 100 linhas)

# documentos = documentos[:100]

print(f"📄 Total de documentos processados: {len(documentos)}")

#4. Inicializar a IA (Embeddings)
print("🧠 Carregando modelo neural...")
modelo_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

#5. Criar/Atualizar o Banco de Dados (Ingestão)
#Se a pasta já existir, ele carrega. se não ele cria.

print("💾 Salvando no ChromaDB (Isso pode demorar um pouco)...")
db = Chroma.from_documents(
    documents=documentos,embedding=modelo_embeddings,persist_directory=PASTA_BANCO
)

print("✅ Sucesso! Banco vetorial criado na pasta 'banco_vetorial'")

#6. Teste Rápido (Sanity Check)
print("\n🔍 Testando busca: 'gastos do exército'")
resultado = db.similarity_search("gastos do exército com suprimentos", k=3)

for i, doc in enumerate(resultado):
    print(f"\n--- Resultado {i+1} ---")
    print(doc.page_content)