#!/usr/bin/env python3
"""
Teste Final - Bypass dos problemas de interferência
"""

def test_quiet():
    """Teste silencioso das correções"""
    results = []
    
    # Teste 1: Config
    try:
        from config_real import SYSTEM_INFO
        if 'source_file' in SYSTEM_INFO and 'config_type' in SYSTEM_INFO:
            results.append("✅ Config corrigido")
        else:
            results.append("❌ Config com problemas")
    except:
        results.append("❌ Config falhou")
    
    # Teste 2: Integration
    try:
        import trading_real_integration
        if hasattr(trading_real_integration, 'safe_auto_init'):
            results.append("✅ Integration corrigido")
        else:
            results.append("❌ Integration com problemas")
    except:
        results.append("❌ Integration falhou")
    
    return results

if __name__ == "__main__":
    import sys
    
    # Executar apenas se chamado diretamente
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        results = test_quiet()
        for r in results:
            print(r)
        print("\n🚀 Para usar: streamlit run dashboard_teste_simples.py")
    else:
        print("Use: python teste_final_quiet.py --test")
