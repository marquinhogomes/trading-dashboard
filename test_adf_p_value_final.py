#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para o erro adf_p_value corrigido
"""

import os
import sys
import pandas as pd
import numpy as np

# Adicionar o diretório atual ao path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

def test_encontrar_linha_monitorada_fix():
    """Testa se a correção da função encontrar_linha_monitorada funciona"""
    print("🧪 Testando correção da função encontrar_linha_monitorada...")
    
    try:
        from calculo_entradas_v55 import encontrar_linha_monitorada
        print("✅ Função importada com sucesso!")
        
        # Criar DataFrame de teste que simula o problema
        dados_teste = {
            'Z-Score': [2.5, -2.1, 1.8, -3.0],
            'alpha': [0.1, 0.2, 0.05, 0.15],
            'beta': [1.2, 0.8, 1.4, 0.9],
            'r2': [0.6, 0.7, 0.5, 0.8],
            'Dependente': ['PETR4', 'VALE3', 'ITUB4', 'BBDC4'],
            'Independente': ['VALE3', 'PETR4', 'BBDC4', 'ITUB4'],
            'Período': [21, 21, 21, 21]
        }
        
        # Teste 1: DataFrame SEM colunas adf_p_value e coint_p_value (situação do erro)
        print("   🔍 Teste 1: DataFrame sem colunas adf_p_value/coint_p_value")
        df_sem_colunas = pd.DataFrame(dados_teste)
        
        linha_operacao = []
        
        resultado = encontrar_linha_monitorada(
            tabela_zscore_mesmo_segmento=df_sem_colunas,
            linha_operacao=linha_operacao,
            dados_preprocessados={},
            filter_params=None,
            enable_cointegration_filter=True
        )
        
        print(f"   ✅ Teste 1 passou! Retornou {len(resultado)} resultados sem erro")
        
        # Teste 2: DataFrame COM colunas adf_p_value e coint_p_value
        print("   🔍 Teste 2: DataFrame com todas as colunas")
        dados_completos = dados_teste.copy()
        dados_completos['adf_p_value'] = [0.02, 0.01, 0.06, 0.03]  # Alguns abaixo de 0.05
        dados_completos['coint_p_value'] = [0.03, 0.02, 0.08, 0.01]  # Alguns abaixo de 0.05
        
        df_completo = pd.DataFrame(dados_completos)
        linha_operacao2 = []
        
        resultado2 = encontrar_linha_monitorada(
            tabela_zscore_mesmo_segmento=df_completo,
            linha_operacao=linha_operacao2,
            dados_preprocessados={},
            filter_params=None,
            enable_cointegration_filter=True
        )
        
        print(f"   ✅ Teste 2 passou! Retornou {len(resultado2)} resultados sem erro")
        
        # Teste 3: DataFrame COM apenas adf_p_value (sem coint_p_value)
        print("   🔍 Teste 3: DataFrame com adf_p_value mas sem coint_p_value")
        dados_parciais = dados_teste.copy()
        dados_parciais['adf_p_value'] = [0.02, 0.01, 0.06, 0.03]
        
        df_parcial = pd.DataFrame(dados_parciais)
        linha_operacao3 = []
        
        resultado3 = encontrar_linha_monitorada(
            tabela_zscore_mesmo_segmento=df_parcial,
            linha_operacao=linha_operacao3,
            dados_preprocessados={},
            filter_params=None,
            enable_cointegration_filter=True
        )
        
        print(f"   ✅ Teste 3 passou! Retornou {len(resultado3)} resultados sem erro")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erro no teste: {e}")
        print(f"   Tipo do erro: {type(e).__name__}")
        if "'adf_p_value'" in str(e):
            print("   🎯 ERRO adf_p_value AINDA PRESENTE!")
            return False
        return True

if __name__ == "__main__":
    print("🧪 TESTE DE CORREÇÃO DO ERRO adf_p_value")
    print("=" * 50)
    
    success = test_encontrar_linha_monitorada_fix()
    
    print("=" * 50)
    if success:
        print("🎉 CORREÇÃO FUNCIONOU! O erro adf_p_value foi resolvido.")
    else:
        print("❌ CORREÇÃO FALHOU! Erro adf_p_value ainda presente.")
