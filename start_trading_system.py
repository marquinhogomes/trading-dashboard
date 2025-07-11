

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de inicialização do Sistema de Trading Streamlit
Execute este arquivo para iniciar o sistema completo
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    if sys.version_info < (3, 8):
        print("❌ ERRO: Python 3.8 ou superior é necessário")
        print(f"Versão atual: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    try:
        import streamlit
        import plotly
        import pandas
        import numpy
        import MetaTrader5
        print("✅ Dependências principais encontradas")
        return True
    except ImportError as e:
        print(f"❌ ERRO: Dependência não encontrada: {e}")
        print("Execute: pip install -r requirements_streamlit.txt")
        return False

def install_dependencies():
    """Instala as dependências automaticamente"""
    print("📦 Instalando dependências...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements_streamlit.txt"
        ])
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError:
        print("❌ ERRO: Falha na instalação das dependências")
        return False

def check_mt5():
    """Verifica se o MetaTrader 5 está disponível"""
    try:
        import MetaTrader5 as mt5
        # Tentativa de inicialização (pode falhar se não estiver configurado)
        result = mt5.initialize()
        if result:
            account_info = mt5.account_info()
            if account_info:
                print(f"✅ MT5 conectado: {account_info.company} - {account_info.server}")
            else:
                print("⚠️ MT5 disponível mas sem conta ativa")
            mt5.shutdown()
        else:
            print("⚠️ MT5 disponível mas não inicializado")
        return True
    except Exception as e:
        print(f"⚠️ MT5 não disponível: {e}")
        print("Instale o MetaTrader 5 para funcionalidade completa")
        return False

def create_directories():
    """Cria diretórios necessários"""
    directories = ['logs', 'data', 'exports', 'backups']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"📁 Diretório criado: {directory}")

def check_config():
    """Verifica se os arquivos de configuração existem"""
    config_files = [
        'config.py',
        'trading_core.py',
        'trading_system_streamlit.py'
    ]
    
    all_exist = True
    for file in config_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} não encontrado")
            all_exist = False
    
    return all_exist

def start_streamlit():
    """Inicia o servidor Streamlit"""
    print("\n🚀 Iniciando Sistema de Trading...")
    print("=" * 50)
    print("📍 URL: http://localhost:8501")
    print("⚙️ Para parar: Ctrl+C")
    print("=" * 50)
    
    try:
        # Iniciar Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "trading_system_streamlit.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--theme.base", "light"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Sistema parado pelo usuário")
    except Exception as e:
        print(f"\n❌ ERRO ao iniciar Streamlit: {e}")

def print_banner():
    """Imprime banner do sistema"""
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║          🚀 SISTEMA DE TRADING PROFISSIONAL 🚀          ║
    ║                                                          ║
    ║              Análise de Cointegração                     ║
    ║              Modelos ARIMA/GARCH                         ║
    ║              Execução Automatizada                       ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    """Função principal de inicialização"""
    print_banner()
    
    print("🔍 Verificando sistema...")
    
    # Verificações
    if not check_python_version():
        sys.exit(1)
    
    # Verificar configurações
    if not check_config():
        print("\n❌ ERRO: Arquivos de configuração não encontrados")
        print("Certifique-se de que todos os arquivos estão no diretório correto")
        sys.exit(1)
    
    # Verificar dependências
    if not check_dependencies():
        install = input("\n📦 Instalar dependências automaticamente? (s/n): ")
        if install.lower() in ['s', 'sim', 'y', 'yes']:
            if not install_dependencies():
                sys.exit(1)
        else:
            print("Execute: pip install -r requirements_streamlit.txt")
            sys.exit(1)
    
    # Verificar MT5
    check_mt5()
    
    # Criar diretórios
    create_directories()
    
    print("\n✅ Sistema verificado com sucesso!")
    
    # Aguardar confirmação
    input("\n🚀 Pressione ENTER para iniciar o sistema...")
    
    # Iniciar Streamlit
    start_streamlit()

if __name__ == "__main__":
    main()
