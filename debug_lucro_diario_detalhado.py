#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug ESPECÍFICO do Lucro/Prejuízo Diário ainda zerado
Verifica se a função está sendo chamada e os valores atualizados
"""

import sys
import os
sys.path.append('.')

def debug_lucro_diario_detalhado():
    """Debug detalhado da persistência do problema"""
    print("🔍 DEBUG DETALHADO: Lucro/Prejuízo Diário ainda zerado")
    print("=" * 70)
    
    print("\n🤔 POSSÍVEIS CAUSAS DO PROBLEMA PERSISTIR:")
    print("1. ❌ Função atualizar_account_info() não está sendo chamada")
    print("2. ❌ Saldo inicial não está sendo calculado corretamente")
    print("3. ❌ dados_sistema['lucro_diario'] não está sendo atualizado")
    print("4. ❌ render_status_cards não está lendo dados_sistema")
    print("5. ❌ atualizar_account_info está sendo sobrescrita")
    
    print("\n🔧 VERIFICAÇÕES NECESSÁRIAS:")
    print("   ✓ 1. Verificar se calcular_saldo_inicial_do_dia() está funcionando")
    print("   ✓ 2. Verificar se atualizar_account_info() está sendo chamada")
    print("   ✓ 3. Verificar se dados_sistema['saldo_inicial'] está correto")
    print("   ✓ 4. Verificar se dados_sistema['lucro_diario'] está sendo atualizado")
    print("   ✓ 5. Adicionar logs de debug em pontos críticos")
    
    print("\n💡 HIPÓTESE PRINCIPAL:")
    print("   A função atualizar_account_info() pode não estar sendo chamada")
    print("   automaticamente, ou o saldo_inicial ainda está sendo")
    print("   definido como balance atual em outro lugar.")
    
    print("\n🚀 PLANO DE CORREÇÃO:")
    print("   1. Adicionar logs de debug detalhados")
    print("   2. Forçar chamada de atualizar_account_info() em render_status_cards")
    print("   3. Verificar se há sobrescrita dos dados")
    print("   4. Garantir que o cálculo seja feito sempre que necessário")

if __name__ == "__main__":
    debug_lucro_diario_detalhado()
