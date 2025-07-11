import threading
import time

def extrair_e_analisar_dados():
    while True:
        # Simula a extração e análise de dados
        print("Extraindo e analisando dados...")
        time.sleep(5)  # Simula um processo demorado

def monitorar_operacoes():
    while True:
        # Simula o monitoramento de operações
        print("Monitorando operações abertas...")
        time.sleep(1)  # Monitoramento mais rápido

# Criação das threads
thread_extracao = threading.Thread(target=extrair_e_analisar_dados)
thread_monitoramento = threading.Thread(target=monitorar_operacoes)

# Iniciar as threads
thread_extracao.start()
thread_monitoramento.start()

# Juntar as threads (opcional, dependendo da lógica do seu programa)
thread_extracao.join()
thread_monitoramento.join()