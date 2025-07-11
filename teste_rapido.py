#!/usr/bin/env python3
"""Teste rápido da validação"""

print("🔄 Teste Rápido de Validação")

try:
    # 1. Testar importações
    from config_real import DEPENDENTE_REAL, FILTER_PARAMS_REAL, SYSTEM_INFO
    from analise_real import get_analise_para_streamlit
    from trading_real_integration import get_real_system_status
    print("✅ Importações OK")
    
    # 2. Testar configurações
    print(f"✅ Config: {len(DEPENDENTE_REAL)} ativos, v{SYSTEM_INFO['version']}")
    
    # 3. Testar status
    status = get_real_system_status()
    print(f"✅ Status: {status.get('fonte')}, Real: {status.get('config_real_carregada')}")
    
    # 4. Validar parâmetros críticos
    assert FILTER_PARAMS_REAL['r2_min'] == 0.5
    assert FILTER_PARAMS_REAL['beta_max'] == 1.5
    assert FILTER_PARAMS_REAL['enable_cointegration_filter'] == True
    print("✅ Parâmetros validados")
    
    print("\n🎉 VALIDAÇÃO COMPLETA - SISTEMA PRONTO!")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
