#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 LAUNCHER DO DASHBOARD TRADING PRO
Script simples para iniciar o dashboard com verificações
"""

import subprocess
import sys
import os
import time
import webbrowser
from datetime import datetime

def check_dependencies():
    """Verifica dependências básicas"""
    print("🔍 Verificando dependências...")
    
    try:
        import streamlit
        print(f"✅ Streamlit {streamlit.__version__} encontrado")
        return True
    except ImportError:
        print("❌ Streamlit não encontrado!")
        print("💡 Instale com: pip install streamlit")
        return False

def start_dashboard():
    """Inicia o dashboard Streamlit"""
    print("\n🚀 Iniciando Trading System Pro Dashboard...")
    print("=" * 50)
    
    # Comando para iniciar o Streamlit
    cmd = [
        sys.executable, "-m", "streamlit", "run", 
        "dashboard_trading_pro.py",
        "--server.port", "8501",
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false"
    ]
    
    try:
        print("⏳ Iniciando servidor Streamlit...")
        
        # Executar comando
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.getcwd()
        )
        
        # Esperar um pouco para o servidor iniciar
        time.sleep(3)
        
        # Verificar se o processo ainda está rodando
        if process.poll() is None:
            print("✅ Dashboard iniciado com sucesso!")
            print("\n📱 Acesse o dashboard em:")
            print("   🌐 http://localhost:8501")
            print("\n⏹️ Para parar, pressione Ctrl+C neste terminal")
            
            # Tentar abrir automaticamente no navegador
            try:
                webbrowser.open("http://localhost:8501")
                print("🌐 Abrindo navegador automaticamente...")
            except:
                print("ℹ️ Abra manualmente: http://localhost:8501")
            
            # Aguardar término do processo
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n⏹️ Parando dashboard...")
                process.terminate()
                print("✅ Dashboard parado!")
                
        else:
            # Processo falhou, mostrar erro
            stdout, stderr = process.communicate()
            print("❌ Falha ao iniciar dashboard!")
            if stderr:
                print(f"Erro: {stderr}")
            
    except FileNotFoundError:
        print("❌ Python ou Streamlit não encontrados no PATH!")
        print("💡 Verifique a instalação do Python e Streamlit")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

def main():
    """Função principal"""
    print("🚀 TRADING SYSTEM PRO - LAUNCHER")
    print("=" * 40)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Verificar dependências
    if not check_dependencies():
        print("\n❌ Dependências não atendidas!")
        input("Pressione Enter para sair...")
        return
    
    # Verificar se o arquivo do dashboard existe
    if not os.path.exists("dashboard_trading_pro.py"):
        print("❌ Arquivo dashboard_trading_pro.py não encontrado!")
        print("💡 Execute este script no mesmo diretório do dashboard")
        input("Pressione Enter para sair...")
        return
    
    # Iniciar dashboard
    start_dashboard()

if __name__ == "__main__":
    main()
