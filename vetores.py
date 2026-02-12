from langchain_community.embeddings import HuggingFaceEmbeddings

# 1. Inicializa o modelo (Cria o objeto/robô, não apenas o texto)
print("Carregando modelo neural local... (aguarde)")
modelo_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 2. Nosso texto de exemplo
texto = "Ministério da Defesa - Fundo do Exército - Valor: 76281.05"

# 3. Transformar em vetor (Agora vai funcionar porque 'modelo_embeddings' é um objeto)
vetor = modelo_embeddings.embed_query(texto)

# 4. Ver o resultado
print(f"\nTexto original: {texto}")
print(f"Tamanho do vetor: {len(vetor)} dimensões")
print(f"Primeiros 10 números do vetor: {vetor[:10]}...")