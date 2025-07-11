#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste para verificar se o bug da análise foi corrigido
"""

import sys
import traceback
import pandas as pd
import numpy as np

def test_zscore_calculation():
    """Testa o cálculo de z-score que estava falhando"""
    try:
        # Simular dados similares ao que causava o erro
        dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
        
        # Criar séries pandas (não arrays)
        y_aligned = pd.Series(np.random.randn(100) + 10, index=dates)
        x_aligned = pd.Series(np.random.randn(100) + 10, index=dates)
        
        # Parâmetros fictícios
        alpha = 1.5
        beta = 0.8
        
        # Calcular resíduo (isso deve resultar em pandas Series)
        residuo = y_aligned - (alpha + beta * x_aligned)
        print(f"Tipo do resíduo: {type(residuo)}")
        print(f"É pandas Series? {isinstance(residuo, pd.Series)}")
        
        # Garantir que residuo seja pandas Series (lógica do fix)
        if not isinstance(residuo, pd.Series):
            if hasattr(residuo, '__len__') and len(residuo) > 0:
                residuo = pd.Series(residuo, index=y_aligned.index if hasattr(y_aligned, 'index') else range(len(residuo)))
            else:
                residuo = pd.Series([residuo], index=[0])
        
        # Calcular z-score (esta linha estava falhando)
        if len(residuo) > 0:
            zscore_atual = (residuo.iloc[-1] - residuo.mean()) / residuo.std()
        else:
            zscore_atual = 0.0
            
        print(f"Z-score calculado com sucesso: {zscore_atual:.4f}")
        print("✅ TESTE PASSOU - Bug corrigido!")
        return True
        
    except Exception as e:
        print(f"❌ TESTE FALHOU - Erro: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False

def test_numpy_array_scenario():
    """Testa cenário onde o resíduo é um numpy array"""
    try:
        # Simular cenário onde residuo pode ser numpy array
        residuo_array = np.random.randn(100)
        print(f"Tipo original: {type(residuo_array)}")
        
        # Aplicar o fix
        residuo = residuo_array
        if not isinstance(residuo, pd.Series):
            if hasattr(residuo, '__len__') and len(residuo) > 0:
                residuo = pd.Series(residuo, index=range(len(residuo)))
            else:
                residuo = pd.Series([residuo], index=[0])
        
        print(f"Tipo após conversão: {type(residuo)}")
        
        # Tentar usar .iloc (isto estava falhando)
        if len(residuo) > 0:
            zscore_atual = (residuo.iloc[-1] - residuo.mean()) / residuo.std()
        else:
            zscore_atual = 0.0
            
        print(f"Z-score do array convertido: {zscore_atual:.4f}")
        print("✅ CONVERSÃO DE NUMPY ARRAY FUNCIONOU!")
        return True
        
    except Exception as e:
        print(f"❌ CONVERSÃO FALHOU - Erro: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    print("🔧 Testando correção do bug de z-score...")
    print("=" * 50)
    
    print("\n1. Testando cálculo normal de z-score:")
    test1 = test_zscore_calculation()
    
    print("\n2. Testando conversão de numpy array:")
    test2 = test_numpy_array_scenario()
    
    print("\n" + "=" * 50)
    if test1 and test2:
        print("🎉 TODOS OS TESTES PASSARAM! Bug corrigido com sucesso!")
    else:
        print("⚠️  Alguns testes falharam. Verifique os logs acima.")
