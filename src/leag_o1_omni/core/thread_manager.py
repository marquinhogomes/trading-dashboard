import threading
import time

def extrair_e_analisar_dados():
    # Simula a extração e análise de dados
    time.sleep(10)  # Simula um processo demorado
    print("Dados extraídos e analisados.")

def monitorar_lucros():
    while True:
        # Simula o monitoramento de lucros
        print("Monitorando lucros...")
        time.sleep(2)  # Verifica a cada 2 segundos

# Cria uma thread para a extração e análise de dados
thread_extracao = threading.Thread(target=extrair_e_analisar_dados)
thread_extracao.start()

# Inicia o monitoramento de lucros na thread principal
monitorar_lucros()