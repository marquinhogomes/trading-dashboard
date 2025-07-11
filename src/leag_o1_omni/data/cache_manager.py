import threading

def extrair_e_analisar_dados():
    # Código para extração e análise de dados
    pass

def monitorar_operacoes():
    # Código para monitoramento de lucros, breakeven, etc.
    pass

# Cria uma thread para a extração e análise de dados
thread_extracao = threading.Thread(target=extrair_e_analisar_dados)
thread_extracao.start()

# Executa o monitoramento na thread principal
monitorar_operacoes()