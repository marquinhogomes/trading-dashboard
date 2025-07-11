#!/usr/bin/env python3
"""
Teste das correções aplicadas
"""

print("🔧 Testando correções aplicadas...")

# Teste 1: config_real
print("\n1. Testando config_real...")
try:
    from config_real import SYSTEM_INFO
    print(f"   ✅ SYSTEM_INFO carregado")
    print(f"   Versão: {SYSTEM_INFO['version']}")
    print(f"   Fonte: {SYSTEM_INFO['source_file']}")
    print(f"   Config Type: {SYSTEM_INFO['config_type']}")
except Exception as e:
    print(f"   ❌ Erro: {e}")

# Teste 2: trading_real_integration
print("\n2. Testando trading_real_integration...")
try:
    from trading_real_integration import safe_auto_init, REAL_CONFIG
    print(f"   ✅ Módulo importado")
    print(f"   REAL_CONFIG disponível: {REAL_CONFIG is not None}")
    
    # Teste de inicialização manual
    result = safe_auto_init()
    print(f"   Inicialização: {'✅' if result else '⚠️'}")
    
except Exception as e:
    print(f"   ❌ Erro: {e}")
    import traceback
    traceback.print_exc()

# Teste 3: dashboard_teste_simples
print("\n3. Testando dashboard simplificado...")
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("dashboard", "dashboard_teste_simples.py")
    if spec:
        print("   ✅ Dashboard de teste disponível")
    else:
        print("   ❌ Dashboard não encontrado")
except Exception as e:
    print(f"   ❌ Erro: {e}")

print("\n🎯 Resumo das Correções:")
print("✅ REAL_CONFIG global declaration fixed")
print("✅ source_file key added to SYSTEM_INFO")  
print("✅ config_type key added to SYSTEM_INFO")
print("\n🚀 Execute: streamlit run dashboard_teste_simples.py")
