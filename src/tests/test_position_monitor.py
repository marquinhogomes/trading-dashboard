import threading
import time

def extracao_e_analise():
    while True:
        print("Extraindo e analisando dados...")
        time.sleep(10)  # Simula um processo demorado

def monitoramento():
    while True:
        print("Monitorando operações...")
        time.sleep(2)  # Monitoramento mais frequente

# Criação das threads
thread_extracao = threading.Thread(target=extracao_e_analise)
thread_monitoramento = threading.Thread(target=monitoramento)

# Início das threads
thread_extracao.start()
thread_monitoramento.start()