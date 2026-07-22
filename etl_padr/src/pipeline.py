import pandas as pd
from sqlalchemy import create_engine

def extrair_dados(caminho_excel, nome_aba=0):
    """
    ETAPA 1: EXTRAÇÃO (Extract)
    Carrega o arquivo Excel para a memória.
    """
    print("⏳ Carregando arquivo Excel...")
    try:
        df = pd.read_excel(caminho_excel, sheet_name=nome_aba)
        print(f"✅ Extração concluída! {len(df)} linhas carregadas.")
        return df
    except Exception as e:
        print(f"❌ Erro na extração: {e}")
        raise e  # Lança o erro para o main.py capturar e enviar o e-mail de alerta!


def transformar_dados(df):
    """
    ETAPA 2: TRATAMENTO E LIMPEZA (Transform)
    Aplica as regras de negócio nos dados.
    """
    print("⏳ Iniciando tratamento dos dados...")
    
    # 1. Padronizar nomes das colunas
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # 2. Remover linhas duplicadas
    df = df.drop_duplicates()
    
    # 3. Tratar valores nulos
    if 'valor' in df.columns:
        df['valor'] = df['valor'].fillna(0.0)
        
    # 4. Garantir tipagem de data
    if 'data' in df.columns:
        df['data'] = pd.to_datetime(df['data'], errors='coerce')
        
    print("✅ Tratamento concluído com sucesso!")
    return df


def carregar_dados(df, tabela_destino, string_conexao):
    """
    ETAPA 3: CARGA (Load)
    Conecta no Banco de Dados e insere os dados tratados.
    """
    print(f"⏳ Conectando ao Banco de Dados e inserindo na tabela '{tabela_destino}'...")
    try:
        engine = create_engine(string_conexao)
        df.to_sql(
            name=tabela_destino, 
            con=engine, 
            if_exists='append', 
            index=False
        )
        print("🚀 Carga no Banco de Dados finalizada com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao carregar dados no banco: {e}")
        raise e


# ==============================================================================
# 🎯 BLOCO DE TESTE INDIVIDUAL (Roda apenas se você executar este arquivo direto)
# ==============================================================================
if __name__ == "__main__":
    CAMINHO_DO_EXCEL = "dados/entrada.xlsx"
    NOME_DA_ABA = 0
    TABELA_BANCO = "tb_vendas_tratadas"
    STRING_CONEXAO = "sqlite:///banco_local.db"

    df_bruto = extrair_dados(CAMINHO_DO_EXCEL, NOME_DA_ABA)
    df_limpo = transformar_dados(df_bruto)
    carregar_dados(df_limpo, TABELA_BANCO, STRING_CONEXAO)