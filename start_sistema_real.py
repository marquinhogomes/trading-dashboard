#!/usr/bin/env python3
"""
Script de inicialização final - Sistema Real Integrado
Execute este arquivo para testar o sistema completo
"""

import os
import sys
from datetime import datetime

def banner():
    print("=" * 60)
    print("🎯 SISTEMA DE TRADING REAL v5.5")
    print("📊 Integração Completa com calculo_entradas_v55.py")
    print("⚡ Dados 100% Reais - Zero Simulação")
    print("=" * 60)
    print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()

def verificar_ambiente():
    """Verifica se o ambiente está pronto"""
    print("🔍 Verificando ambiente...")
    
    # Verificar arquivos essenciais
    arquivos_necessarios = [
        'config_real.py',
        'analise_real.py', 
        'trading_real_integration.py',
        'trading_dashboard_real.py',
        'calculo_entradas_v55.py'
    ]
    
    arquivos_encontrados = 0
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"   ✅ {arquivo}")
            arquivos_encontrados += 1
        else:
            print(f"   ❌ {arquivo} - FALTANDO!")
    
    print(f"\n📊 Status: {arquivos_encontrados}/{len(arquivos_necessarios)} arquivos encontrados")
    return arquivos_encontrados == len(arquivos_necessarios)

def testar_sistema():
    """Testa sistema completo"""
    print("\n🧪 Testando sistema...")
    
    try:
        # Teste 1: Configurações
        print("   1. Configurações reais...", end=" ")
        from config_real import DEPENDENTE_REAL, SYSTEM_INFO
        print(f"✅ ({len(DEPENDENTE_REAL)} ativos)")
        
        # Teste 2: Análise
        print("   2. Módulo de análise...", end=" ")
        from analise_real import get_analise_para_streamlit
        print("✅")
        
        # Teste 3: Integração
        print("   3. Sistema de integração...", end=" ")
        from trading_real_integration import get_real_system_status
        print("✅")
        
        # Teste 4: Dashboard
        print("   4. Dashboard Streamlit...", end=" ")
        import trading_dashboard_real
        print("✅")
        
        # Teste 5: Status
        print("   5. Status do sistema...", end=" ")
        status = get_real_system_status()
        print(f"✅ ({status.get('fonte', 'N/A')})")
        
        return True
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False

def menu_principal():
    """Menu principal do sistema"""
    print("\n🎯 SISTEMA PRONTO! Escolha uma opção:")
    print()
    print("1. 🚀 Executar Dashboard Streamlit")
    print("2. 🧪 Executar Teste Completo")
    print("3. 📊 Ver Status do Sistema")
    print("4. 📋 Ver Configurações")
    print("5. 🚪 Sair")
    print()
    
    escolha = input("Digite sua escolha (1-5): ").strip()
    
    if escolha == "1":
        print("\n🚀 Iniciando Dashboard Streamlit...")
        print("💡 O dashboard será aberto no seu navegador")
        print("🔗 URL: http://localhost:8501")
        input("\nPressione ENTER para continuar...")
        os.system("streamlit run trading_dashboard_real.py")
        
    elif escolha == "2":
        print("\n🧪 Executando teste completo...")
        os.system("python test_sistema_completo.py")
        input("\nPressione ENTER para continuar...")
        
    elif escolha == "3":
        print("\n📊 Status do Sistema:")
        try:
            from trading_real_integration import get_real_system_status
            status = get_real_system_status()
            for key, value in status.items():
                print(f"   {key}: {value}")
        except Exception as e:
            print(f"   ❌ Erro: {e}")
        input("\nPressione ENTER para continuar...")
        
    elif escolha == "4":
        print("\n📋 Configurações do Sistema:")
        try:
            from config_real import SYSTEM_INFO, DEPENDENTE_REAL, get_setores_disponiveis
            print(f"   Versão: {SYSTEM_INFO['version']}")
            print(f"   Ativos: {len(DEPENDENTE_REAL)}")
            print(f"   Setores: {len(get_setores_disponiveis())}")
            print(f"   Data extração: {SYSTEM_INFO['extracted_date']}")
        except Exception as e:
            print(f"   ❌ Erro: {e}")
        input("\nPressione ENTER para continuar...")
        
    elif escolha == "5":
        print("\n👋 Obrigado por usar o Sistema de Trading Real!")
        return False
        
    else:
        print("\n❌ Opção inválida!")
        input("Pressione ENTER para continuar...")
    
    return True

def main():
    """Função principal"""
    banner()
    
    # Verificar ambiente
    if not verificar_ambiente():
        print("\n❌ Ambiente não está pronto!")
        print("💡 Certifique-se de que todos os arquivos estão presentes")
        return
    
    # Testar sistema
    if not testar_sistema():
        print("\n❌ Sistema com problemas!")
        print("💡 Verifique os logs de erro acima")
        return
    
    # Menu interativo
    print("\n🎉 SISTEMA VALIDADO E PRONTO!")
    while True:
        if not menu_principal():
            break

if __name__ == "__main__":
    main()
