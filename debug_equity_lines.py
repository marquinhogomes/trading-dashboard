#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug das linhas do gráfico de equity
Analisa os dados para identificar por que as linhas estão sobrepostas
"""

import sys
import os
sys.path.append('.')

def debug_equity_function():
    """Debug da função obter_equity_historico_mt5"""
    print("🔍 DEBUG: Análise das linhas do gráfico de equity")
    print("=" * 60)
    
    # Simula dados como se fossem do MT5
    print("\n1. SIMULAÇÃO DE DADOS MT5:")
    print("   • Equity atual: R$ 10.500,00")
    print("   • Balance atual: R$ 10.000,00")
    print("   • Profit atual: +R$ 500,00")
    print("   • Deals com lucros: +R$ 300, +R$ 200")
    
    # Simula a lógica atual da função
    equity_atual = 10500.0
    balance_atual = 10000.0
    profit_atual = 500.0
    
    deals_lucros = [300.0, 200.0]  # Total: 500
    lucro_total_deals = sum(deals_lucros)
    
    print(f"\n2. CÁLCULO ATUAL (PROBLEMÁTICO):")
    print(f"   • Lucro total dos deals: R$ {lucro_total_deals:,.2f}")
    
    # Lógica atual (problemática)
    equity_inicial_atual = equity_atual - lucro_total_deals
    balance_inicial_atual = balance_atual - lucro_total_deals
    
    print(f"   • Equity inicial calculado: R$ {equity_inicial_atual:,.2f}")
    print(f"   • Balance inicial calculado: R$ {balance_inicial_atual:,.2f}")
    
    # Mostra os pontos gerados pela lógica atual
    print(f"\n3. PONTOS GERADOS (LÓGICA ATUAL):")
    pontos_atuais = []
    
    # Ponto inicial
    pontos_atuais.append({
        'equity': equity_inicial_atual,
        'balance': balance_inicial_atual,
        'profit': 0.0
    })
    
    # Pontos dos deals
    lucro_acumulado = 0
    for deal in deals_lucros:
        lucro_acumulado += deal
        pontos_atuais.append({
            'equity': equity_inicial_atual + lucro_acumulado,
            'balance': balance_inicial_atual + lucro_acumulado,  # PROBLEMA AQUI!
            'profit': lucro_acumulado
        })
    
    # Ponto atual
    pontos_atuais.append({
        'equity': equity_atual,
        'balance': balance_atual,
        'profit': profit_atual
    })
    
    for i, ponto in enumerate(pontos_atuais):
        print(f"   Ponto {i+1}: Equity={ponto['equity']:,.2f}, Balance={ponto['balance']:,.2f}, Profit={ponto['profit']:,.2f}")
    
    print(f"\n❌ PROBLEMA IDENTIFICADO:")
    print(f"   As linhas ficam sobrepostas porque o balance está sendo calculado")
    print(f"   como 'balance_inicial + lucro_acumulado', quando deveria ser")
    print(f"   o balance real reportado pelo MT5!")
    
    print(f"\n4. CORREÇÃO PROPOSTA:")
    print(f"   • Equity: Patrimônio total (saldo + lucro das posições abertas)")
    print(f"   • Balance: Saldo realizado (apenas trades fechados)")
    print(f"   • Profit: Lucro das posições abertas")
    print(f"   • Equity = Balance + Profit")
    
    # Lógica corrigida
    print(f"\n5. PONTOS CORRIGIDOS:")
    pontos_corrigidos = []
    
    # Para uma correção adequada, precisamos saber o balance histórico
    # Como não temos, vamos usar uma aproximação melhor
    
    # Ponto inicial
    balance_inicial_correto = balance_atual  # Balance não muda com profit
    equity_inicial_correto = balance_inicial_correto
    
    pontos_corrigidos.append({
        'equity': equity_inicial_correto,
        'balance': balance_inicial_correto,
        'profit': 0.0
    })
    
    # Pontos intermediários
    lucro_acumulado = 0
    for deal in deals_lucros:
        lucro_acumulado += deal
        # Balance só muda quando trade é fechado (realizando lucro)
        balance_no_momento = balance_inicial_correto + lucro_acumulado
        pontos_corrigidos.append({
            'equity': balance_no_momento,  # Se não há posições abertas
            'balance': balance_no_momento,
            'profit': 0.0  # Profit zerado após fechamento
        })
    
    # Ponto atual (com posições abertas)
    pontos_corrigidos.append({
        'equity': equity_atual,
        'balance': balance_atual,
        'profit': profit_atual
    })
    
    for i, ponto in enumerate(pontos_corrigidos):
        print(f"   Ponto {i+1}: Equity={ponto['equity']:,.2f}, Balance={ponto['balance']:,.2f}, Profit={ponto['profit']:,.2f}")
    
    print(f"\n✅ AGORA AS LINHAS SERÃO DIFERENTES:")
    print(f"   • Linha Equity: Mostra o patrimônio total")
    print(f"   • Linha Balance: Mostra apenas os lucros realizados")
    print(f"   • A diferença entre elas mostra o profit das posições abertas")

if __name__ == "__main__":
    debug_equity_function()
