#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Launcher para Dashboard Trading Pro - MT5 Real
Inicia o dashboard Streamlit com configurações otimizadas
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas"""
    print("🔍 Verificando dependências...")
    
    dependencias_criticas = [
        'streamlit',
        'plotly',
        'pandas',
        'numpy',
        'MetaTrader5'
    ]
    
    faltando = []
    
    for dep in dependencias_criticas:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep}")
            faltando.append(dep)
    
    if faltando:
        print(f"\n⚠️  Dependências faltando: {', '.join(faltando)}")
        print("📋 Execute: pip install -r requirements_dashboard.txt")
        return False
    
    print("✅ Todas as dependências críticas estão instaladas!")
    return True

def configurar_ambiente():
    """Configura ambiente para o dashboard"""
    print("⚙️  Configurando ambiente...")
    
    # Configurações do Streamlit
    os.environ['STREAMLIT_SERVER_PORT'] = '8501'
    os.environ['STREAMLIT_SERVER_ADDRESS'] = 'localhost'
    os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    
    # Configurações do TensorFlow
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    
    # Configurações do Windows para UTF-8
    if os.name == 'nt':
        os.system('chcp 65001 > nul')
    
    print("✅ Ambiente configurado!")

def criar_config_streamlit():
    """Cria arquivo de configuração do Streamlit"""
    config_dir = Path.home() / '.streamlit'
    config_dir.mkdir(exist_ok=True)
    
    config_content = """
[server]
port = 8501
address = "localhost"
headless = false
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
serverAddress = "localhost"
serverPort = 8501

[theme]
primaryColor = "#2980b9"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[logger]
level = "info"
"""
    
    config_file = config_dir / 'config.toml'
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print(f"✅ Configuração do Streamlit criada em: {config_file}")

def iniciar_dashboard():
    """Inicia o dashboard Streamlit"""
    print("🚀 Iniciando Dashboard Trading Pro...")
    print("=" * 60)
    print("🏆 DASHBOARD TRADING PROFESSIONAL")
    print("📈 Sistema Completo de Trading MT5")
    print("🔗 URL: http://localhost:8501")
    print("=" * 60)
    
    # Comando para iniciar o Streamlit
    cmd = [
        sys.executable, 
        '-m', 'streamlit', 
        'run', 
        'dashboard_trading_pro_real.py',
        '--server.port=8501',
        '--server.address=localhost',
        '--browser.gatherUsageStats=false',
        '--server.headless=false'
    ]
    
    try:
        # Executa o comando
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao iniciar o dashboard: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Dashboard interrompido pelo usuário")
        return True
    
    return True

def main():
    """Função principal do launcher"""
    print("🎯 LAUNCHER - DASHBOARD TRADING PRO")
    print("Sistema Profissional de Trading MT5 Real")
    print("=" * 50)
    
    # Verifica se está no diretório correto
    if not os.path.exists('dashboard_trading_pro_real.py'):
        print("❌ Arquivo dashboard_trading_pro_real.py não encontrado!")
        print("💡 Execute este launcher no mesmo diretório do dashboard")
        input("Pressione Enter para sair...")
        return
    
    # Verifica dependências
    if not verificar_dependencias():
        print("\n💡 Para instalar dependências:")
        print("pip install -r requirements_dashboard.txt")
        input("Pressione Enter para sair...")
        return
    
    # Configura ambiente
    configurar_ambiente()
    
    # Cria configuração do Streamlit
    criar_config_streamlit()
    
    print("\n🎮 Controles:")
    print("- Ctrl+C: Parar o dashboard")
    print("- Browser: http://localhost:8501")
    print("- Logs: Visíveis no terminal")
    
    input("\nPressione Enter para iniciar o dashboard...")
    
    # Inicia dashboard
    sucesso = iniciar_dashboard()
    
    if sucesso:
        print("\n✅ Dashboard finalizado com sucesso!")
    else:
        print("\n❌ Dashboard finalizado com erro!")
    
    input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()
