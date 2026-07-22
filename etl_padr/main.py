import schedule
import time

# IMPORTANTE: Puxa as funções criadas dentro dos arquivos da pasta /src
from src.pipeline import extrair_dados, transformar_dados, carregar_dados
from src.notificacoes import enviar_alerta

def rodar_pipeline_completo():
    """
    ROUTINA PRINCIPAL: Junta as 3 etapas (Extração, Tratamento e Carga).
    """
    print("\n⏰ --- INICIANDO EXECUÇÃO AUTOMÁTICA ---")
    try:
        # 1. Caminho da planilha de entrada (Altere conforme a necessidade)
        caminho_planilha = "dados/entrada.xlsx"
        
        # 2. String de conexão do Banco de Dados (Exemplo com SQLite local)
        # Para PostgreSQL use: "postgresql://usuario:senha@localhost:5432/nome_banco"
        banco_conexao = "sqlite:///banco_local.db" 
        
        # 3. Executa as 3 fases do ETL sequencialmente
        df_bruto = extrair_dados(caminho_planilha)
        df_limpo = transformar_dados(df_bruto)
        carregar_dados(df_limpo, tabela_destino="tb_vendas", string_conexao=banco_conexao)
        
        print("🎉 Processo rodou com sucesso!")
        
    except Exception as e:
        print(f"💥 Ocorreu uma falha no pipeline: {e}")
        # Descomente a linha abaixo para te enviar e-mail se der erro!
        # enviar_alerta("❌ ERRO NO ETL", f"Falha: {e}", "seu_email@empresa.com")


# ==============================================================================
# AGENDAMENTO DA AUTOMAÇÃO
# ==============================================================================

# Configura o script para rodar sozinho todos os dias às 08:00
schedule.every().day.at("08:00").do(rodar_pipeline_completo)

if __name__ == "__main__":
    print("🤖 Robô de ETL Ativo! Aguardando o horário programado...")
    
    # Roda uma primeira vez imediatamente ao abrir o terminal para testar
    rodar_pipeline_completo()
    
    # Loop infinito que mantém o programa rodando no terminal checando o relógio
    while True:
        schedule.run_pending() # Verifica se deu o horário agendado
        time.sleep(60)        # Espera 60 segundos antes de checar de novo