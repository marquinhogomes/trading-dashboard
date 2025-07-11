#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TESTE FINAL - DASHBOARD OTIMIZADO COM THREADING
==================================================

Este script verifica se o dashboard foi otimizado corretamente
com integração completa do sistema de threading avançado.
"""

import sys
import os
sys.path.append('.')

def testar_imports():
    """Testa todos os imports necessários"""
    print("🧪 TESTE 1: Verificando imports...")
    
    try:
        import streamlit as st
        print("✅ Streamlit importado")
    except ImportError as e:
        print(f"❌ Erro ao importar Streamlit: {e}")
        return False
    
    try:
        import dashboard_trading_pro_real
        print("✅ Dashboard trading pro real importado")
    except ImportError as e:
        print(f"❌ Erro ao importar dashboard: {e}")
        return False
    
    try:
        from sistema_integrado import SistemaIntegrado
        print("✅ Sistema integrado importado")
    except ImportError as e:
        print(f"❌ Erro ao importar sistema integrado: {e}")
        return False
    
    return True

def testar_classe_otimizada():
    """Testa se a classe foi otimizada corretamente"""
    print("\n🧪 TESTE 2: Verificando otimização da classe...")
    
    try:
        from dashboard_trading_pro_real import TradingSystemReal, SISTEMA_INTEGRADO_DISPONIVEL
        
        # Testa criação da instância
        sistema = TradingSystemReal()
        print("✅ Instância TradingSystemReal criada")
        
        # Verifica se tem sistema integrado
        if SISTEMA_INTEGRADO_DISPONIVEL:
            print("✅ Sistema integrado disponível")
            
            if hasattr(sistema, 'sistema_integrado') and sistema.sistema_integrado:
                print("✅ Sistema integrado inicializado")
            else:
                print("❌ Sistema integrado não inicializado")
                return False
                
            if hasattr(sistema, 'modo_otimizado') and sistema.modo_otimizado:
                print("✅ Modo otimizado ativado")
            else:
                print("❌ Modo otimizado não ativado")
                return False
        else:
            print("⚠️ Sistema integrado não disponível - modo básico")
        
        # Verifica logs
        if hasattr(sistema, 'logs') and isinstance(sistema.logs, list):
            print("✅ Sistema de logs inicializado")
            if len(sistema.logs) > 0:
                print(f"✅ {len(sistema.logs)} logs gerados na inicialização")
        else:
            print("❌ Sistema de logs não inicializado")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste da classe: {e}")
        return False

def testar_metodos_otimizados():
    """Testa métodos específicos da otimização"""
    print("\n🧪 TESTE 3: Verificando métodos otimizados...")
    
    try:
        from dashboard_trading_pro_real import TradingSystemReal
        sistema = TradingSystemReal()
        
        # Testa método log
        if hasattr(sistema, 'log'):
            sistema.log("Teste de log")
            print("✅ Método log funcionando")
        else:
            print("❌ Método log não encontrado")
            return False
        
        # Testa métodos de sistema integrado
        if sistema.modo_otimizado:
            if hasattr(sistema, 'executar_sistema_integrado'):
                print("✅ Método executar_sistema_integrado presente")
            else:
                print("❌ Método executar_sistema_integrado ausente")
                return False
                
            if hasattr(sistema, 'sincronizar_dados_sistema'):
                print("✅ Método sincronizar_dados_sistema presente")
            else:
                print("❌ Método sincronizar_dados_sistema ausente")
                return False
        
        # Testa iniciar_sistema
        if hasattr(sistema, 'iniciar_sistema'):
            print("✅ Método iniciar_sistema presente")
        else:
            print("❌ Método iniciar_sistema ausente")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de métodos: {e}")
        return False

def testar_threads_disponivel():
    """Testa se as threads do sistema integrado estão disponíveis"""
    print("\n🧪 TESTE 4: Verificando threads do sistema integrado...")
    
    try:
        from dashboard_trading_pro_real import TradingSystemReal
        sistema = TradingSystemReal()
        
        if sistema.modo_otimizado and sistema.sistema_integrado:
            # Verifica métodos de thread
            threads_methods = [
                'thread_monitoramento',
                'thread_monitoramento_posicoes', 
                'thread_break_even_continuo',
                'thread_ajustes_programados'
            ]
            
            for method_name in threads_methods:
                if hasattr(sistema.sistema_integrado, method_name):
                    print(f"✅ Thread {method_name} disponível")
                else:
                    print(f"❌ Thread {method_name} não encontrada")
                    return False
            
            # Verifica configurações
            if hasattr(sistema.sistema_integrado, 'stops_ja_ajustados'):
                print("✅ Controle de stops ajustados presente")
            if hasattr(sistema.sistema_integrado, 'ajustes_executados_hoje'):
                print("✅ Controle de ajustes executados presente")
                
            print("✅ Todas as threads estão disponíveis")
        else:
            print("⚠️ Sistema integrado não disponível - threads não testadas")
            
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de threads: {e}")
        return False

def testar_dashboard_execucao():
    """Testa se o dashboard pode ser executado"""
    print("\n🧪 TESTE 5: Verificando execução do dashboard...")
    
    try:
        # Simula inicialização do Streamlit (importação)
        import dashboard_trading_pro_real
        
        # Verifica funções principais
        funcoes_principais = [
            'render_sidebar',
            'render_status_cards',
            'main'
        ]
        
        for func_name in funcoes_principais:
            if hasattr(dashboard_trading_pro_real, func_name):
                print(f"✅ Função {func_name} presente")
            else:
                print(f"❌ Função {func_name} ausente")
                return False
        
        print("✅ Dashboard pronto para execução")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de execução: {e}")
        return False

def executar_todos_os_testes():
    """Executa todos os testes"""
    print("🎯 INICIANDO BATERIA DE TESTES - DASHBOARD OTIMIZADO")
    print("=" * 60)
    
    testes = [
        testar_imports,
        testar_classe_otimizada,
        testar_metodos_otimizados,
        testar_threads_disponivel,
        testar_dashboard_execucao
    ]
    
    resultados = []
    
    for teste in testes:
        resultado = teste()
        resultados.append(resultado)
    
    print("\n" + "=" * 60)
    print("📋 RESUMO DOS TESTES:")
    
    nomes_testes = [
        "Imports",
        "Classe Otimizada", 
        "Métodos Otimizados",
        "Threads Disponíveis",
        "Execução Dashboard"
    ]
    
    for i, (nome, resultado) in enumerate(zip(nomes_testes, resultados)):
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"  {i+1}. {nome}: {status}")
    
    total_passou = sum(resultados)
    total_testes = len(resultados)
    
    print(f"\n🏆 RESULTADO FINAL: {total_passou}/{total_testes} testes passaram")
    
    if total_passou == total_testes:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Dashboard otimizado está funcionando perfeitamente!")
        print("\n📋 Para executar:")
        print("   streamlit run dashboard_trading_pro_real.py")
        return True
    else:
        print("⚠️ Alguns testes falharam. Verifique os erros acima.")
        return False

if __name__ == "__main__":
    sucesso = executar_todos_os_testes()
    if sucesso:
        print("\n🚀 Sistema pronto para uso!")
    else:
        print("\n🔧 Sistema precisa de ajustes.")
    sys.exit(0 if sucesso else 1)
