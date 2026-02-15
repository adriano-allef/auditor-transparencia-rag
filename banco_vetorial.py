import pandas as pd
import glob
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
import os

#1. Configuração de Caminhos (Infraestrutura)
PASTA_DADOS = "dados"
PASTA_BANCO = "BANCO_VETORIAL" #Onde o Chroma vai salvar os arquivos

print("\n ⚙️ Iniciando a Pipeline de Ingestão de Dados em lote...\n")

#2. Varredura de Pasta (Busca TODOS os arquivos CSV)
arquivos_csv = glob.glob(os.path.join(PASTA_DADOS, "*.csv"))

#Proteção: Caso a pasta esteja vazia, encerra com aviso amigável
if not arquivos_csv:
    print(f"❌ Nenhum arquivo .csv encontrado na pasta '{PASTA_DADOS}'.")
    exit()

print(f"📂 Encontrados {len(arquivos_csv)} arquivos para processar.")

documentos = []

# 3. O loop de Processamento (Pasta arquivo por arquivo)
for arquivo in arquivos_csv:
    nome_arquivo = os.path.basename(arquivo)
    print(f" -> Lendo e higienizando dados de: {nome_arquivo}")

    #Lê o CSV atual
    df = pd.read_csv(arquivo, encoding='latin1', sep=';')

    # ===================================================================
    # DATA CLEANING (A sua lógica impecável do main.py)
    # ===================================================================
    #Garante que é texto, troca a vírgula por ponto (CORRIGIDO NOME DA COLUNA)
    df['VALOR TRANSAÇÃO'] = df['VALOR TRANSAÇÃO'].astype(str).str.replace(',','.')
    
    #Converte para número (errors='coerce' transforma erros/textos zoados em Vazio/NaN) (CORRIGIDO NOME DA COLUNA)
    df['VALOR TRANSAÇÃO'] = pd.to_numeric(df['VALOR TRANSAÇÃO'], errors='coerce')

    #Remove qualquer linha que tenha ficado sem valor após a conversão para não quebrar a IA
    df = df.dropna(subset=['VALOR TRANSAÇÃO'])

    # ===================================================================
    # ENGENHARIA DE PROMPT (Transformar tabela em vetor)
    # ===================================================================

    #A IA não lê tabelas bem. Ela lê texto. Vamos criar uma "história" para cada linha.
    #Ex.: "O órgão Ministério da Defesa gastou R$ 1000 com a empresa X"
    print("⚙️ Processando linhas para formato de IA...")

    # CORREÇÃO: Este loop agora está indentado para rodar DENTRO do loop de arquivos
    for index, linha in df.iterrows():
        #FOi criada uma string única com todas as informações importantes
        conteudo = (
            f"Defesa do orgão {linha['NOME ÓRGÃO SUPERIOR']} ({linha['NOME ÓRGÃO']}). "
            f"Data: {linha['DATA TRANSAÇÃO']}. "
            f"Valor: R$ {linha['VALOR TRANSAÇÃO']}. "
            f"Favorecido: {linha['NOME FAVORECIDO']}."
        )
        
        #Foi criado o objeto Document (O padrão que o LangChain aceita)
        #metadata serve para filtros futuros (ex: filtrar só ano 2024)
        doc = Document(
            page_content=conteudo,
            #O 'metadata' agora guarda de qual mês veio a informação!
            metadata={"origem": nome_arquivo, "linha": index}
        )
        documentos.append(doc)

#Limitando para teste (Opcional: Se o PC for lento, descomente a linha abaixo para testar apenas com 100 linhas)
# documentos = documentos[:100]

print(f"\n📄 Total de documentos processados: {len(documentos)}")

#4. Inicializar a IA (Embeddings)
print("🧠 Carregando modelo neural.local...")
modelo_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

#5. Criar/Atualizar o Banco de Dados (Ingestão)
#Se a pasta já existir, ele carrega. Se não, ele cria.

print("💾 Ingerindo no ChromaDB (Isso pode demorar um pouco)...")
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