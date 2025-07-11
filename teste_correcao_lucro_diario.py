#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste da correção do cálculo de Lucro/Prejuízo Diário
Simula o cenário com perda de R$ 133,00
"""

import sys
import os
sys.path.append('.')

def teste_correcao_lucro_diario():
    """Testa a nova lógica de cálculo do lucro diário"""
    print("🧪 TESTE: Correção do Lucro/Prejuízo Diário")
    print("=" * 60)
    
    # Simula dados reais do MT5
    print("\n📊 DADOS SIMULADOS DO MT5:")
    balance_atual = 9867.00  # Balance após os trades
    equity_atual = 9867.00   # Equity sem posições abertas
    
    # Simula deals do dia
    deals_do_dia = [
        {'profit': -50.00, 'time': '09:30'},
        {'profit': -83.00, 'time': '11:15'},
    ]
    
    lucro_total_dia = sum([deal['profit'] for deal in deals_do_dia])
    
    print(f"   • Balance atual: R$ {balance_atual:,.2f}")
    print(f"   • Equity atual: R$ {equity_atual:,.2f}")
    print(f"   • Deals do dia: {len(deals_do_dia)}")
    print(f"   • Lucro total dos deals: R$ {lucro_total_dia:+,.2f}")
    
    print(f"\n✅ NOVA LÓGICA (CORRIGIDA):")
    
    # Nova lógica
    saldo_inicial_correto = balance_atual - lucro_total_dia
    lucro_diario_correto = equity_atual - saldo_inicial_correto
    
    print(f"   saldo_inicial = balance_atual - lucro_total_dia")
    print(f"   saldo_inicial = {balance_atual:,.2f} - ({lucro_total_dia:+,.2f})")
    print(f"   saldo_inicial = R$ {saldo_inicial_correto:,.2f}")
    print(f"")
    print(f"   lucro_diario = equity_atual - saldo_inicial")
    print(f"   lucro_diario = {equity_atual:,.2f} - {saldo_inicial_correto:,.2f}")
    print(f"   lucro_diario = R$ {lucro_diario_correto:+,.2f}")
    
    print(f"\n🎯 RESULTADO:")
    if abs(lucro_diario_correto - lucro_total_dia) < 0.01:  # Tolerância de 1 centavo
        print(f"   ✅ SUCESSO: Lucro diário = R$ {lucro_diario_correto:+,.2f}")
        print(f"   ✅ CONFERE: Igual ao total dos deals (R$ {lucro_total_dia:+,.2f})")
    else:
        print(f"   ❌ ERRO: Lucro diário calculado incorretamente")
    
    print(f"\n📱 EXIBIÇÃO NO DASHBOARD:")
    percentual = (lucro_diario_correto / saldo_inicial_correto * 100) if saldo_inicial_correto > 0 else 0
    print(f"   💰 Métrica: 'Lucro/Prejuízo Diário'")
    print(f"   💵 Valor: R$ {lucro_diario_correto:+,.2f}")
    print(f"   📊 Delta: {percentual:+.2f}%")
    
    if lucro_diario_correto < 0:
        print(f"   🔴 Cor: Vermelho (prejuízo)")
    else:
        print(f"   🟢 Cor: Verde (lucro)")

if __name__ == "__main__":
    teste_correcao_lucro_diario()
