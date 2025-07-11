#!/usr/bin/env python3
"""
Diagnóstico do erro KeyError: 'trading'
"""

print("🔍 Diagnosticando erro 'trading'...")

# Teste 1: Verificar get_real_config_for_streamlit diretamente
print("\n1. Testando get_real_config_for_streamlit()...")
try:
    from config_real import get_real_config_for_streamlit
    config = get_real_config_for_streamlit()
    
    print(f"   ✅ Configuração carregada com {len(config)} chaves")
    print(f"   📋 Chaves: {list(config.keys())}")
    
    if 'trading' in config:
        print(f"   ✅ Seção 'trading' encontrada")
        print(f"   📊 Trading keys: {list(config['trading'].keys())}")
        print(f"   💰 Limite operações: {config['trading']['limite_operacoes']}")
        print(f"   💰 Valor operação: {config['trading']['valor_operacao']}")
    else:
        print(f"   ❌ Seção 'trading' NÃO encontrada!")
        
except Exception as e:
    print(f"   ❌ Erro: {e}")
    import traceback
    traceback.print_exc()

# Teste 2: Verificar variáveis no trading_real_integration
print("\n2. Testando variáveis do trading_real_integration...")
try:
    import trading_real_integration as tri
    
    print(f"   HAS_REAL_CONFIG: {tri.HAS_REAL_CONFIG}")
    print(f"   REAL_CONFIG existe: {hasattr(tri, 'REAL_CONFIG')}")
    
    if hasattr(tri, 'REAL_CONFIG') and tri.REAL_CONFIG:
        config = tri.REAL_CONFIG
        print(f"   REAL_CONFIG chaves: {list(config.keys())}")
        
        if 'trading' in config:
            print(f"   ✅ 'trading' presente em REAL_CONFIG")
        else:
            print(f"   ❌ 'trading' AUSENTE em REAL_CONFIG!")
            print(f"   🔧 Corrigindo...")
            
            # Tentar corrigir
            from config_real import get_real_config_for_streamlit
            new_config = get_real_config_for_streamlit()
            if 'trading' in new_config:
                tri.REAL_CONFIG = new_config
                print(f"   ✅ REAL_CONFIG corrigido!")
            else:
                print(f"   ❌ Problema persiste na fonte!")
    else:
        print(f"   ❌ REAL_CONFIG não inicializado")
        
except Exception as e:
    print(f"   ❌ Erro: {e}")
    import traceback
    traceback.print_exc()

print("\n🎯 Diagnóstico concluído!")
