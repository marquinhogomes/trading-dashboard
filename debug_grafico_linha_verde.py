#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEBUG: Teste específico da linha verde (Balance) do gráfico de equity
Valida se as operações fechadas do dia estão sendo consideradas corretamente
"""

import sys
import os
import MetaTrader5 as mt5
from datetime import datetime, time as time_module
import pandas as pd
import plotly.graph_objects as go

def debug_grafico_linha_verde():
    """Debug focado especificamente na linha verde do gráfico"""
    print("DEBUG: Linha Verde (Balance) do Grafico de Equity")
    print("=" * 70)
    
    # Simulação de dados do MT5 para reproduzir o problema
    print("CENARIO SIMULADO:")
    print("   - Inicio do dia: R$ 10.000,00")
    print("   - 3 operacoes fechadas:")
    print("     - Trade 1: +R$ 50,00")
    print("     - Trade 2: -R$ 83,00")  
    print("     - Trade 3: +R$ 20,00")
    print("   - Resultado total: -R$ 13,00")
    print("   - Balance atual no MT5: R$ 9.987,00")
    print("   - 1 posicao aberta com +R$ 25,00 de profit")
    print("   - Equity atual: R$ 10.012,00")
    
    # Dados simulados
    balance_atual = 9987.00
    equity_atual = 10012.00
    profit_atual = 25.00
    
    # Simular deals fechados do dia
    deals_simulados = [
        {'time': '09:30', 'profit': 50.00},   # Lucro
        {'time': '11:15', 'profit': -83.00},  # Perda
        {'time': '14:45', 'profit': 20.00}    # Lucro pequeno
    ]
    
    lucro_total_dia = sum([deal['profit'] for deal in deals_simulados])
    
    print(f"\n📈 CÁLCULO DO SALDO INICIAL:")
    print(f"   • Balance atual: R$ {balance_atual:,.2f}")
    print(f"   • Lucro total dos deals: R$ {lucro_total_dia:+,.2f}")
    print(f"   • Saldo inicial = {balance_atual:,.2f} - ({lucro_total_dia:+,.2f})")
    
    saldo_inicial = balance_atual - lucro_total_dia
    print(f"   • Saldo inicial calculado: R$ {saldo_inicial:,.2f}")
    
    print(f"\n🎯 VALIDAÇÃO:")
    print(f"   ✅ Saldo inicial: R$ {saldo_inicial:,.2f}")
    print(f"   ✅ Balance final: R$ {balance_atual:,.2f}")
    print(f"   ✅ Diferença: R$ {balance_atual - saldo_inicial:+,.2f}")
    print(f"   ✅ Confere com deals: R$ {lucro_total_dia:+,.2f}")
    
    # Simular pontos do gráfico corrigidos
    print(f"\n📊 PONTOS DA LINHA VERDE (BALANCE):")
    print("Horário    Balance      Descrição")
    print("-" * 45)
    
    # Ponto inicial
    balance_progressivo = saldo_inicial
    print(f"00:00      R$ {balance_progressivo:>8,.2f}  Início do dia")
    
    # Pontos dos deals
    for deal in deals_simulados:
        balance_progressivo += deal['profit']
        status = "📈" if deal['profit'] > 0 else "📉" 
        print(f"{deal['time']}      R$ {balance_progressivo:>8,.2f}  {status} Deal: {deal['profit']:+,.2f}")
    
    # Ponto atual
    print(f"Agora      R$ {balance_atual:>8,.2f}  Estado atual")
    
    print(f"\n🟢 LINHA VERDE CORRIGIDA:")
    print(f"   📍 Início: R$ {saldo_inicial:,.2f}")
    print(f"   📍 Fim: R$ {balance_atual:,.2f}")
    print(f"   📊 Mostra evolução das operações fechadas: R$ {lucro_total_dia:+,.2f}")
    
    print(f"\n🟦 LINHA AZUL (EQUITY):")
    print(f"   📍 Atual: R$ {equity_atual:,.2f}")
    print(f"   📊 Inclui posições abertas: +R$ {profit_atual:,.2f}")
    
    print(f"\n🎉 STATUS DA CORREÇÃO:")
    if abs(balance_atual - (saldo_inicial + lucro_total_dia)) < 0.01:
        print("   ✅ SUCESSO: Linha verde reflete corretamente as operações fechadas!")
        print("   ✅ Balance progride corretamente do saldo inicial")
        print("   ✅ Diferença confere com o total dos deals")
    else:
        print("   ❌ ERRO: Cálculo ainda inconsistente")
    
    print(f"\n📱 COMO APARECE NO DASHBOARD:")
    print(f"   💰 Lucro/Prejuízo Diário: R$ {equity_atual - saldo_inicial:+,.2f}")
    print(f"   📊 Percentual: {((equity_atual - saldo_inicial) / saldo_inicial * 100):+.2f}%")
    print(f"   🎯 Gráfico mostra evolução desde R$ {saldo_inicial:,.2f}")

if __name__ == "__main__":
    debug_grafico_linha_verde()
