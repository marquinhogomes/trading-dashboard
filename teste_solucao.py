#!/usr/bin/env python3
"""
Teste da solução para o problema do filtro ADF
"""

import MetaTrader5 as mt5
import pandas as pd
from dashboard_trading_pro_real import TradingSystemReal

def testar_solucao():
    """Testa a solução com a função modificada"""
    
    print("🔧 TESTE DA SOLUÇÃO - FILTRO ADF DESABILITADO")
    print("=" * 60)
    
    # Inicializar sistema
    trading_system = TradingSystemReal()
    
    if not trading_system.conectar_mt5():
        print("❌ Falha ao conectar MT5")
        return
    
    # Configuração de teste
    config = {
        'ativos_selecionados': ['PETR4', 'VALE3', 'BBAS3'],
        'timeframe': '1 dia',
        'periodo_analise': 50,
        'filtro_zscore': False,
        'filtro_r2': False,
        'filtro_beta': False,
        'filtro_cointegração': False
    }
    
    print("🚀 Executando análise com filtro ADF desabilitado...")
    
    # Executa análise
    trading_system.executar_analise_real(config)
    
    # Verifica resultados
    print(f"\n📊 RESULTADOS:")
    print(f"Sinais ativos encontrados: {len(trading_system.sinais_ativos)}")
    
    if trading_system.sinais_ativos:
        print("✅ SUCESSO! Pares válidos encontrados:")
        for i, sinal in enumerate(trading_system.sinais_ativos[:5]):  # Mostra primeiros 5
            print(f"  {i+1}. {sinal['par']}: Z-Score={sinal['zscore']:.3f}, R²={sinal['r2']:.3f}")
    else:
        print("❌ Ainda não encontrou pares válidos")
    
    # Mostra últimos logs
    print(f"\n📋 ÚLTIMOS LOGS:")
    for log in trading_system.logs[-10:]:
        print(log)
    
    mt5.shutdown()

if __name__ == "__main__":
    testar_solucao()
