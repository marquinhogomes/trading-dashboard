import asyncio

async def extrair_e_analisar_dados():
    while True:
        # Simula a extração e análise de dados
        print("Extraindo e analisando dados...")
        await asyncio.sleep(5)  # Simula um tempo de processamento

async def monitorar_operacoes():
    while True:
        # Simula o monitoramento de operações
        print("Monitorando operações...")
        await asyncio.sleep(1)  # Monitoramento mais frequente

async def main():
    await asyncio.gather(
        extrair_e_analisar_dados(),
        monitorar_operacoes()
    )

# Executa o loop principal
asyncio.run(main())