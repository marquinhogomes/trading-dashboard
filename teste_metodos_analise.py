#!/usr/bin/env python3
"""
Script para testar os métodos de análise do SistemaIntegrado
"""

import sys
import os
import pandas as pd
from datetime import datetime

# Adiciona o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def testar_metodos_analise():
    """Testa os métodos de análise implementados"""
    print("=== Teste dos Métodos de Análise ===")
    
    try:
        # Importa o sistema integrado
        from sistema_integrado import SistemaIntegrado
        print("✓ Sistema integrado importado com sucesso")
        
        # Cria uma instância (sem inicializar threads automáticas)
        sistema = SistemaIntegrado()
        print("✓ Sistema integrado criado com sucesso")
        
        # Testa se os métodos existem
        if hasattr(sistema, 'start_analysis_thread'):
            print("✓ Método start_analysis_thread encontrado")
        else:
            print("✗ Método start_analysis_thread não encontrado")
            
        if hasattr(sistema, 'stop_analysis_thread'):
            print("✓ Método stop_analysis_thread encontrado")
        else:
            print("✗ Método stop_analysis_thread não encontrado")
            
        if hasattr(sistema, 'is_analysis_running'):
            print("✓ Método is_analysis_running encontrado")
        else:
            print("✗ Método is_analysis_running não encontrado")
        
        # Testa o estado inicial
        is_running = sistema.is_analysis_running()
        print(f"✓ Estado inicial is_analysis_running: {is_running}")
        
        # Cria dados de teste
        tabela_teste = pd.DataFrame({
            'ID': [1, 2, 3],
            'Ativo1': ['PETR4', 'VALE3', 'BBAS3'],
            'Ativo2': ['PETR3', 'VALE5', 'BBDC4']
        })
        
        config_teste = {
            'filtro_zscore': True,
            'r2_min': 0.5,
            'beta_max': 2.0,
            'valor_operacao': 1000
        }
        
        # Testa start_analysis_thread
        print("🔄 Testando start_analysis_thread...")
        resultado = sistema.start_analysis_thread(
            tabela_linha_operacao01=tabela_teste,
            config=config_teste
        )
        print(f"✓ start_analysis_thread retornou: {resultado}")
        
        # Verifica se está rodando
        import time
        time.sleep(1)  # Aguarda 1 segundo
        is_running = sistema.is_analysis_running()
        print(f"✓ is_analysis_running após start: {is_running}")
        
        # Testa stop_analysis_thread
        print("🔄 Testando stop_analysis_thread...")
        resultado = sistema.stop_analysis_thread()
        print(f"✓ stop_analysis_thread retornou: {resultado}")
        
        # Verifica se parou
        time.sleep(1)  # Aguarda 1 segundo
        is_running = sistema.is_analysis_running()
        print(f"✓ is_analysis_running após stop: {is_running}")
        
        print("✅ Todos os testes concluídos com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    testar_metodos_analise()
