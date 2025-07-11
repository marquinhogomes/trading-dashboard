#!/usr/bin/env python3
"""
Script de teste simples para verificar a inicialização do TradingSystemReal.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def testar_inicializacao():
    """Testa a inicialização da classe TradingSystemReal"""
    print("=== Teste de Inicialização do TradingSystemReal ===")
    
    try:
        # Importa o módulo
        from dashboard_trading_pro_real import TradingSystemReal
        print("✓ Módulo importado com sucesso")
        
        # Cria uma instância
        sistema = TradingSystemReal()
        print("✓ Instância criada com sucesso")
        
        # Verifica se o atributo logs existe
        if hasattr(sistema, 'logs'):
            print(f"✓ Atributo 'logs' encontrado: {type(sistema.logs)}")
            print(f"✓ Conteúdo inicial dos logs: {sistema.logs}")
        else:
            print("✗ Atributo 'logs' não encontrado")
        
        # Verifica se logs_exibicao funciona
        try:
            logs_exibicao = sistema.logs_exibicao
            print(f"✓ Propriedade 'logs_exibicao' funciona: {type(logs_exibicao)}")
            print(f"✓ Conteúdo logs_exibicao: {logs_exibicao}")
        except Exception as e:
            print(f"✗ Erro ao acessar logs_exibicao: {e}")
            
        # Testa o método log
        try:
            if hasattr(sistema, 'log'):
                sistema.log("Teste de log")
                print("✓ Método 'log' funciona")
            else:
                print("✗ Método 'log' não encontrado")
        except Exception as e:
            print(f"✗ Erro ao testar método log: {e}")
        
        print("✓ Teste concluído com sucesso!")
        
    except Exception as e:
        print(f"✗ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    testar_inicializacao()
