import threading
import time

def extrair_e_analisar_dados():
    while True:
        # Simula a extração e análise de dados
        print("Extraindo e analisando dados...")
        time.sleep(10)  # Simula um processo demorado

def monitorar_operacoes():
    while True:
        # Simula o monitoramento de operações
        print("Monitorando operações abertas...")
        time.sleep(1)  # Verifica a cada segundo

# Cria threads para as funções
thread_extracao = threading.Thread(target=extrair_e_analisar_dados)
thread_monitoramento = threading.Thread(target=monitorar_operacoes)

# Inicia as threads
thread_extracao.start()
thread_monitoramento.start()

# Aguarda as threads terminarem (nunca vão terminar neste exemplo)
thread_extracao.join()
thread_monitoramento.join()