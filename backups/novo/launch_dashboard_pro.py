#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 LAUNCHER - TRADING SYSTEM PRO DASHBOARD
Launcher script para executar o dashboard com configurações otimizadas
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    required_packages = [
        'streamlit',
        'pandas',
        'numpy',
        'plotly',
        'statsmodels'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Dependências faltando:")
        for pkg in missing_packages:
            print(f"   - {pkg}")
        print("\n💡 Execute:")
        print("   pip install -r requirements_dashboard_pro.txt")
        return False
    
    return True

def launch_dashboard():
    """Lança o dashboard Streamlit"""
    dashboard_file = Path("dashboard_trading_pro.py")
    
    if not dashboard_file.exists():
        print("❌ Arquivo dashboard_trading_pro.py não encontrado!")
        return False
    
    print("🚀 Iniciando Trading System Pro Dashboard...")
    print("📱 O dashboard abrirá automaticamente no seu navegador")
    print("🌐 URL: http://localhost:8501")
    print("⏹️  Para parar, pressione Ctrl+C")
    print("-" * 60)
    
    # Configurações otimizadas do Streamlit
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        str(dashboard_file),
        "--server.port=8501",
        "--server.address=localhost",
        "--browser.serverAddress=localhost",
        "--browser.gatherUsageStats=false",
        "--server.maxUploadSize=200",
        "--theme.base=dark",
        "--theme.primaryColor=#1e3c72",
        "--theme.backgroundColor=#0e1117",
        "--theme.secondaryBackgroundColor=#262730",
        "--theme.textColor=#fafafa"
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n✅ Dashboard finalizado pelo usuário")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar dashboard: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False
    
    return True

def main():
    """Função principal do launcher"""
    print("=" * 60)
    print("🏛️  TRADING SYSTEM PRO - DASHBOARD LAUNCHER")
    print("=" * 60)
    
    # Verificar dependências
    if not check_dependencies():
        return 1
    
    print("✅ Todas as dependências estão instaladas")
    time.sleep(1)
    
    # Lançar dashboard
    if not launch_dashboard():
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
