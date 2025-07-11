#!/usr/bin/env python3
"""
Teste Prático: Execução do Dashboard com Foco no Gráfico de Equity
=================================================================
"""

import subprocess
import sys
import os
import time
from datetime import datetime

def main():
    print("🚀 TESTE PRÁTICO: Dashboard com Gráfico de Equity")
    print("=" * 60)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Verifica se streamlit está instalado
    try:
        import streamlit
        print("✅ Streamlit disponível")
    except ImportError:
        print("❌ Streamlit não instalado")
        print("💡 Execute: pip install streamlit")
        return
    
    # Verifica se o dashboard existe
    dashboard_path = "dashboard_trading_pro_real.py"
    if not os.path.exists(dashboard_path):
        print(f"❌ {dashboard_path} não encontrado")
        return
    
    print(f"✅ {dashboard_path} encontrado")
    
    # Instruções para o usuário
    print("\n📋 INSTRUÇÕES PARA O TESTE:")
    print("1. O dashboard será executado em background")
    print("2. Acesse http://localhost:8501 no navegador")
    print("3. Navegue até a aba 'Gráficos'")
    print("4. Verifique se o gráfico de equity aparece")
    print("5. Teste o botão '🔄 Atualizar' se necessário")
    print("6. Pressione Ctrl+C no terminal para parar")
    
    print("\n🎯 O QUE TESTAR:")
    print("✓ Gráfico aparece automaticamente (se MT5 conectado)")
    print("✓ Métricas atuais são exibidas (se não há histórico)")
    print("✓ Botão 'Atualizar' funciona")
    print("✓ Status 'online/offline' correto")
    print("✓ Mensagens de orientação aparecem")
    
    input("\n⏸️  Pressione ENTER para executar o dashboard...")
    
    try:
        print(f"\n🚀 Executando: streamlit run {dashboard_path}")
        print("🌐 URL: http://localhost:8501")
        print("🛑 Para parar: Ctrl+C")
        print("-" * 60)
        
        # Executa o dashboard
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            dashboard_path, "--server.port", "8501"
        ])
        
    except KeyboardInterrupt:
        print("\n🛑 Dashboard interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro ao executar dashboard: {str(e)}")

if __name__ == "__main__":
    main()
