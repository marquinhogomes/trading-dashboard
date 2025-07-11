#!/usr/bin/env python3
"""
Teste simples para verificar se o MT5 está coletando dados
"""

import MetaTrader5 as mt5
import pandas as pd

# Inicializa MT5
if not mt5.initialize():
    print("❌ Falha ao inicializar MT5")
    exit()

# Testa um símbolo específico
simbolo = 'PETR4'
rates = mt5.copy_rates_from_pos(simbolo, mt5.TIMEFRAME_D1, 0, 10)

if rates is not None and len(rates) > 0:
    print(f"✅ {simbolo}: {len(rates)} registros coletados")
    df = pd.DataFrame(rates)
    print(f"📊 Primeiros valores de close: {df['close'].head().tolist()}")
else:
    print(f"❌ {simbolo}: Sem dados")

# Fecha MT5
mt5.shutdown()
