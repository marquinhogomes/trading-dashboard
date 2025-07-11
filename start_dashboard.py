#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 INICIALIZADOR DO DASHBOARD TRADING PRO
Script Python para iniciar o dashboard com todas as verificações necessárias
"""

import subprocess
import sys
import os
import time
import webbrowser
from datetime import datetime

def print_header():
    """Imprime cabeçalho do launcher"""
    print("=" * 60)
    print("🚀 TRADING SYSTEM PRO - DASHBOARD LAUNCHER")
    print("=" * 60)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatível")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Incompatível")
        print("💡 Necessário Python 3.8 ou superior")
        return False

def check_and_install_dependencies():
    """Verifica e instala dependências necessárias"""
    print("\n📦 Verificando dependências...")
    
    required_packages = [
        'streamlit',
        'pandas', 
        'numpy',
        'plotly',
        'matplotlib',
        'seaborn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - não encontrado")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📥 Instalando {len(missing_packages)} pacotes faltantes...")
        
        for package in missing_packages:
            try:
                print(f"   Instalando {package}...")
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", package
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"   ✅ {package} instalado com sucesso")
            except subprocess.CalledProcessError:
                print(f"   ❌ Falha ao instalar {package}")
                return False
    
    print("✅ Todas as dependências estão disponíveis!")
    return True

def check_dashboard_file():
    """Verifica se o arquivo do dashboard existe"""
    dashboard_file = "dashboard_trading_pro.py"
    
    if os.path.exists(dashboard_file):
        print(f"✅ Arquivo {dashboard_file} encontrado")
        return True
    else:
        print(f"❌ Arquivo {dashboard_file} não encontrado!")
        print("💡 Certifique-se de estar no diretório correto")
        return False

def start_streamlit_dashboard():
    """Inicia o dashboard Streamlit"""
    print("\n🚀 Iniciando Dashboard...")
    print("-" * 40)
    
    # Comando para iniciar o Streamlit
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        "dashboard_trading_pro.py",
        "--server.port", "8501",
        "--server.headless", "false",
        "--browser.gatherUsageStats", "false"
    ]
    
    try:
        print("⏳ Iniciando servidor Streamlit...")
        print("🌐 O dashboard será aberto automaticamente no navegador")
        print("📱 URL: http://localhost:8501")
        print("\n⏹️ Para parar o dashboard, pressione Ctrl+C")
        print("=" * 60)
        
        # Executar o comando
        result = subprocess.run(cmd, cwd=os.getcwd())
        
        if result.returncode == 0:
            print("\n✅ Dashboard encerrado normalmente")
        else:
            print(f"\n⚠️ Dashboard encerrado com código {result.returncode}")
            
    except KeyboardInterrupt:
        print("\n⏹️ Dashboard interrompido pelo usuário")
    except FileNotFoundError:
        print("❌ Streamlit não encontrado!")
        print("💡 Instale com: pip install streamlit")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False
    
    return True

def run_quick_test():
    """Executa teste rápido do sistema"""
    print("\n🧪 Executando teste rápido...")
    
    try:
        # Teste de importação do dashboard
        import dashboard_trading_pro
        print("✅ Dashboard importado com sucesso")
        
        # Teste básico de funcionalidades
        if hasattr(dashboard_trading_pro, 'main'):
            print("✅ Função main encontrada")
        else:
            print("⚠️ Função main não encontrada")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erro ao importar dashboard: {e}")
        return False
    except Exception as e:
        print(f"⚠️ Erro no teste: {e}")
        return True  # Continuar mesmo com warnings

def main():
    """Função principal do launcher"""
    print_header()
    
    # 1. Verificar versão do Python
    if not check_python_version():
        input("\nPressione Enter para sair...")
        return
    
    # 2. Verificar e instalar dependências
    if not check_and_install_dependencies():
        print("\n❌ Falha na instalação de dependências!")
        input("Pressione Enter para sair...")
        return
    
    # 3. Verificar arquivo do dashboard
    if not check_dashboard_file():
        input("\nPressione Enter para sair...")
        return
    
    # 4. Executar teste rápido
    if not run_quick_test():
        print("\n⚠️ Teste falhou, mas tentando iniciar mesmo assim...")
    
    # 5. Iniciar dashboard
    print("\n🎯 Tudo pronto! Iniciando dashboard...")
    time.sleep(1)
    
    success = start_streamlit_dashboard()
    
    if success:
        print("\n✅ Obrigado por usar o Trading System Pro!")
    else:
        print("\n❌ Problemas durante a execução")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Execução interrompida pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        input("Pressione Enter para sair...")

def start_dashboard():
    """Inicia apenas o dashboard Streamlit"""
    print("🚀 Iniciando Dashboard de Trading...")
    print("📍 URL: http://localhost:8501")
    print("⚙️ Para parar: Ctrl+C")
    print("=" * 50)
    
    try:
        # Iniciar Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "trading_dashboard_real.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Dashboard parado pelo usuário")
    except Exception as e:
        print(f"\n❌ ERRO ao iniciar dashboard: {e}")

if __name__ == "__main__":
    start_dashboard()
