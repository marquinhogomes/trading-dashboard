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
        time.sleep(2)  # Verifica operações a cada 2 segundos

# Cria threads para execução paralela
thread_extracao = threading.Thread(target=extrair_e_analisar_dados)
thread_monitoramento = threading.Thread(target=monitorar_operacoes)

# Inicia as threads
thread_extracao.start()
thread_monitoramento.start()

# Aguarda as threads terminarem (neste caso, elas nunca terminam)
thread_extracao.join()
thread_monitoramento.join()