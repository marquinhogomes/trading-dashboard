#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste da implementação da segunda seleção no dashboard
"""

import sys
import os
sys.path.append('.')

def test_imports():
    """Testa se todas as importações necessárias estão funcionando"""
    print("🔍 Testando importações...")
    
    try:
        # Testa importação do dashboard
        from dashboard_trading_pro_real import TradingSystemReal
        print("✅ Dashboard importado com sucesso")
        
        # Testa importações do sistema de análise
        from calculo_entradas_v55 import (
            calcular_residuo_zscore_timeframe,
            calcular_residuo_zscore_timeframe01,
            encontrar_linha_monitorada,
            encontrar_linha_monitorada01,
            filtrar_melhores_pares
        )
        print("✅ Sistema de análise importado com sucesso")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_trading_system():
    """Testa a criação do sistema de trading"""
    print("\n🔍 Testando sistema de trading...")
    
    try:
        from dashboard_trading_pro_real import TradingSystemReal
        
        # Cria instância do sistema
        sistema = TradingSystemReal()
        print("✅ Sistema de trading criado com sucesso")
        
        # Verifica métodos essenciais
        metodos_essenciais = [
            'executar_analise_real',
            'obter_dados_historicos_mt5',
            'iniciar_sistema',
            'parar_sistema'
        ]
        
        for metodo in metodos_essenciais:
            if hasattr(sistema, metodo):
                print(f"✅ Método {metodo} encontrado")
            else:
                print(f"❌ Método {metodo} NÃO encontrado")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar sistema: {e}")
        return False

def test_analysis_functions():
    """Testa se as funções de análise estão acessíveis"""
    print("\n🔍 Testando funções de análise...")
    
    try:
        from calculo_entradas_v55 import (
            calcular_residuo_zscore_timeframe,
            calcular_residuo_zscore_timeframe01,
            encontrar_linha_monitorada,
            encontrar_linha_monitorada01,
            filtrar_melhores_pares
        )
        
        # Verifica assinaturas das funções
        import inspect
        
        # Primeira seleção
        sig1 = inspect.signature(calcular_residuo_zscore_timeframe)
        print(f"✅ calcular_residuo_zscore_timeframe: {len(sig1.parameters)} parâmetros")
        
        sig2 = inspect.signature(encontrar_linha_monitorada)
        print(f"✅ encontrar_linha_monitorada: {len(sig2.parameters)} parâmetros")
        
        sig3 = inspect.signature(filtrar_melhores_pares)
        print(f"✅ filtrar_melhores_pares: {len(sig3.parameters)} parâmetros")
        
        # Segunda seleção
        sig4 = inspect.signature(calcular_residuo_zscore_timeframe01)
        print(f"✅ calcular_residuo_zscore_timeframe01: {len(sig4.parameters)} parâmetros")
        
        sig5 = inspect.signature(encontrar_linha_monitorada01)
        print(f"✅ encontrar_linha_monitorada01: {len(sig5.parameters)} parâmetros")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar funções: {e}")
        return False

def test_dashboard_structure():
    """Testa a estrutura do dashboard"""
    print("\n🔍 Testando estrutura do dashboard...")
    
    try:
        # Verifica se o arquivo dashboard existe e é válido Python
        dashboard_path = "dashboard_trading_pro_real.py"
        
        if not os.path.exists(dashboard_path):
            print(f"❌ Arquivo {dashboard_path} não encontrado")
            return False
        
        print(f"✅ Arquivo {dashboard_path} encontrado")
        
        # Tenta compilar o arquivo
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        compile(code, dashboard_path, 'exec')
        print("✅ Dashboard compila sem erros de sintaxe")
        
        # Verifica se contém as novas funcionalidades
        if 'render_segunda_selecao' in code:
            print("✅ Função render_segunda_selecao encontrada")
        else:
            print("❌ Função render_segunda_selecao NÃO encontrada")
            return False
        
        if 'calcular_residuo_zscore_timeframe01' in code:
            print("✅ Referência a calcular_residuo_zscore_timeframe01 encontrada")
        else:
            print("❌ Referência a calcular_residuo_zscore_timeframe01 NÃO encontrada")
            return False
        
        if 'tabela_linha_operacao01' in code:
            print("✅ Referência a tabela_linha_operacao01 encontrada")
        else:
            print("❌ Referência a tabela_linha_operacao01 NÃO encontrada")
            return False
        
        return True
        
    except SyntaxError as e:
        print(f"❌ Erro de sintaxe no dashboard: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro ao testar dashboard: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🚀 TESTE DA IMPLEMENTAÇÃO DA SEGUNDA SELEÇÃO")
    print("=" * 60)
    
    resultados = []
    
    # Executa testes
    resultados.append(("Importações", test_imports()))
    resultados.append(("Sistema de Trading", test_trading_system()))
    resultados.append(("Funções de Análise", test_analysis_functions()))
    resultados.append(("Estrutura do Dashboard", test_dashboard_structure()))
    
    # Mostra resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES:")
    print("=" * 60)
    
    sucesso_total = True
    for nome, resultado in resultados:
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{nome:<25} {status}")
        if not resultado:
            sucesso_total = False
    
    print("=" * 60)
    
    if sucesso_total:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("🚀 Dashboard está pronto para usar a segunda seleção")
    else:
        print("⚠️ ALGUNS TESTES FALHARAM")
        print("🔧 Verifique os erros acima antes de usar o dashboard")
    
    print("=" * 60)
    
    return sucesso_total

if __name__ == "__main__":
    main()
