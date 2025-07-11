import threading
import time

def extracao_e_analise():
    while True:
        # Simula a extração e análise de dados
        print("Extraindo e analisando dados...")
        time.sleep(10)  # Simula um processo demorado

def monitoramento():
    while True:
        # Simula o monitoramento de lucros e operações
        print("Monitorando operações...")
        time.sleep(2)  # Monitoramento mais frequente

# Cria threads para cada função
thread_extracao = threading.Thread(target=extracao_e_analise)
thread_monitoramento = threading.Thread(target=monitoramento)

# Inicia as threads
thread_extracao.start()
thread_monitoramento.start()

# Aguarda as threads terminarem (nunca vão terminar neste exemplo)
thread_extracao.join()
thread_monitoramento.join()