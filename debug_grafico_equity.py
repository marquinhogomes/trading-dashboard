#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug do problema do gráfico de equity - linha verde (Balance)
Identifica por que a linha verde não reflete corretamente as operações fechadas
"""

import sys
import os
sys.path.append('.')

def debug_grafico_equity():
    """Debug do gráfico de equity"""
    print("🔍 DEBUG: Problema da linha verde (Balance) no gráfico de equity")
    print("=" * 70)
    
    print("\n📊 PROBLEMA IDENTIFICADO:")
    print("   A linha verde (Balance) não reflete corretamente as operações fechadas")
    print("   porque está usando o mesmo erro de lógica que já corrigimos:")
    print("   balance_inicial = balance_atual (ERRADO!)")
    
    print("\n🏦 CENÁRIO EXEMPLO:")
    print("   • Balance início do dia: R$ 10.000,00")
    print("   • Operação 1 fechada: -R$ 50,00 às 09:30")
    print("   • Operação 2 fechada: -R$ 83,00 às 11:15")
    print("   • Balance atual: R$ 9.867,00")
    print("   • Posições abertas: R$ 0,00 (nenhuma)")
    
    print("\n❌ LÓGICA ATUAL (PROBLEMÁTICA) - função obter_equity_historico_mt5:")
    print("   balance_inicial = balance_atual  # R$ 9.867,00 (ERRADO!)")
    print("   ")
    print("   Pontos gerados:")
    print("   Ponto 1 (início): Balance=9.867,00")
    print("   Ponto 2 (deal 1): Balance=9.817,00  # 9.867 + (-50)")
    print("   Ponto 3 (deal 2): Balance=9.784,00  # 9.867 + (-133)")
    print("   Ponto 4 (atual):  Balance=9.867,00")
    print("   ")
    print("   Resultado: Linha verde com valores INCORRETOS!")
    
    print("\n✅ LÓGICA CORRETA:")
    print("   # Deve usar a mesma função que corrigimos!")
    print("   balance_inicial = calcular_saldo_inicial_do_dia()  # R$ 10.000,00")
    print("   ")
    print("   Pontos corretos:")
    print("   Ponto 1 (início): Balance=10.000,00")
    print("   Ponto 2 (deal 1): Balance=9.950,00   # 10.000 + (-50)")
    print("   Ponto 3 (deal 2): Balance=9.867,00   # 10.000 + (-133)")
    print("   Ponto 4 (atual):  Balance=9.867,00")
    print("   ")
    print("   Resultado: Linha verde com valores CORRETOS!")
    
    print("\n🔧 CORREÇÃO NECESSÁRIA:")
    print("   1. Modificar obter_equity_historico_mt5()")
    print("   2. Usar sistema.calcular_saldo_inicial_do_dia()")
    print("   3. Aplicar a mesma lógica que já funciona no lucro diário")
    print("   4. Garantir que Balance reflita operações fechadas corretamente")

if __name__ == "__main__":
    debug_grafico_equity()
