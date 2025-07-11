#!/usr/bin/env python3
"""
Script de debug para verificar por que o gráfico de resultado acumulado não aparece
"""

import sys
import os
from datetime import datetime, timedelta
import MetaTrader5 as mt5

def debug_mt5_connection():
    """Testa conexão e dados do MT5"""
    print("🔍 INICIANDO DEBUG DO MT5...")
    
    # Tenta inicializar MT5
    if not mt5.initialize():
        print("❌ Falha ao inicializar MT5")
        print(f"Erro: {mt5.last_error()}")
        return False
    
    print("✅ MT5 inicializado com sucesso")
    
    # Informações da conta
    account_info = mt5.account_info()
    if account_info:
        print(f"📊 Conta: {account_info.login}")
        print(f"💰 Balance: R$ {account_info.balance:,.2f}")
        print(f"💰 Equity: R$ {account_info.equity:,.2f}")
    else:
        print("❌ Não foi possível obter informações da conta")
    
    # Testa busca de deals históricos
    data_inicio = datetime.now() - timedelta(days=30)
    data_fim = datetime.now()
    
    print(f"\n🔍 Buscando deals de {data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}")
    
    deals = mt5.history_deals_get(data_inicio, data_fim)
    
    if deals is None:
        print("❌ Nenhum deal encontrado (None)")
        return False
    
    print(f"📊 Total de deals encontrados: {len(deals)}")
    
    # Filtra deals com profit/loss (fechamentos)
    deals_com_resultado = [d for d in deals if d.profit != 0]
    print(f"💰 Deals com resultado (lucro/prejuízo): {len(deals_com_resultado)}")
    
    if len(deals_com_resultado) > 0:
        print("\n📋 Primeiros 5 deals com resultado:")
        for i, deal in enumerate(deals_com_resultado[:5]):
            data_deal = datetime.fromtimestamp(deal.time)
            print(f"  {i+1}. {deal.symbol} | {data_deal.strftime('%d/%m %H:%M')} | R$ {deal.profit:+.2f}")
    
    # Agrupa por data
    trades_por_dia = {}
    for deal in deals_com_resultado:
        data_deal = datetime.fromtimestamp(deal.time).date()
        if data_deal not in trades_por_dia:
            trades_por_dia[data_deal] = []
        trades_por_dia[data_deal].append(deal.profit)
    
    print(f"\n📅 Dias com trades: {len(trades_por_dia)}")
    if trades_por_dia:
        print("Resumo por dia:")
        for data, lucros in sorted(trades_por_dia.items()):
            total_dia = sum(lucros)
            print(f"  {data.strftime('%d/%m/%Y')}: {len(lucros)} trades, Total: R$ {total_dia:+.2f}")
    
    mt5.shutdown()
    return True

if __name__ == "__main__":
    debug_mt5_connection()
    input("\nPressione Enter para sair...")
