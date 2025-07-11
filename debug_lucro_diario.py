#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug do cálculo de Lucro/Prejuízo Diário
Analisa por que o valor está zerado quando deveria mostrar -R$ 133,00
"""

import sys
import os
sys.path.append('.')

def debug_lucro_diario():
    """Debug do cálculo de lucro diário"""
    print("🔍 DEBUG: Problema do Lucro/Prejuízo Diário zerado")
    print("=" * 60)
    
    print("\n📊 SITUAÇÃO ATUAL:")
    print("   • MT5 mostra perda de R$ 133,00 hoje")
    print("   • Dashboard mostra R$ 0,00")
    print("   • Problema: saldo_inicial incorreto")
    
    print("\n❌ PROBLEMA IDENTIFICADO:")
    print("   O saldo_inicial está sendo definido como o balance ATUAL")
    print("   no momento da conexão, e não o balance do INÍCIO DO DIA")
    
    print("\n🏦 CENÁRIO EXEMPLO:")
    print("   • Balance início do dia: R$ 10.000,00")
    print("   • Trades do dia: -R$ 133,00")
    print("   • Balance atual: R$ 9.867,00")
    print("   • Equity atual: R$ 9.867,00 (sem posições abertas)")
    
    print("\n📝 LÓGICA ATUAL (PROBLEMÁTICA):")
    print("   saldo_inicial = balance_atual  # R$ 9.867,00 (ERRADO!)")
    print("   lucro_diario = equity_atual - saldo_inicial")
    print("   lucro_diario = 9.867,00 - 9.867,00 = 0,00  # ZERO!")
    
    print("\n✅ LÓGICA CORRETA:")
    print("   saldo_inicial = balance_inicio_do_dia  # R$ 10.000,00")
    print("   lucro_diario = equity_atual - saldo_inicial")
    print("   lucro_diario = 9.867,00 - 10.000,00 = -133,00  # CORRETO!")
    
    print("\n🔧 SOLUÇÕES PROPOSTAS:")
    print("   1. Usar histórico de deals para calcular balance inicial")
    print("   2. Armazenar balance do primeiro login do dia")
    print("   3. Usar arquivo saldo_inicial.json (como no sistema original)")
    print("   4. Calcular com base no profit total do dia")

if __name__ == "__main__":
    debug_lucro_diario()
