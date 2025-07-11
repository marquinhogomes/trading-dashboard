#!/usr/bin/env python3
"""
Teste para debugar o erro pairs_dependente
"""

print("🔍 Debugando erro do sistema...")

# Teste 1: Importar config_real
try:
    from config_real import get_real_config_for_streamlit, DEPENDENTE_REAL, INDEPENDENTE_REAL
    config = get_real_config_for_streamlit()
    print(f"✅ Config carregada com {len(config)} chaves")
    print(f"   Chaves disponíveis: {list(config.keys())}")
    print(f"   pairs_dependente presente: {'pairs_dependente' in config}")
    print(f"   pairs_independente presente: {'pairs_independente' in config}")
    if 'pairs_dependente' in config:
        print(f"   Qtd dependentes: {len(config['pairs_dependente'])}")
    if 'pairs_independente' in config:
        print(f"   Qtd independentes: {len(config['pairs_independente'])}")
except Exception as e:
    print(f"❌ Erro no config_real: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*50)

# Teste 2: Importar trading_real_integration
try:
    print("🔄 Testando importação do módulo de integração...")
    import trading_real_integration
    print("✅ Módulo de integração importado com sucesso!")
    
    # Verificar estado
    if hasattr(trading_real_integration, 'real_state'):
        state = trading_real_integration.real_state
        print(f"   Estado inicializado: {state.is_initialized}")
        print(f"   Logs disponíveis: {len(state.logs)}")
        if state.logs:
            print("   Últimos logs:")
            for log in state.logs[-3:]:
                print(f"      {log}")
    
    # Verificar REAL_CONFIG
    if hasattr(trading_real_integration, 'REAL_CONFIG'):
        config = trading_real_integration.REAL_CONFIG
        print(f"   REAL_CONFIG carregado: {config is not None}")
        if config:
            print(f"   Chaves em REAL_CONFIG: {list(config.keys())}")
    
except Exception as e:
    print(f"❌ Erro no trading_real_integration: {e}")
    import traceback
    traceback.print_exc()

print("\n🎯 Debug concluído!")
