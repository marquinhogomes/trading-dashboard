#!/usr/bin/env python3
"""
Teste de Sintaxe: Dashboard Trading Pro
=====================================
"""

import sys
import os

def testar_sintaxe():
    """Testa se o arquivo tem problemas de sintaxe"""
    print("🧪 TESTE DE SINTAXE DO DASHBOARD")
    print("=" * 50)
    
    # Caminho do arquivo
    arquivo = "dashboard_trading_pro_real.py"
    
    if not os.path.exists(arquivo):
        print(f"❌ Arquivo {arquivo} não encontrado")
        return False
    
    print(f"✅ Arquivo {arquivo} encontrado")
    
    try:
        # Tenta compilar o arquivo
        with open(arquivo, 'r', encoding='utf-8') as f:
            codigo = f.read()
        
        # Compila o código
        compile(codigo, arquivo, 'exec')
        print("✅ Sintaxe do arquivo está correta")
        
        # Tenta importar
        import importlib.util
        spec = importlib.util.spec_from_file_location("dashboard", arquivo)
        dashboard = importlib.util.module_from_spec(spec)
        
        print("✅ Arquivo pode ser importado")
        
        # Verifica se as funções principais existem
        spec.loader.exec_module(dashboard)
        
        funcoes_essenciais = [
            'TradingSystemReal',
            'render_header',
            'render_sidebar', 
            'render_equity_chart',
            'main'
        ]
        
        for funcao in funcoes_essenciais:
            if hasattr(dashboard, funcao):
                print(f"✅ {funcao} encontrada")
            else:
                print(f"❌ {funcao} NÃO encontrada")
                return False
        
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("💡 O dashboard deve funcionar corretamente")
        return True
        
    except SyntaxError as e:
        print(f"❌ ERRO DE SINTAXE:")
        print(f"   Linha {e.lineno}: {e.text}")
        print(f"   Erro: {e.msg}")
        return False
        
    except ImportError as e:
        print(f"❌ ERRO DE IMPORTAÇÃO: {str(e)}")
        return False
        
    except Exception as e:
        print(f"❌ ERRO GERAL: {str(e)}")
        return False

if __name__ == "__main__":
    testar_sintaxe()
