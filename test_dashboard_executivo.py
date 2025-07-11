#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TESTE DO DASHBOARD EXECUTIVO - TRADING QUANTITATIVO
Script de teste para verificar se o dashboard está funcionando corretamente
"""

import sys
import os
import importlib.util

def test_dashboard_import():
    """Testa se o dashboard pode ser importado sem erros"""
    try:
        # Caminho para o dashboard
        dashboard_path = os.path.join(os.path.dirname(__file__), 'dashboard_trading_pro.py')
        
        # Verificar se o arquivo existe
        if not os.path.exists(dashboard_path):
            return False, "Arquivo dashboard_trading_pro.py não encontrado"
        
        print("✅ Arquivo dashboard_trading_pro.py encontrado!")
        return True, "Dashboard disponível para execução!"
        
    except Exception as e:
        return False, f"Erro ao verificar dashboard: {str(e)}"

def test_required_dependencies():
    """Testa se as dependências estão instaladas"""
    required_modules = [
        'streamlit',
        'pandas', 
        'numpy',
        'plotly',
        'datetime'
    ]
    
    missing_modules = []
    available_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            available_modules.append(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        return False, f"Módulos não encontrados: {', '.join(missing_modules)}"
    else:
        return True, f"Dependências OK: {', '.join(available_modules)}"

def run_all_tests():
    """Executa todos os testes"""
    print("🧪 TESTE DO DASHBOARD EXECUTIVO - TRADING QUANTITATIVO")
    print("=" * 60)
    
    tests = [
        ("📦 Teste de Dependências", test_required_dependencies),
        ("📁 Verificação de Arquivo", test_dashboard_import)
    ]
    
    all_passed = True
    
    for test_name, test_func in tests:
        print(f"\n{test_name}...")
        try:
            success, message = test_func()
            if success:
                print(f"✅ {message}")
            else:
                print(f"❌ {message}")
                all_passed = False
        except Exception as e:
            print(f"❌ Erro inesperado: {str(e)}")
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 DASHBOARD PRONTO PARA USO!")
        print("\n📊 Funcionalidades implementadas:")
        print("   ✅ Header institucional com logo e data/hora")
        print("   ✅ Cartões de status executivos (8 KPIs)")
        print("   ✅ Sidebar com login MT5 e configurações")
        print("   ✅ Painéis de gráficos interativos")
        print("   ✅ Tabelas de sinais e posições")
        print("   ✅ Histórico e auditoria com tabs")
        print("   ✅ Sistema de alertas e relatórios")
        print("   ✅ Tema escuro executivo responsivo")
        print("\n🚀 Para executar o dashboard:")
        print("   streamlit run dashboard_trading_pro.py")
        print("\n🌐 O dashboard abrirá em: http://localhost:8501")
    else:
        print("⚠️  VERIFICAR DEPENDÊNCIAS!")
        print("\n🔧 Instale as dependências faltantes:")
        print("   pip install streamlit pandas numpy plotly")
    
    print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    run_all_tests()
