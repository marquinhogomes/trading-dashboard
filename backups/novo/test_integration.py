#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TESTE DE INTEGRAÇÃO COMPLETO - TRADING SYSTEM PRO
Script para verificar todas as dependências e integrações do sistema
"""

import sys
import os
import time
from datetime import datetime

def print_header():
    """Imprime cabeçalho do teste"""
    print("=" * 80)
    print("🚀 TRADING SYSTEM PRO - TESTE DE INTEGRAÇÃO COMPLETO")
    print("=" * 80)
    print(f"⏰ Iniciado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

def test_python_version():
    """Testa versão do Python"""
    print("📍 1. Testando versão do Python...")
    
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("   ✅ Versão do Python compatível")
        return True
    else:
        print("   ❌ Versão do Python não compatível (mínimo: 3.8)")
        return False

def test_core_packages():
    """Testa pacotes essenciais"""
    print("\n📍 2. Testando pacotes essenciais...")
    
    essential_packages = [
        ('streamlit', '1.28.0'),
        ('pandas', '2.0.0'),
        ('numpy', '1.24.0'),
        ('plotly', '5.15.0'),
        ('matplotlib', '3.7.0'),
        ('scipy', '1.10.0')
    ]
    
    all_ok = True
    
    for package, min_version in essential_packages:
        try:
            module = __import__(package)
            if hasattr(module, '__version__'):
                version = module.__version__
                print(f"   ✅ {package}: {version}")
            else:
                print(f"   ✅ {package}: importado com sucesso")
        except ImportError:
            print(f"   ❌ {package}: NÃO ENCONTRADO")
            all_ok = False
        except Exception as e:
            print(f"   ⚠️ {package}: erro na importação - {e}")
            all_ok = False
    
    return all_ok

def test_statistical_packages():
    """Testa pacotes estatísticos"""
    print("\n📍 3. Testando pacotes estatísticos...")
    
    stat_packages = [
        'statsmodels',
        'arch',
        'sklearn',
        'seaborn'
    ]
    
    all_ok = True
    
    for package in stat_packages:
        try:
            module = __import__(package)
            if hasattr(module, '__version__'):
                version = module.__version__
                print(f"   ✅ {package}: {version}")
            else:
                print(f"   ✅ {package}: importado com sucesso")
        except ImportError:
            print(f"   ⚠️ {package}: não encontrado (opcional)")
        except Exception as e:
            print(f"   ⚠️ {package}: erro na importação - {e}")
    
    return all_ok

def test_mt5_integration():
    """Testa integração com MetaTrader 5"""
    print("\n📍 4. Testando integração MetaTrader 5...")
    
    try:
        import MetaTrader5 as mt5
        print("   ✅ MetaTrader5 importado com sucesso")
        
        # Tentar inicializar (sem conectar)
        if mt5.initialize():
            print("   ✅ MT5 inicializado com sucesso")
            mt5.shutdown()
            return True
        else:
            print("   ⚠️ MT5 não pode ser inicializado (normal se não instalado)")
            return False
            
    except ImportError:
        print("   ⚠️ MetaTrader5 não encontrado (instalação opcional)")
        return False
    except Exception as e:
        print(f"   ⚠️ Erro no teste MT5: {e}")
        return False

def test_local_modules():
    """Testa módulos locais do sistema"""
    print("\n📍 5. Testando módulos locais...")
    
    # Adicionar diretório atual ao path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    local_modules = [
        'sistema_integrado',
        'calculo_entradas_v55',
        'dashboard_trading_pro'
    ]
    
    results = {}
    
    for module_name in local_modules:
        try:
            if os.path.exists(f"{module_name}.py"):
                # Testar importação
                module = __import__(module_name)
                print(f"   ✅ {module_name}: importado com sucesso")
                results[module_name] = True
                
                # Verificar classes principais
                if module_name == 'sistema_integrado':
                    if hasattr(module, 'SistemaIntegrado'):
                        print("   ✅ Classe SistemaIntegrado encontrada")
                    else:
                        print("   ⚠️ Classe SistemaIntegrado não encontrada")
                
            else:
                print(f"   ❌ {module_name}.py: arquivo não encontrado")
                results[module_name] = False
                
        except ImportError as e:
            print(f"   ❌ {module_name}: erro de importação - {e}")
            results[module_name] = False
        except Exception as e:
            print(f"   ⚠️ {module_name}: erro inesperado - {e}")
            results[module_name] = False
    
    return results

def test_dashboard_functionality():
    """Testa funcionalidades básicas do dashboard"""
    print("\n📍 6. Testando funcionalidades do dashboard...")
    
    try:
        # Importar o dashboard
        import dashboard_trading_pro
        print("   ✅ Dashboard importado com sucesso")
        
        # Verificar funções principais
        required_functions = [
            'initialize_session_state',
            'render_header',
            'render_system_status',
            'main'
        ]
        
        all_functions_ok = True
        for func_name in required_functions:
            if hasattr(dashboard_trading_pro, func_name):
                print(f"   ✅ Função {func_name} encontrada")
            else:
                print(f"   ❌ Função {func_name} não encontrada")
                all_functions_ok = False
        
        return all_functions_ok
        
    except Exception as e:
        print(f"   ❌ Erro ao testar dashboard: {e}")
        return False

def test_streamlit_compatibility():
    """Testa compatibilidade com Streamlit"""
    print("\n📍 7. Testando compatibilidade com Streamlit...")
    
    try:
        import streamlit as st
        print("   ✅ Streamlit importado")
        
        # Verificar versão
        version = st.__version__
        major, minor = map(int, version.split('.')[:2])
        
        if major >= 1 and minor >= 28:
            print(f"   ✅ Streamlit {version} é compatível")
            return True
        else:
            print(f"   ⚠️ Streamlit {version} pode ter problemas (recomendado: 1.28+)")
            return True
            
    except Exception as e:
        print(f"   ❌ Erro no teste Streamlit: {e}")
        return False

def test_file_permissions():
    """Testa permissões de arquivo"""
    print("\n📍 8. Testando permissões de arquivo...")
    
    try:
        # Testar criação de arquivo temporário
        test_file = "test_permissions.tmp"
        
        with open(test_file, 'w') as f:
            f.write("teste")
        
        # Testar leitura
        with open(test_file, 'r') as f:
            content = f.read()
        
        # Remover arquivo de teste
        os.remove(test_file)
        
        print("   ✅ Permissões de arquivo OK")
        return True
        
    except Exception as e:
        print(f"   ❌ Problema com permissões: {e}")
        return False

def generate_system_report(results):
    """Gera relatório final do sistema"""
    print("\n" + "=" * 80)
    print("📊 RELATÓRIO FINAL DO SISTEMA")
    print("=" * 80)
    
    total_tests = 8
    passed_tests = sum([
        results['python_version'],
        results['core_packages'],
        results['statistical_packages'],
        results['mt5_integration'],
        bool(results['local_modules'].get('dashboard_trading_pro', False)),
        results['dashboard_functionality'],
        results['streamlit_compatibility'],
        results['file_permissions']
    ])
    
    success_rate = (passed_tests / total_tests) * 100
    
    print(f"✅ Testes passados: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
    print()
    
    # Status dos componentes
    print("🔧 STATUS DOS COMPONENTES:")
    print(f"   Python: {'✅' if results['python_version'] else '❌'}")
    print(f"   Pacotes essenciais: {'✅' if results['core_packages'] else '❌'}")
    print(f"   Pacotes estatísticos: {'✅' if results['statistical_packages'] else '⚠️'}")
    print(f"   MetaTrader 5: {'✅' if results['mt5_integration'] else '⚠️'}")
    print(f"   Sistema integrado: {'✅' if results['local_modules'].get('sistema_integrado') else '❌'}")
    print(f"   Cálculo de entradas: {'✅' if results['local_modules'].get('calculo_entradas_v55') else '❌'}")
    print(f"   Dashboard: {'✅' if results['dashboard_functionality'] else '❌'}")
    print(f"   Streamlit: {'✅' if results['streamlit_compatibility'] else '❌'}")
    print(f"   Permissões: {'✅' if results['file_permissions'] else '❌'}")
    print()
    
    # Recomendações
    print("💡 RECOMENDAÇÕES:")
    
    if not results['core_packages']:
        print("   📦 Instale os pacotes essenciais: pip install streamlit pandas numpy plotly matplotlib scipy")
    
    if not results['statistical_packages']:
        print("   📊 Instale pacotes estatísticos: pip install statsmodels arch scikit-learn seaborn")
    
    if not results['mt5_integration']:
        print("   🔌 Para trading real, instale MetaTrader5: pip install MetaTrader5")
    
    if not results['local_modules'].get('sistema_integrado'):
        print("   ⚙️ Verifique se sistema_integrado.py está no diretório")
    
    if success_rate >= 80:
        print("\n🎉 SISTEMA PRONTO PARA USO!")
        print("   Execute: streamlit run dashboard_trading_pro.py")
    elif success_rate >= 60:
        print("\n⚠️ SISTEMA FUNCIONAL COM LIMITAÇÕES")
        print("   Algumas funcionalidades podem estar limitadas")
    else:
        print("\n❌ SISTEMA REQUER CONFIGURAÇÃO ADICIONAL")
        print("   Resolva os problemas listados acima")
    
    print()
    print("🚀 Para iniciar o dashboard:")
    print("   streamlit run dashboard_trading_pro.py --server.port 8501")

def main():
    """Função principal do teste"""
    print_header()
    
    # Executar todos os testes
    results = {}
    
    results['python_version'] = test_python_version()
    results['core_packages'] = test_core_packages()
    results['statistical_packages'] = test_statistical_packages()
    results['mt5_integration'] = test_mt5_integration()
    results['local_modules'] = test_local_modules()
    results['dashboard_functionality'] = test_dashboard_functionality()
    results['streamlit_compatibility'] = test_streamlit_compatibility()
    results['file_permissions'] = test_file_permissions()
    
    # Gerar relatório final
    generate_system_report(results)
    
    print(f"\n⏰ Teste concluído em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

if __name__ == "__main__":
    main()
