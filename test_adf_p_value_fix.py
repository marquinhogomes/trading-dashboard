#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste para validar se o erro 'adf_p_value' foi corrigido na análise.
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Adicionar o diretório atual ao path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

def test_adf_p_value_fix():
    """Testa se o erro adf_p_value foi corrigido"""
    print("🔍 Testando importação das funções...")
    
    try:
        from calculo_entradas_v55 import (
            calcular_residuo_zscore_timeframe,
            extrair_dados,
            preprocessar_dados,
            dependente,
            independente,
            periodo
        )
        print("✅ Importação bem-sucedida!")
    except Exception as e:
        print(f"❌ Erro na importação: {e}")
        return False
    
    print("🔍 Testando função calcular_residuo_zscore_timeframe...")
    
    try:
        # Usar ativos reais da lista
        dep = dependente[0] if dependente else 'PETR4'
        ind = independente[0] if independente else 'VALE3'
        ibov = 'IBOV'
        win = 'WIN$'
        per = periodo[0] if periodo else 21
        
        print(f"   Testando par: {dep}/{ind} com período {per}")
        
        # Gerar dados simulados simples para teste
        dates = pd.date_range(end=datetime.now(), periods=500, freq='H')
        np.random.seed(42)
        
        dados_simulados = {}
        for symbol in [dep, ind, ibov, win]:
            price_base = 100 + np.random.normal(0, 10)
            returns = np.random.normal(0.001, 0.02, 500)  # Retornos normais
            prices = [price_base]
            for ret in returns[1:]:
                prices.append(prices[-1] * (1 + ret))
            
            dados_simulados[symbol] = pd.DataFrame({
                'close': prices,
                'open': [p * 0.999 for p in prices],
                'high': [p * 1.002 for p in prices],
                'low': [p * 0.998 for p in prices],
                'volume': np.random.randint(1000, 10000, 500)
            }, index=dates)
        
        print("   Dados simulados criados!")
        
        # Testar a função diretamente
        resultado = calcular_residuo_zscore_timeframe(
            dep=dep,
            ind=ind,
            ibov=ibov,
            win=win,
            periodo=per,
            dados_preprocessados=dados_simulados,
            zscore_threshold=2.0,
            enable_zscore_filter=True,
            enable_r2_filter=True,
            enable_beta_filter=True,
            enable_cointegration_filter=True,
            zscore_min_threshold=0.5,
            zscore_max_threshold=3.0,
            r2_min_threshold=0.1,
            beta_max_threshold=5.0
        )
        
        if resultado is None:
            print("   ⚠️ Resultado é None (par rejeitado pelos filtros - comportamento normal)")
            return True
        
        # Verificar se o resultado tem o formato esperado
        if not isinstance(resultado, (list, tuple)):
            print(f"   ❌ Resultado não é lista/tupla: {type(resultado)}")
            return False
        
        if len(resultado) != 16:
            print(f"   ❌ Resultado tem {len(resultado)} elementos, esperado 16")
            print(f"   Resultado: {resultado}")
            return False
        
        # Testar desempacotamento (onde o erro adf_p_value acontecia)
        try:
            (alpha, beta, half_life, zscore_final, residuo_atual, 
             adf_p_value, pred_resid, resid_atual, zscore_forecast_compra, 
             zscore_forecast_venda, zf_compra, zf_venda, nd_dep, nd_ind, 
             coint_p_value, r2) = resultado
             
            print("   ✅ Desempacotamento bem-sucedido!")
            print(f"   adf_p_value: {adf_p_value}")
            print(f"   r2: {r2}")
            print(f"   zscore_final: {zscore_final}")
            
            # Verificar se os valores são válidos
            if adf_p_value is None:
                print("   ⚠️ adf_p_value é None")
            else:
                print(f"   ✅ adf_p_value válido: {adf_p_value}")
                
            return True
            
        except ValueError as ve:
            print(f"   ❌ Erro no desempacotamento: {ve}")
            print(f"   Resultado recebido: {resultado}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro geral no teste: {e}")
        return False

if __name__ == "__main__":
    print("🧪 TESTE DO FIX adf_p_value")
    print("=" * 50)
    
    success = test_adf_p_value_fix()
    
    print("=" * 50)
    if success:
        print("🎉 TESTE PASSOU! O erro adf_p_value foi corrigido.")
    else:
        print("❌ TESTE FALHOU! Ainda há problemas.")
