import pandas as pd
import glob
import os

def consolidar_pasta_excel(caminho_pasta):
    """
    FUNÇÃO AUXILIAR: Junta vários arquivos Excel de uma pasta em uma única tabela.
    """
    print("📂 Lendo todos os arquivos da pasta...")
    
    # glob.glob busca todos os arquivos que terminam com .xlsx na pasta indicada
    arquivos = glob.glob(os.path.join(caminho_pasta, "*.xlsx"))
    
    lista_dfs = [] # Lista vazia para guardar cada tabela lida
    
    for arquivo in arquivos:
        print(f"📄 Lendo: {arquivo}")
        df = pd.read_excel(arquivo)
        
        # Cria uma coluna informando de qual arquivo veio aquela linha (ótimo para auditagem)
        df['arquivo_origem'] = os.path.basename(arquivo)
        
        # Adiciona a tabela lida dentro da lista
        lista_dfs.append(df)
        
    if lista_dfs:
        # pd.concat junta todas as tabelas da lista em uma única tabela gigante
        df_final = pd.concat(lista_dfs, ignore_index=True)
        print(f"✅ Consolidação pronta! Total de {len(df_final)} linhas combinadas.")
        return df_final
    else:
        print("⚠️ Nenhum arquivo .xlsx foi encontrado na pasta.")
        return pd.DataFrame()