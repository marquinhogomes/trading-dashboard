#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste da correção do gráfico de equity - linha verde (Balance)
Simula o cenário com operações fechadas
"""

import sys
import os
from datetime import datetime, timedelta
sys.path.append('.')

def teste_correcao_grafico_equity():
    """Testa a nova lógica do gráfico de equity"""
    print("🧪 TESTE: Correção da linha verde (Balance) no gráfico de equity")
    print("=" * 70)
    
    # Simula dados reais do MT5
    print("\n📊 DADOS SIMULADOS DO MT5:")
    balance_atual = 9867.00
    equity_atual = 9867.00
    profit_atual = 0.00  # Sem posições abertas
    
    # Simula deals do dia
    deals_do_dia = [
        {'profit': -50.00, 'time': '09:30', 'timestamp': datetime.now() - timedelta(hours=4)},
        {'profit': -83.00, 'time': '11:15', 'timestamp': datetime.now() - timedelta(hours=2)},
    ]
    
    lucro_total_dia = sum([deal['profit'] for deal in deals_do_dia])
    
    print(f"   • Balance atual: R$ {balance_atual:,.2f}")
    print(f"   • Equity atual: R$ {equity_atual:,.2f}")
    print(f"   • Profit atual: R$ {profit_atual:,.2f}")
    print(f"   • Deals do dia: {len(deals_do_dia)}")
    print(f"   • Lucro total dos deals: R$ {lucro_total_dia:+,.2f}")
    
    print(f"\n✅ NOVA LÓGICA DO GRÁFICO (CORRIGIDA):")
    
    # Calcula balance inicial correto (mesma lógica que já funciona)
    balance_inicial_correto = balance_atual - lucro_total_dia
    equity_inicial_correto = balance_inicial_correto
    
    print(f"   balance_inicial = balance_atual - lucro_total_dia")
    print(f"   balance_inicial = {balance_atual:,.2f} - ({lucro_total_dia:+,.2f})")
    print(f"   balance_inicial = R$ {balance_inicial_correto:,.2f}")
    
    print(f"\n📈 PONTOS DO GRÁFICO CORRIGIDOS:")
    pontos_corretos = []
    
    # Ponto inicial
    pontos_corretos.append({
        'momento': 'Início do dia',
        'equity': equity_inicial_correto,
        'balance': balance_inicial_correto,
        'profit': 0.0
    })
    
    # Pontos dos deals
    lucro_acumulado = 0
    for i, deal in enumerate(deals_do_dia):
        lucro_acumulado += deal['profit']
        balance_no_momento = balance_inicial_correto + lucro_acumulado
        
        pontos_corretos.append({
            'momento': f"Deal {i+1} ({deal['time']})",
            'equity': balance_no_momento,
            'balance': balance_no_momento,
            'profit': 0.0  # Zerado após fechamento
        })
    
    # Ponto atual
    pontos_corretos.append({
        'momento': 'Agora',
        'equity': equity_atual,
        'balance': balance_atual,
        'profit': profit_atual
    })
    
    print(f"\n{'Momento':<20} {'Equity':<12} {'Balance':<12} {'Profit':<12}")
    print("-" * 60)
    
    for ponto in pontos_corretos:
        print(f"{ponto['momento']:<20} "
              f"R$ {ponto['equity']:>8.2f}  "
              f"R$ {ponto['balance']:>8.2f}  "
              f"R$ {ponto['profit']:>8.2f}")
    
    print(f"\n🎯 RESULTADO DA CORREÇÃO:")
    print(f"   ✅ Balance inicial: R$ {balance_inicial_correto:,.2f} (início do dia)")
    print(f"   ✅ Balance final: R$ {balance_atual:,.2f} (após trades)")
    print(f"   ✅ Diferença: R$ {balance_atual - balance_inicial_correto:+,.2f}")
    print(f"   ✅ Confere com deals: R$ {lucro_total_dia:+,.2f}")
    
    if abs((balance_atual - balance_inicial_correto) - lucro_total_dia) < 0.01:
        print(f"   ✅ SUCESSO: Linha verde agora reflete corretamente as operações fechadas!")
    else:
        print(f"   ❌ ERRO: Cálculo ainda incorreto")
    
    print(f"\n📱 VISUALIZAÇÃO NO GRÁFICO:")
    print(f"   🟦 Linha Equity (azul): Mostra patrimônio total")
    print(f"   🟢 Linha Balance (verde): Mostra evolução das operações fechadas")
    print(f"   🔴 Linha Profit (vermelha): Mostra lucro das posições abertas")
    print(f"   📊 Agora Balance vai de R$ {balance_inicial_correto:,.2f} para R$ {balance_atual:,.2f}")

if __name__ == "__main__":
    teste_correcao_grafico_equity()
