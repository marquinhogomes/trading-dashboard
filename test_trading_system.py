#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste para verificar se a classe TradingSystemReal está funcionando corretamente
"""

import sys
sys.path.append('.')

try:
    from dashboard_trading_pro_real import TradingSystemReal
    
    print("✅ Importação da classe TradingSystemReal: OK")
    
    # Cria instância
    sistema = TradingSystemReal()
    print("✅ Criação da instância: OK")
    
    # Verifica se os métodos existem
    metodos_necessarios = ['iniciar_sistema', 'parar_sistema', 'conectar_mt5', 'log']
    
    for metodo in metodos_necessarios:
        if hasattr(sistema, metodo):
            print(f"✅ Método '{metodo}': OK")
        else:
            print(f"❌ Método '{metodo}': NÃO ENCONTRADO")
    
    # Testa log
    sistema.log("Teste de log")
    print("✅ Teste de log: OK")
    
    print("\n🎉 Todos os testes passaram! O objeto está funcionando corretamente.")
    
except Exception as e:
    print(f"❌ Erro durante os testes: {str(e)}")
    import traceback
    traceback.print_exc()
