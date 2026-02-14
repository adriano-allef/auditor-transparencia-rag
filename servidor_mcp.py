import os
from mcp.server.fastmcp import FastMCP

#Criamos o servidor MCP
mcp = FastMCP("Auditor")

@mcp.tool()
def guardar_relatorio(nome_fornecido:str, conteudo:str):
    """
    A função dessa ferramenta é salvar o seu relatório no computador local.
    """
    pasta_segura = "relatorios"
    
    #1. Sanitização (Sandboxing contra Path Traversal)
    nome_limpo = os.path.basename(nome_fornecido)
    caminho_final = os.path.join(pasta_segura, nome_limpo)

    #2. Garantir que a pasta existe (Idempotencia)
    os.makedirs(pasta_segura, exist_ok=True)

    #3. Escrita segura do ficheiro
    with open(caminho_final, 'w', encoding='utf-8') as ficheiro:
        ficheiro.write(conteudo)

    return f"🟩Sucesso! Relatório guardado em: {caminho_final}"

#3. Ligando o servidor
if __name__ == "__main__":
    mcp.run()

