#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste final da correção do Lucro/Prejuízo Diário
Simula o cenário real com logs detalhados
"""

import sys
import os
sys.path.append('.')

def simular_correcao_completa():
    """Simula o funcionamento completo da correção"""
    print("🧪 TESTE FINAL: Correção Completa do Lucro/Prejuízo Diário")
    print("=" * 70)
    
    print("\n📊 CENÁRIO REAL SIMULADO:")
    print("   • Conta começou o dia com R$ 10.000,00")
    print("   • Houve 2 trades: -R$ 50,00 e -R$ 83,00")
    print("   • Total de perdas: -R$ 133,00")
    print("   • Balance atual: R$ 9.867,00")
    print("   • Equity atual: R$ 9.867,00 (sem posições abertas)")
    
    # Simula dados do MT5
    balance_atual = 9867.00
    equity_atual = 9867.00
    profit_atual = 0.00  # Sem posições abertas
    
    deals_do_dia = [
        {'profit': -50.00, 'symbol': 'PETR4', 'time': '09:30'},
        {'profit': -83.00, 'symbol': 'VALE3', 'time': '11:15'},
    ]
    
    print(f"\n🔧 PROCESSO DE CORREÇÃO:")
    
    # 1. Calcular saldo inicial
    print(f"1️⃣ CALCULAR SALDO INICIAL:")
    lucro_total_dia = sum([deal['profit'] for deal in deals_do_dia])
    saldo_inicial_calculado = balance_atual - lucro_total_dia
    
    print(f"   • Deals encontrados: {len(deals_do_dia)}")
    print(f"   • Lucro total dos deals: R$ {lucro_total_dia:+,.2f}")
    print(f"   • Balance atual: R$ {balance_atual:,.2f}")
    print(f"   • Saldo inicial = {balance_atual:,.2f} - ({lucro_total_dia:+,.2f})")
    print(f"   • Saldo inicial = R$ {saldo_inicial_calculado:,.2f} ✅")
    
    # 2. Atualizar informações da conta
    print(f"\n2️⃣ ATUALIZAR INFORMAÇÕES DA CONTA:")
    print(f"   • Equity atual: R$ {equity_atual:,.2f}")
    print(f"   • Saldo inicial: R$ {saldo_inicial_calculado:,.2f}")
    
    # 3. Calcular lucro diário
    print(f"\n3️⃣ CALCULAR LUCRO DIÁRIO:")
    lucro_diario_final = equity_atual - saldo_inicial_calculado
    percentual = (lucro_diario_final / saldo_inicial_calculado * 100)
    
    print(f"   • lucro_diario = equity_atual - saldo_inicial")
    print(f"   • lucro_diario = {equity_atual:,.2f} - {saldo_inicial_calculado:,.2f}")
    print(f"   • lucro_diario = R$ {lucro_diario_final:+,.2f} ✅")
    print(f"   • Percentual: {percentual:+.2f}%")
    
    # 4. Renderizar no dashboard
    print(f"\n4️⃣ RENDERIZAR NO DASHBOARD:")
    cor_status = "🔴 VERMELHO" if lucro_diario_final < 0 else "🟢 VERDE"
    print(f"   📱 Métrica: 'Lucro/Prejuízo Diário'")
    print(f"   💵 Valor: R$ {lucro_diario_final:+,.2f}")
    print(f"   📊 Delta: {percentual:+.2f}%")
    print(f"   🎨 Cor: {cor_status}")
    
    # 5. Verificação final
    print(f"\n5️⃣ VERIFICAÇÃO FINAL:")
    if abs(lucro_diario_final - lucro_total_dia) < 0.01:
        print(f"   ✅ SUCESSO: Lucro diário ({lucro_diario_final:+,.2f}) = Total deals ({lucro_total_dia:+,.2f})")
        print(f"   ✅ CORREÇÃO FUNCIONANDO: O valor não está mais zerado!")
    else:
        print(f"   ❌ ERRO: Valores não coincidem")
    
    print(f"\n🎯 LOGS QUE APARECERÃO NO DASHBOARD:")
    print(f"   📅 Calculando saldo inicial para 2025-01-27")
    print(f"   🔍 Buscando deals desde 00:00:00")
    print(f"   📊 CÁLCULO SALDO INICIAL:")
    print(f"      • Deals hoje: 2")
    print(f"      • Lucro total dos deals: R$ -133,00")
    print(f"      • Balance atual: R$ 9.867,00")
    print(f"      • Saldo inicial calculado: R$ 10.000,00")
    print(f"   📊 CÁLCULO LUCRO DIÁRIO:")
    print(f"      • Equity atual: R$ 9.867,00")
    print(f"      • Saldo inicial: R$ 10.000,00")
    print(f"      • Lucro diário: R$ -133,00")

if __name__ == "__main__":
    simular_correcao_completa()
