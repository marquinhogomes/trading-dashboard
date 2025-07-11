import asyncio

async def extrair_e_analisar_dados():
    # Simula a extração e análise de dados
    await asyncio.sleep(5)  # Simula um atraso
    print("Dados extraídos e analisados.")

async def monitorar_operacoes():
    while True:
        # Simula o monitoramento de operações
        print("Monitorando operações abertas...")
        await asyncio.sleep(1)  # Verifica a cada segundo

async def main():
    # Executa as duas funções em paralelo
    await asyncio.gather(
        extrair_e_analisar_dados(),
        monitorar_operacoes()
    )

# Executa o loop principal
asyncio.run(main())