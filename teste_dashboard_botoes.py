#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para verificar o funcionamento do sistema integrado
e diagnosticar problemas com os botões do dashboard.
"""

import sys
import os
import traceback
from datetime import datetime

def testar_sistema_integrado():
    """Testa a criação e funcionamento do sistema integrado"""
    print("="*60)
    print("DIAGNÓSTICO DO SISTEMA INTEGRADO")
    print("="*60)
    
    # Teste 1: Importação do módulo
    try:
        print("\n1. Testando importação do sistema_integrado...")
        from sistema_integrado import SistemaIntegrado
        print("✅ Importação bem-sucedida")
    except Exception as e:
        print(f"❌ Erro na importação: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False
    
    # Teste 2: Criação da instância
    try:
        print("\n2. Testando criação da instância...")
        sistema = SistemaIntegrado()
        print("✅ Instância criada com sucesso")
    except Exception as e:
        print(f"❌ Erro na criação: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False
    
    # Teste 3: Verificação dos atributos essenciais
    try:
        print("\n3. Testando atributos essenciais...")
        
        # Verifica se os atributos necessários existem
        atributos_necessarios = [
            'running', 'analysis_thread', 'analysis_thread_lock', 
            'analysis_thread_stop_event', 'logs', 'dados_sistema'
        ]
        
        for attr in atributos_necessarios:
            if not hasattr(sistema, attr):
                print(f"❌ Atributo '{attr}' não encontrado")
                return False
            else:
                print(f"✅ Atributo '{attr}' encontrado")
        
        print("✅ Todos os atributos essenciais estão presentes")
        
    except Exception as e:
        print(f"❌ Erro na verificação de atributos: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False
    
    # Teste 4: Verificação dos métodos de análise
    try:
        print("\n4. Testando métodos de análise...")
        
        # Verifica se os métodos necessários existem
        metodos_necessarios = [
            'start_analysis_thread', 'stop_analysis_thread', 
            'is_analysis_running', 'log'
        ]
        
        for metodo in metodos_necessarios:
            if not hasattr(sistema, metodo):
                print(f"❌ Método '{metodo}' não encontrado")
                return False
            elif not callable(getattr(sistema, metodo)):
                print(f"❌ Método '{metodo}' não é callable")
                return False
            else:
                print(f"✅ Método '{metodo}' encontrado e callable")
        
        print("✅ Todos os métodos essenciais estão presentes")
        
    except Exception as e:
        print(f"❌ Erro na verificação de métodos: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False
    
    # Teste 5: Teste de start/stop da análise
    try:
        print("\n5. Testando start/stop da análise...")
        
        # Verifica estado inicial
        print(f"Estado inicial da análise: {sistema.is_analysis_running()}")
        
        # Tenta iniciar a análise
        config_teste = {
            'zscore_min': 2.0,
            'zscore_max': 6.5,
            'max_posicoes': 5,
            'valor_operacao': 10000
        }
        
        print("Iniciando análise...")
        resultado = sistema.start_analysis_thread(config=config_teste)
        print(f"Resultado do start_analysis_thread: {resultado}")
        
        # Aguarda um pouco
        import time
        time.sleep(1)
        
        # Verifica se está rodando
        is_running = sistema.is_analysis_running()
        print(f"Estado após iniciar: {is_running}")
        
        if is_running:
            print("✅ Análise iniciada com sucesso")
            
            # Tenta parar
            print("Parando análise...")
            sistema.stop_analysis_thread()
            
            # Aguarda um pouco
            time.sleep(1)
            
            # Verifica se parou
            is_running_after_stop = sistema.is_analysis_running()
            print(f"Estado após parar: {is_running_after_stop}")
            
            if not is_running_after_stop:
                print("✅ Análise parada com sucesso")
            else:
                print("⚠️ Análise pode ainda estar rodando")
        else:
            print("❌ Análise não iniciou corretamente")
            
    except Exception as e:
        print(f"❌ Erro no teste de start/stop: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False
    
    # Teste 6: Verificação de logs
    try:
        print("\n6. Testando sistema de logs...")
        
        sistema.log("Teste de log do sistema integrado")
        
        if hasattr(sistema, 'logs') and len(sistema.logs) > 0:
            print("✅ Sistema de logs funcionando")
            print(f"Último log: {sistema.logs[-1]}")
        else:
            print("❌ Sistema de logs não funcionando")
            
    except Exception as e:
        print(f"❌ Erro no teste de logs: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False
    
    print("\n" + "="*60)
    print("DIAGNÓSTICO CONCLUÍDO COM SUCESSO")
    print("="*60)
    
    return True

def testar_dashboard_integration():
    """Testa a integração com o dashboard"""
    print("\n" + "="*60)
    print("TESTANDO INTEGRAÇÃO COM O DASHBOARD")
    print("="*60)
    
    try:
        print("\n1. Testando criação da classe TradingSystemReal...")
        
        # Simula a criação como no dashboard
        sys.path.append('.')
        
        # Importa e cria a classe TradingSystemReal
        exec(open('dashboard_trading_pro_real.py').read(), globals())
        
        # Cria uma instância como no dashboard
        trading_system = TradingSystemReal()
        print("✅ TradingSystemReal criada com sucesso")
        
        # Teste de criação do sistema integrado
        print("\n2. Testando criação do sistema integrado via dashboard...")
        
        if hasattr(trading_system, 'criar_sistema_integrado'):
            trading_system.criar_sistema_integrado()
            
            if hasattr(trading_system, 'sistema_integrado') and trading_system.sistema_integrado is not None:
                print("✅ Sistema integrado criado via dashboard")
                
                # Testa os métodos como no dashboard
                print("\n3. Testando métodos como no dashboard...")
                
                # Simula o fluxo do botão "Iniciar Análise"
                config_temp = {
                    'zscore_min': 2.0,
                    'zscore_max': 6.5,
                    'max_posicoes': 5,
                    'valor_operacao': 10000
                }
                
                # Tenta iniciar como no dashboard
                started = trading_system.sistema_integrado.start_analysis_thread(config=config_temp)
                print(f"Resultado do start_analysis_thread: {started}")
                
                # Verifica se está rodando
                import time
                time.sleep(1)
                
                analysis_running = trading_system.sistema_integrado.is_analysis_running()
                print(f"Estado da análise: {analysis_running}")
                
                if analysis_running:
                    print("✅ Fluxo do dashboard funcionando corretamente")
                    
                    # Para a análise
                    trading_system.sistema_integrado.stop_analysis_thread()
                    time.sleep(1)
                    
                    analysis_running_after = trading_system.sistema_integrado.is_analysis_running()
                    print(f"Estado após parar: {analysis_running_after}")
                    
                else:
                    print("❌ Fluxo do dashboard não funcionando")
                    
            else:
                print("❌ Sistema integrado não foi criado via dashboard")
                
        else:
            print("❌ Método criar_sistema_integrado não encontrado")
            
    except Exception as e:
        print(f"❌ Erro no teste de integração: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False
    
    return True

if __name__ == "__main__":
    print(f"Iniciando diagnóstico em {datetime.now()}")
    print(f"Python: {sys.version}")
    print(f"Diretório atual: {os.getcwd()}")
    
    # Executa os testes
    teste1_ok = testar_sistema_integrado()
    teste2_ok = testar_dashboard_integration()
    
    print("\n" + "="*60)
    print("RESUMO DOS TESTES")
    print("="*60)
    print(f"Teste do Sistema Integrado: {'✅ PASSOU' if teste1_ok else '❌ FALHOU'}")
    print(f"Teste de Integração Dashboard: {'✅ PASSOU' if teste2_ok else '❌ FALHOU'}")
    
    if teste1_ok and teste2_ok:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("O problema pode estar na interface Streamlit ou na lógica de rerun.")
    else:
        print("\n⚠️ ALGUNS TESTES FALHARAM!")
        print("Verifique os erros acima para identificar o problema.")
