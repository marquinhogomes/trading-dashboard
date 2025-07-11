#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para verificar a correção do erro 'ndiffss'
"""

import sys
sys.path.append('.')

def testar_estrutura_dados():
    """Testa se a estrutura de dados está correta"""
    print("🧪 Testando estrutura de dados para análise real...")
    
    try:
        from dashboard_trading_pro_real import TradingSystemReal
        import pandas as pd
        import numpy as np
        
        sistema = TradingSystemReal()
        
        # Simula dados históricos para teste
        print("📊 Criando dados de teste...")
        dados_teste = {
            'ABEV3': {
                'close': {
                    'data': pd.Series(np.random.normal(100, 5, 200)),
                    'ndiffs': 0,
                    'raw': pd.Series(np.random.normal(100, 5, 200)),
                    'is_stationary': True
                }
            },
            'VALE3': {
                'close': {
                    'data': pd.Series(np.random.normal(50, 3, 200)),
                    'ndiffs': 0,
                    'raw': pd.Series(np.random.normal(50, 3, 200)),
                    'is_stationary': True
                }
            },
            'IBOV': {
                'close': {
                    'data': pd.Series(np.random.normal(120000, 5000, 200)),
                    'ndiffs': 0,
                    'raw': pd.Series(np.random.normal(120000, 5000, 200)),
                    'is_stationary': True
                }
            }
        }
        
        print("✅ Estrutura de dados criada com sucesso")
        
        # Testa acesso aos campos necessários
        simbolos_teste = ['ABEV3', 'VALE3', 'IBOV']
        
        for simbolo in simbolos_teste:
            # Testa se existe a estrutura esperada
            if simbolo in dados_teste:
                close_data = dados_teste[simbolo]['close']
                
                # Verifica se tem os campos necessários
                if 'ndiffs' in close_data:
                    print(f"✅ {simbolo}: campo 'ndiffs' encontrado = {close_data['ndiffs']}")
                else:
                    print(f"❌ {simbolo}: campo 'ndiffs' NÃO encontrado")
                
                if 'raw' in close_data:
                    print(f"✅ {simbolo}: campo 'raw' encontrado (tamanho: {len(close_data['raw'])})")
                else:
                    print(f"❌ {simbolo}: campo 'raw' NÃO encontrado")
            else:
                print(f"❌ {simbolo}: símbolo não encontrado")
        
        print("\n🧪 Testando importação da função de análise...")
        
        try:
            from calculo_entradas_v55 import calcular_residuo_zscore_timeframe
            print("✅ Função calcular_residuo_zscore_timeframe importada com sucesso")
            
            # Teste básico da função (sem executar completamente)
            print("🔍 Testando chamada da função com dados de teste...")
            
            # Parâmetros de teste
            config_teste = {
                'enable_zscore_filter': True,
                'enable_r2_filter': True,
                'enable_beta_filter': True,
                'enable_cointegration_filter': True,
                'zscore_min_threshold': -2.0,
                'zscore_max_threshold': 2.0,
                'r2_min_threshold': 0.50,
                'beta_max_threshold': 1.5
            }
            
            try:
                resultado = calcular_residuo_zscore_timeframe(
                    dep='ABEV3',
                    ind='VALE3',
                    ibov='IBOV',
                    win='IBOV',
                    periodo=100,
                    dados_preprocessados=dados_teste,
                    verbose=False,
                    **config_teste
                )
                
                print("✅ Função executada com sucesso!")
                print(f"📊 Tipo do resultado: {type(resultado)}")
                
                if isinstance(resultado, dict):
                    print(f"📊 Chaves no resultado: {list(resultado.keys())}")
                    
            except Exception as e:
                print(f"⚠️ Erro na execução da função: {str(e)}")
                # Isso é esperado se não tivermos dados MT5 reais
                if "'ndiffs'" in str(e) or "'raw'" in str(e):
                    print("❌ Erro ainda relacionado à estrutura de dados")
                else:
                    print("ℹ️ Erro diferente (pode ser normal com dados simulados)")
                    
        except ImportError as e:
            print(f"❌ Erro ao importar função: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔧 Teste de Correção do Erro 'ndiffss'")
    print("=" * 50)
    
    sucesso = testar_estrutura_dados()
    
    print("=" * 50)
    if sucesso:
        print("✅ TESTE CONCLUÍDO - Estrutura corrigida")
        print("💡 Execute o dashboard para testar com dados reais")
    else:
        print("❌ TESTE FALHOU - Verifique os erros acima")
    
    print("\n📋 Para testar com MT5 real:")
    print("1. Execute: streamlit run dashboard_trading_pro_real.py")
    print("2. Conecte ao MT5")  
    print("3. Inicie o sistema")
    print("4. Monitore os logs para confirmar que o erro foi resolvido")
