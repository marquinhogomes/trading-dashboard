#!/usr/bin/env python3
"""
Teste rápido da correção do KeyError: 'trading'
"""

print("🧪 Testando correção do KeyError: 'trading'...")

try:
    # Importar módulo corrigido
    print("1. Importando trading_real_integration...")
    import trading_real_integration as tri
    
    # Verificar REAL_CONFIG
    print("2. Verificando REAL_CONFIG...")
    if hasattr(tri, 'REAL_CONFIG') and tri.REAL_CONFIG:
        config = tri.REAL_CONFIG
        print(f"   ✅ REAL_CONFIG carregado: {len(config)} chaves")
        print(f"   📋 Chaves: {list(config.keys())}")
        
        if 'trading' in config:
            print(f"   ✅ Seção 'trading' presente!")
            trading_config = config['trading']
            print(f"   💰 Limite operações: {trading_config.get('limite_operacoes', 'N/A')}")
            print(f"   💰 Valor operação: {trading_config.get('valor_operacao', 'N/A')}")
        else:
            print(f"   ❌ Seção 'trading' AINDA ausente!")
    else:
        print(f"   ❌ REAL_CONFIG não carregado")
    
    # Teste de inicialização
    print("3. Testando inicialização...")
    if hasattr(tri, 'safe_auto_init'):
        resultado = tri.safe_auto_init()
        print(f"   Resultado: {'✅' if resultado else '❌'}")
    else:
        print(f"   ❌ Função safe_auto_init não encontrada")
    
    print("\n🎉 TESTE CONCLUÍDO!")
    
except Exception as e:
    print(f"❌ Erro durante teste: {e}")
    import traceback
    traceback.print_exc()

print("\n🚀 Execute: streamlit run dashboard_teste_simples.py")
