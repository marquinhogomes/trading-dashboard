#!/usr/bin/env python3
"""
Teste rápido após correção do erro pairs_dependente
"""
import sys
print("🔍 Testando sistema após correções...")

try:
    print("1. Importando config_real...")
    from config_real import DEPENDENTE_REAL, get_real_config_for_streamlit
    config = get_real_config_for_streamlit()
    print(f"   ✅ {len(DEPENDENTE_REAL)} dependentes, {len(config)} configurações")
    
    print("2. Importando módulo de integração...")
    from trading_real_integration import real_state, HAS_REAL_CONFIG
    print(f"   ✅ Estado carregado, config real: {HAS_REAL_CONFIG}")
    
    print("3. Teste manual de inicialização...")
    from trading_real_integration import safe_auto_init
    result = safe_auto_init()
    print(f"   {'✅' if result else '⚠️'} Inicialização: {result}")
    
    print("4. Importando dashboard...")
    import trading_dashboard_real
    print("   ✅ Dashboard importado com sucesso")
    
    print("\n🎉 SISTEMA FUNCIONANDO!")
    print("🚀 Execute: streamlit run trading_dashboard_real.py")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
