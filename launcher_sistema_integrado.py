#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 LAUNCHER DO SISTEMA DE TRADING INTEGRADO
============================================

Este script é o ponto de entrada único para executar todo o sistema de trading.
Ele verifica todos os componentes e inicia o dashboard integrado.

Autor: Sistema de IA Avançado
Data: 24/06/2025
Versão: 1.0 Final
"""

import os
import sys
import subprocess
import importlib.util
from pathlib import Path

def verificar_ambiente():
    """Verifica se o ambiente está configurado corretamente"""
    print("🔍 VERIFICANDO AMBIENTE DO SISTEMA...")
    print("=" * 50)
    
    # Verificar Python
    python_version = sys.version
    print(f"✅ Python: {python_version}")
    
    # Verificar arquivos essenciais
    arquivos_essenciais = [
        "dashboard_trading_integrado.py",
        "sistema_integrado.py",
        "calculo_entradas_v55.py"
    ]
    
    for arquivo in arquivos_essenciais:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo}: Encontrado")
        else:
            print(f"❌ {arquivo}: NÃO ENCONTRADO")
            return False
    
    # Verificar dependências críticas
    dependencias = [
        ("streamlit", "Interface web"),
        ("MetaTrader5", "Conexão com MT5"),
        ("pandas", "Manipulação de dados"),
        ("numpy", "Cálculos numéricos"),
        ("plotly", "Visualizações")
    ]
    
    print("\n📦 VERIFICANDO DEPENDÊNCIAS...")
    for nome, descricao in dependencias:
        try:
            spec = importlib.util.find_spec(nome)
            if spec is not None:
                print(f"✅ {nome}: {descricao}")
            else:
                print(f"❌ {nome}: NÃO ENCONTRADO - {descricao}")
                return False
        except ImportError:
            print(f"❌ {nome}: ERRO DE IMPORTAÇÃO - {descricao}")
            return False
    
    return True

def executar_dashboard():
    """Executa o dashboard integrado"""
    print("\n🚀 INICIANDO DASHBOARD INTEGRADO...")
    print("=" * 50)
    
    try:
        # Executar teste rápido primeiro
        print("⚡ Executando teste rápido...")
        result = subprocess.run([
            sys.executable, "teste_dashboard_integrado.py"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Teste rápido concluído com sucesso!")
        else:
            print("⚠️ Teste rápido com avisos, mas continuando...")
        
        # Executar o dashboard
        print("\n🎯 Iniciando Streamlit Dashboard...")
        print("🌐 O dashboard será aberto em: http://localhost:8502")
        print("⏹️ Para parar, pressione Ctrl+C no terminal")
        print("\n" + "=" * 50)
        
        # Executar streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "dashboard_trading_integrado.py",
            "--server.address", "localhost",
            "--server.port", "8502",
            "--browser.gatherUsageStats", "false"
        ])
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Dashboard interrompido pelo usuário")
        print("✅ Sistema encerrado com segurança")
    except subprocess.TimeoutExpired:
        print("\n⏰ Timeout no teste - mas continuando com o dashboard...")
        # Tentar executar mesmo assim
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "dashboard_trading_integrado.py"
        ])
    except Exception as e:
        print(f"\n❌ Erro ao executar dashboard: {e}")
        return False
    
    return True

def main():
    """Função principal do launcher"""
    print("🎯 SISTEMA DE TRADING INTEGRADO - LAUNCHER")
    print("=" * 50)
    print("🏆 Versão: 1.0 Final")
    print("📅 Data: 24/06/2025")
    print("🔧 Componentes: Sistema Integrado + Dashboard Unificado")
    print("=" * 50)
    
    # Verificar ambiente
    if not verificar_ambiente():
        print("\n❌ FALHA NA VERIFICAÇÃO DO AMBIENTE")
        print("Por favor, instale as dependências necessárias.")
        return False
    
    print("\n✅ AMBIENTE VERIFICADO COM SUCESSO!")
    
    # Executar dashboard
    if executar_dashboard():
        print("\n🎉 SISTEMA EXECUTADO COM SUCESSO!")
        return True
    else:
        print("\n❌ FALHA NA EXECUÇÃO DO SISTEMA")
        return False

if __name__ == "__main__":
    try:
        sucesso = main()
        if sucesso:
            print("\n🏁 LAUNCHER CONCLUÍDO")
        else:
            print("\n⚠️ LAUNCHER FINALIZADO COM PROBLEMAS")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Launcher interrompido pelo usuário")
        print("✅ Encerrado com segurança")
    except Exception as e:
        print(f"\n💥 Erro crítico no launcher: {e}")
        sys.exit(1)
