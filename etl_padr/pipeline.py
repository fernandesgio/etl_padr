import pandas as pd
from sqlalchemy import create_engine
import sys

def extrair_dados(caminho_excel, nome_aba=0):
    """
    ETAPA 1: EXTRAÇÃO (Extract)
    Carrega o arquivo Excel para a memória.
    """
    print("⏳ Carregando arquivo Excel...")
    try:
        # ALTERE AQUI: Se o Excel tiver senha ou aba específica, ajuste sheet_name
        df = pd.read_excel(caminho_excel, sheet_name=nome_aba)
        print(f"✅ Extração concluída! {len(df)} linhas carregadas.")
        return df
    except Exception as e:
        print(f"❌ Erro na extração: {e}")
        sys.exit(1)


def transformar_dados(df):
    """
    ETAPA 2: TRATAMENTO E LIMPEZA (Transform)
    Aplica as regras de negócio nos dados.
    """
    print("⏳ Iniciando tratamento dos dados...")
    
    # 1. Padronizar nomes das colunas (remove espaços, coloca em minúsculo)
    # Exemplo: " Data Venda " -> "data_venda"
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # 2. ALTERE AQUI: Remover linhas duplicadas
    df = df.drop_duplicates()
    
    # 3. ALTERE AQUI: Tratar valores nulos de colunas específicas
    # Exemplo: Preenche valores ausentes da coluna 'valor' com 0.0
    if 'valor' in df.columns:
        df['valor'] = df['valor'].fillna(0.0)
        
    # 4. ALTERE AQUI: Garantir tipagem correta
    # Exemplo: Converter coluna de data para o formato datetime
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
        # Criando o motor de conexão com o banco
        engine = create_engine(string_conexao)
        
        # ALTERE AQUI: if_exists pode ser:
        # 'append': Insere novos dados no final da tabela (mais comum)
        # 'replace': Apaga a tabela existente e recria do zero
        df.to_sql(
            name=tabela_destino, 
            con=engine, 
            if_exists='append', 
            index=False
        )
        print("🚀 Carga no Banco de Dados finalizada com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao carregar dados no banco: {e}")


# ==============================================================================
# 🎯 EXECUÇÃO PRINCIPAL (Altere os valores abaixo conforme sua necessidade)
# ==============================================================================
if __name__ == "__main__":
    
    # 1. ALTERE AQUI: Caminho do seu arquivo Excel
    CAMINHO_DO_EXCEL = "dados/entrada.xlsx"
    NOME_DA_ABA = 0  # 0 é a primeira aba. Pode colocar o nome: "Vendas"
    
    # 2. ALTERE AQUI: Nome da tabela de destino no seu banco de dados
    TABELA_BANCO = "tb_vendas_tratadas"
    
    # 3. ALTERE AQUI: String de conexão do seu Banco de Dados
    # Exemplo PostgreSQL: "postgresql://usuario:senha@localhost:5432/nome_do_banco"
    # Exemplo MySQL: "mysql+pymysql://usuario:senha@localhost:3306/nome_do_banco"
    # Exemplo SQLite (Local para testes): "sqlite:///meu_banco.db"
    STRING_CONEXAO = "sqlite:///banco_local.db"

    # Executando a esteira ETL
    df_bruto = extrair_dados(CAMINHO_DO_EXCEL, NOME_DA_ABA)
    df_limpo = transformar_dados(df_bruto)
    carregar_dados(df_limpo, TABELA_BANCO, STRING_CONEXAO)