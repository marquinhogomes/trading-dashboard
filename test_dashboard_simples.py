#!/usr/bin/env python3
"""
Teste da função executar_analise_real_simples
"""

import MetaTrader5 as mt5
from dashboard_trading_pro_real import TradingSystemReal

def main():
    # Cria sistema de trading
    trading_system = TradingSystemReal()
    
    # Conecta ao MT5
    if not trading_system.conectar_mt5():
        print("❌ Falha ao conectar MT5")
        return    # Configuração de teste com valores originais rigorosos
    config = {
        'timeframe': '1 dia',
        'periodos_analise': [70, 100, 120, 140, 160, 180, 200, 220, 240, 250],  # Múltiplos períodos
        'filtro_zscore': True,      # Valores originais
        'filtro_r2': True,          # Valores originais
        'filtro_beta': True,        # Valores originais
        'filtro_cointegração': True, # Valores originais
        'zscore_min': 2.0,          # Valores originais
        'zscore_max': 2.0,          # Valores originais
        'r2_min': 0.50,             # Valores originais (50%)
        'ativos_selecionados': ['PETR4', 'VALE3', 'BBAS3', 'ITUB4', 'ABEV3']  # Poucos ativos para teste
    }
    
    print("🧪 Executando teste com FILTROS ORIGINAIS RIGOROSOS...")
    
    # Executa teste
    trading_system.executar_analise_real(config)
    
    # Mostra logs
    print("\n📋 LOGS:")
    for log in trading_system.logs[-20:]:  # Últimos 20 logs
        print(log)

if __name__ == "__main__":
    main()
