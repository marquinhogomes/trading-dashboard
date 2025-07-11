#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste de carregamento dos módulos reais
"""

try:
    print("🔄 Testando importação dos módulos...")
    
    print("1. Config real...")
    from config_real import SYSTEM_INFO, DEPENDENTE_REAL, SEGMENTOS_REAIS, FILTER_PARAMS_REAL
    print(f"   ✅ Config carregada: {len(DEPENDENTE_REAL)} dependentes, {len(SEGMENTOS_REAIS)} setores")
    
    print("2. Análise real...")
    from analise_real import executar_analise_completa, get_analise_para_streamlit
    print("   ✅ Módulo de análise carregado")
    
    print("3. Trading integration...")
    from trading_real_integration import get_real_analysis_data, get_real_system_status
    print("   ✅ Módulo de integração carregado")
    
    print("4. Testando funcionalidade...")
    status = get_real_system_status()
    print(f"   ✅ Status: {status.get('fonte', 'N/A')}")
    
    print("\n🎉 TODOS OS MÓDULOS CARREGADOS COM SUCESSO!")
    print(f"📊 Sistema: {SYSTEM_INFO}")
    
except Exception as e:
    print(f"❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
