#!/usr/bin/env python3
"""
Teste completo do sistema real integrado
"""

def testar_sistema_completo():
    print("🔄 Testando sistema completo...")
    
    try:
        # 1. Testar configurações
        print("1. Testando configurações...")
        from config_real import DEPENDENTE_REAL, SEGMENTOS_REAIS, get_setores_disponiveis
        print(f"   ✅ {len(DEPENDENTE_REAL)} ativos, {len(SEGMENTOS_REAIS)} mapeamentos")
        print(f"   ✅ {len(get_setores_disponiveis())} setores disponíveis")
        
        # 2. Testar análise
        print("2. Testando módulo de análise...")
        from analise_real import get_analise_para_streamlit
        print("   ✅ Módulo de análise importado")
        
        # 3. Testar integração
        print("3. Testando integração...")
        from trading_real_integration import get_real_system_status, get_real_analysis_data
        print("   ✅ Módulo de integração importado")
        
        # 4. Testar status
        print("4. Testando status do sistema...")
        status = get_real_system_status()
        print(f"   ✅ Status obtido: {status.get('fonte', 'N/A')}")
        
        # 5. Testar dashboard
        print("5. Testando dashboard...")
        import trading_dashboard_real
        print("   ✅ Dashboard real importado")
        
        print("\n🎉 SISTEMA REAL INTEGRADO COM SUCESSO!")
        print("📊 Resumo:")
        print(f"   - Ativos: {len(DEPENDENTE_REAL)}")
        print(f"   - Setores: {len(get_setores_disponiveis())}")
        print(f"   - Sistema ativo: {status.get('config_real_carregada', False)}")
        print(f"   - Análise disponível: {status.get('analise_real_disponivel', False)}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    testar_sistema_completo()
