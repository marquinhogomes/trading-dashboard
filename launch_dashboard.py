#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 LAUNCHER PARA O DASHBOARD WALL STREET LEVEL
Este script facilita a inicialização do dashboard profissional
"""

import os
import sys
import subprocess

def main():
    """Launcher principal para o dashboard."""
    print("🎯 Iniciando Sistema de Trading Profissional - Wall Street Level")
    print("=" * 60)
    
    # Verificar se estamos no diretório correto
    dashboard_file = "trading_dashboard_fixed.py"
    if not os.path.exists(dashboard_file):
        print(f"❌ Erro: Arquivo {dashboard_file} não encontrado!")
        print("Certifique-se de estar no diretório correto do projeto.")
        return
    
    print(f"✅ Dashboard encontrado: {dashboard_file}")
    print("🚀 Iniciando Streamlit...")
    print("📊 O dashboard será aberto automaticamente no seu navegador")
    print("💡 Para parar o servidor, pressione Ctrl+C")
    print("=" * 60)
    
    try:
        # Executar o dashboard
        cmd = [sys.executable, "-m", "streamlit", "run", dashboard_file]
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 Dashboard encerrado pelo usuário")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar o dashboard: {e}")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main()
