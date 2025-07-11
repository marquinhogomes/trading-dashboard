#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verifica e corrige problemas na classe TradingSystemReal
"""

import os
import sys

def verificar_arquivo():
    """Verifica se o arquivo dashboard_trading_pro_real.py está correto"""
    
    caminho = "dashboard_trading_pro_real.py"
    
    if not os.path.exists(caminho):
        print("❌ Arquivo dashboard_trading_pro_real.py não encontrado!")
        return False
    
    with open(caminho, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Verifica se a classe existe
    if 'class TradingSystemReal:' not in conteudo:
        print("❌ Classe TradingSystemReal não encontrada!")
        return False
    
    # Verifica se os métodos existem
    metodos_necessarios = ['def iniciar_sistema', 'def parar_sistema', 'def conectar_mt5']
    metodos_encontrados = []
    metodos_faltando = []
    
    for metodo in metodos_necessarios:
        if metodo in conteudo:
            metodos_encontrados.append(metodo)
            print(f"✅ {metodo}: encontrado")
        else:
            metodos_faltando.append(metodo)
            print(f"❌ {metodo}: NÃO encontrado")
    
    # Verifica estrutura da sessão
    if "st.session_state.trading_system = TradingSystemReal()" in conteudo:
        print("✅ Inicialização da sessão: OK")
    else:
        print("❌ Problema na inicialização da sessão")
    
    # Verifica se há problemas de indentação
    linhas = conteudo.split('\n')
    problemas_indentacao = []
    
    for i, linha in enumerate(linhas, 1):
        if linha.strip().startswith('def ') and not linha.startswith('    def ') and not linha.startswith('def '):
            if 'TradingSystemReal' in linhas[max(0, i-10):i]:  # Se está dentro da classe
                problemas_indentacao.append(f"Linha {i}: {linha.strip()}")
    
    if problemas_indentacao:
        print("❌ Problemas de indentação encontrados:")
        for problema in problemas_indentacao[:5]:  # Mostra apenas os primeiros 5
            print(f"   {problema}")
    else:
        print("✅ Indentação: OK")
    
    return len(metodos_faltando) == 0 and len(problemas_indentacao) == 0

def testar_importacao():
    """Testa se a importação funciona"""
    try:
        from dashboard_trading_pro_real import TradingSystemReal
        sistema = TradingSystemReal()
        
        print("✅ Importação: OK")
        
        # Testa métodos específicos
        if hasattr(sistema, 'iniciar_sistema'):
            print("✅ Método iniciar_sistema: OK")
        else:
            print("❌ Método iniciar_sistema: NÃO ENCONTRADO")
            return False
            
        if hasattr(sistema, 'parar_sistema'):
            print("✅ Método parar_sistema: OK")
        else:
            print("❌ Método parar_sistema: NÃO ENCONTRADO")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na importação: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔍 Verificando arquivo dashboard_trading_pro_real.py...")
    print("=" * 50)
    
    arquivo_ok = verificar_arquivo()
    print("\n" + "=" * 50)
    
    if arquivo_ok:
        print("🧪 Testando importação...")
        importacao_ok = testar_importacao()
        print("=" * 50)
        
        if importacao_ok:
            print("✅ TODOS OS TESTES PASSARAM!")
            print("🚀 O dashboard deve funcionar corretamente.")
        else:
            print("❌ FALHA NOS TESTES DE IMPORTAÇÃO!")
    else:
        print("❌ FALHA NA VERIFICAÇÃO DO ARQUIVO!")
    
    print("\n💡 Para executar o dashboard:")
    print("   streamlit run dashboard_trading_pro_real.py")
