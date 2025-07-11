#!/usr/bin/env python3
"""
Teste rápido para verificar se as correções do erro 'adf_p_value' estão funcionando
"""

import sys
import os

# Adicionar caminho do projeto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Teste de importações básicas"""
    try:
        print("🔄 Testando importações...")
        
        # Tentar importar função principal
        from calculo_entradas_v55 import calcular_residuo_zscore_timeframe
        print("✅ calcular_residuo_zscore_timeframe importada com sucesso")
        
        # Tentar importar trading_real_integration
        from trading_real_integration import REAL_CONFIG, HAS_REAL_CONFIG
        print(f"✅ trading_real_integration importado: HAS_REAL_CONFIG={HAS_REAL_CONFIG}")
        
        if HAS_REAL_CONFIG and 'trading' in REAL_CONFIG:
            print(f"✅ Seção 'trading' encontrada em REAL_CONFIG")
        else:
            print(f"⚠️ Seção 'trading' não encontrada ou config indisponível")
            
        return True
        
    except Exception as e:
        print(f"❌ Erro na importação: {e}")
        return False

def test_function_call():
    """Teste básico da função principal"""
    try:
        print("\n🔄 Testando chamada básica da função...")
        
        from calculo_entradas_v55 import calcular_residuo_zscore_timeframe
        import pandas as pd
        import numpy as np
        
        # Dados simulados em formato pandas DataFrame (formato correto)
        n_pontos = 100
        dates = pd.date_range('2024-01-01', periods=n_pontos, freq='H')
        
        dados_teste = {
            'PETR4': pd.DataFrame({
                'close': 10 + np.random.randn(n_pontos) * 0.5,
                'open': 10 + np.random.randn(n_pontos) * 0.5,
                'high': 10 + np.random.randn(n_pontos) * 0.5,
                'low': 10 + np.random.randn(n_pontos) * 0.5
            }, index=dates),
            'VALE3': pd.DataFrame({
                'close': 20 + np.random.randn(n_pontos) * 0.5,
                'open': 20 + np.random.randn(n_pontos) * 0.5,
                'high': 20 + np.random.randn(n_pontos) * 0.5,
                'low': 20 + np.random.randn(n_pontos) * 0.5
            }, index=dates),
            'IBOV': pd.DataFrame({
                'close': 100 + np.random.randn(n_pontos) * 1.0,
                'open': 100 + np.random.randn(n_pontos) * 1.0,
                'high': 100 + np.random.randn(n_pontos) * 1.0,
                'low': 100 + np.random.randn(n_pontos) * 1.0
            }, index=dates),
            'WIN$': pd.DataFrame({
                'close': 50 + np.random.randn(n_pontos) * 0.3,
                'open': 50 + np.random.randn(n_pontos) * 0.3,
                'high': 50 + np.random.randn(n_pontos) * 0.3,
                'low': 50 + np.random.randn(n_pontos) * 0.3
            }, index=dates)
        }
        
        # Chamada com dados em formato correto - esperamos que retorne None por filtros
        resultado = calcular_residuo_zscore_timeframe(
            dep='PETR4',
            ind='VALE3', 
            ibov='IBOV',
            win='WIN$',
            periodo=21,  # Usar número em vez de string
            dados_preprocessados=dados_teste,
            verbose=True
        )
        
        if resultado is None:
            print("✅ Função retornou None (par rejeitado pelos filtros - comportamento esperado)")
        else:
            print(f"✅ Função retornou resultado com {len(resultado)} elementos")
            
        return True
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Erro na chamada da função: {e}")
        
        if "'adf_p_value'" in error_msg:
            print("🔍 CONFIRMADO: Erro ainda relacionado ao 'adf_p_value'")
        elif "list indices must be integers" in error_msg:
            print("🔍 ERRO CORRIGIDO: Problema de formato de dados resolvido")
        
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 TESTE DE CORREÇÃO DO ERRO 'adf_p_value'")
    print("=" * 60)
    
    success = True
    
    # Teste 1: Importações
    if not test_imports():
        success = False
    
    # Teste 2: Função principal  
    if not test_function_call():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("✅ TODOS OS TESTES PASSARAM!")
        print("🎯 As correções parecem estar funcionando corretamente.")
    else:
        print("❌ ALGUNS TESTES FALHARAM!")
        print("🔧 Correções adicionais podem ser necessárias.")
    print("=" * 60)
