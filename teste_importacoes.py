#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste de Importações - Verifica se todas as dependências funcionam
"""

def testar_importacoes():
    """Testa todas as importações críticas do projeto"""
    print("🔍 TESTANDO IMPORTAÇÕES...")
    
    try:
        import numpy as np
        print(f"✅ NumPy {np.__version__}")
        
        # Testa especificamente np.nan (forma correta)
        teste_nan = np.nan
        print(f"✅ np.nan funcionando: {teste_nan}")
        
    except Exception as e:
        print(f"❌ NumPy falhou: {e}")
        return False
    
    try:
        import pandas as pd
        print(f"✅ Pandas {pd.__version__}")
    except Exception as e:
        print(f"❌ Pandas falhou: {e}")
        return False
    
    try:
        import sklearn
        print(f"✅ Scikit-learn {sklearn.__version__}")
    except Exception as e:
        print(f"❌ Scikit-learn falhou: {e}")
        return False
    
    try:
        import arch
        print(f"✅ Arch {arch.__version__}")
    except Exception as e:
        print(f"❌ Arch falhou: {e}")
        return False
        
    try:
        import pandas_ta as pta
        print(f"✅ Pandas-TA disponível")
    except Exception as e:
        print(f"❌ Pandas-TA falhou: {e}")
        return False
    
    try:
        import MetaTrader5 as mt5
        print(f"✅ MetaTrader5 disponível")
    except Exception as e:
        print(f"❌ MetaTrader5 falhou: {e}")
        return False
        
    try:
        import statsmodels
        print(f"✅ Statsmodels {statsmodels.__version__}")
    except Exception as e:
        print(f"❌ Statsmodels falhou: {e}")
        return False
    
    print("\n🎉 TODAS AS IMPORTAÇÕES FUNCIONARAM!")
    return True

def testar_codigo_minimo():
    """Testa um código mínimo com as funcionalidades principais"""
    print("\n🧪 TESTANDO CÓDIGO BÁSICO...")
    
    try:
        import numpy as np
        import pandas as pd
        
        # Cria dados de teste
        dados = pd.DataFrame({
            'precos': [10.5, 11.2, 10.8, 11.5, 12.0],
            'volume': [1000, 1500, 1200, 1800, 2000]
        })
        
        # Testa operações com NaN
        dados_com_nan = dados.copy()
        dados_com_nan.loc[2, 'precos'] = np.nan
        
        # Remove NaN (método correto)
        dados_limpos = dados_com_nan.dropna()
        
        print(f"✅ Dados originais: {len(dados)} linhas")
        print(f"✅ Dados com NaN: {dados_com_nan.isnull().sum().sum()} valores NaN")
        print(f"✅ Dados limpos: {len(dados_limpos)} linhas")
        
        return True
        
    except Exception as e:
        print(f"❌ Teste básico falhou: {e}")
        return False

if __name__ == "__main__":
    print("🎯 TESTE DE COMPATIBILIDADE - SISTEMA TRADING")
    print("=" * 50)
    
    sucesso_imports = testar_importacoes()
    sucesso_codigo = testar_codigo_minimo()
    
    print("\n" + "=" * 50)
    if sucesso_imports and sucesso_codigo:
        print("🎉 SISTEMA PRONTO PARA EXECUÇÃO!")
        print("👉 Execute: python sistema_integrado.py")
    else:
        print("❌ PROBLEMAS DETECTADOS - Verifique as dependências")
    print("=" * 50)
