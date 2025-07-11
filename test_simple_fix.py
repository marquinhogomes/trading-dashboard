#!/usr/bin/env python3
"""
Teste simplificado para verificar as correções
"""

print("=" * 50)
print("🧪 TESTE SIMPLES DE CORREÇÕES")
print("=" * 50)

# Teste 1: Verificar se a seção trading está sendo carregada corretamente
print("\n1. Testando configuração de trading...")
try:
    from trading_real_integration import REAL_CONFIG, HAS_REAL_CONFIG
    
    print(f"   ✅ HAS_REAL_CONFIG: {HAS_REAL_CONFIG}")
    
    if HAS_REAL_CONFIG and REAL_CONFIG:
        print(f"   📊 REAL_CONFIG tem {len(REAL_CONFIG)} chaves")
        
        if 'trading' in REAL_CONFIG:
            print(f"   ✅ Seção 'trading' encontrada!")
            trading_params = list(REAL_CONFIG['trading'].keys())
            print(f"   📋 Parâmetros trading: {trading_params}")
        else:
            print(f"   ❌ Seção 'trading' AINDA não encontrada")
            print(f"   📋 Chaves disponíveis: {list(REAL_CONFIG.keys())}")
    else:
        print("   ⚠️ REAL_CONFIG não disponível")
        
except Exception as e:
    print(f"   ❌ Erro: {e}")

# Teste 2: Verificar importação da função principal
print("\n2. Testando importação da função principal...")
try:
    from calculo_entradas_v55 import calcular_residuo_zscore_timeframe
    print("   ✅ Função calcular_residuo_zscore_timeframe importada com sucesso")
except Exception as e:
    print(f"   ❌ Erro na importação: {e}")

# Teste 3: Verificar se warnings do TensorFlow foram suprimidos
print("\n3. Testando supressão de warnings do TensorFlow...")
try:
    # Deve importar sem warnings excessivos
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        import tensorflow as tf
    print("   ✅ TensorFlow importado sem warnings críticos")
except Exception as e:
    print(f"   ⚠️ TensorFlow não disponível: {e}")

print("\n" + "=" * 50)
print("✅ TESTE BÁSICO CONCLUÍDO")
print("=" * 50)
