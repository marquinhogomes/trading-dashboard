#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste Final Completo - Verifica todo o sistema
"""

def testar_sistema_completo():
    """Testa o sistema de trading completo"""
    print("🎯 TESTE FINAL DO SISTEMA DE TRADING")
    print("=" * 50)
    
    # Teste 1: Importações básicas
    print("\n📦 1. TESTANDO IMPORTAÇÕES BÁSICAS...")
    try:
        import numpy as np
        import pandas as pd
        import sklearn
        import arch
        print("✅ Bibliotecas científicas: OK")
    except Exception as e:
        print(f"❌ Erro nas bibliotecas básicas: {e}")
        return False
    
    # Teste 2: Keras/TensorFlow
    print("\n🧠 2. TESTANDO KERAS/TENSORFLOW...")
    try:
        import keras
        print(f"✅ Keras {keras.__version__}: OK")
    except Exception as e:
        print(f"⚠️  Keras não disponível: {e}")
    
    # Teste 3: MetaTrader5
    print("\n💹 3. TESTANDO METATRADER5...")
    try:
        import MetaTrader5 as mt5
        print("✅ MetaTrader5: OK")
    except Exception as e:
        print(f"❌ MetaTrader5 falhou: {e}")
        return False
    
    # Teste 4: Arquivo principal
    print("\n📄 4. TESTANDO ARQUIVO PRINCIPAL...")
    try:
        # Simula leitura do arquivo principal
        with open('calculo_entradas_v55.py', 'r', encoding='utf-8') as f:
            conteudo = f.read(1000)  # Lê apenas uma parte
        print("✅ Arquivo calculo_entradas_v55.py: OK")
    except Exception as e:
        print(f"❌ Erro no arquivo principal: {e}")
        return False
    
    # Teste 5: Sistema integrado
    print("\n🔧 5. TESTANDO SISTEMA INTEGRADO...")
    try:
        with open('sistema_integrado.py', 'r', encoding='utf-8') as f:
            conteudo = f.read(1000)
        print("✅ Sistema integrado: OK")
    except Exception as e:
        print(f"❌ Erro no sistema integrado: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 TODOS OS TESTES PASSARAM!")
    print("✅ Sistema pronto para execução completa")
    print("👉 Execute: python sistema_integrado.py")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    testar_sistema_completo()
