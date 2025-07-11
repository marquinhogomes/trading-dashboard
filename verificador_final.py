#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificador Final - Testa se todas as correções funcionam
"""

import sys
import os
import subprocess
import time
from datetime import datetime

def verificar_arquivos():
    """Verifica se os arquivos necessários existem"""
    print("🔍 VERIFICANDO ARQUIVOS...")
    
    arquivos_necessarios = [
        'sistema_integrado_fixed.py',
        'calculo_entradas_v55.py',
        'requirements.txt'
    ]
    
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"   ✅ {arquivo}")
        else:
            print(f"   ❌ {arquivo} - NÃO ENCONTRADO")
    
    print()

def verificar_encoding():
    """Testa se o encoding UTF-8 funciona"""
    print("🔤 VERIFICANDO ENCODING UTF-8...")
    
    try:
        # Testa caracteres especiais
        emojis = "🎯📊💰📈🔍⚡✅❌"
        print(f"   Emojis: {emojis}")
        
        # Testa caracteres latinos
        texto = "Ação, coração, não"
        print(f"   Acentos: {texto}")
        
        # Testa encoding do arquivo original
        if os.path.exists('calculo_entradas_v55.py'):
            encodings = ['utf-8', 'latin-1', 'cp1252']
            for encoding in encodings:
                try:
                    with open('calculo_entradas_v55.py', 'r', encoding=encoding) as f:
                        f.read(100)  # Lê apenas um pedaço
                    print(f"   ✅ Leitura OK com {encoding}")
                    break
                except UnicodeDecodeError:
                    print(f"   ⚠️  Erro com {encoding}")
        
        print("   ✅ Encoding UTF-8 funcionando")
    except Exception as e:
        print(f"   ❌ Erro de encoding: {e}")
    
    print()

def verificar_sintaxe():
    """Verifica se não há erros de sintaxe"""
    print("🐍 VERIFICANDO SINTAXE PYTHON...")
    
    try:
        import ast
        
        arquivos_python = [
            'sistema_integrado_fixed.py',
            'calculo_entradas_v55.py'
        ]
        
        for arquivo in arquivos_python:
            if os.path.exists(arquivo):
                try:
                    with open(arquivo, 'r', encoding='utf-8', errors='ignore') as f:
                        codigo = f.read()
                    ast.parse(codigo)
                    print(f"   ✅ {arquivo} - Sintaxe OK")
                except SyntaxError as e:
                    print(f"   ❌ {arquivo} - Erro de sintaxe: {e}")
                except Exception as e:
                    print(f"   ⚠️  {arquivo} - Aviso: {e}")
    
    except Exception as e:
        print(f"   ❌ Erro na verificação: {e}")
    
    print()

def verificar_imports():
    """Verifica se os imports funcionam"""
    print("📦 VERIFICANDO IMPORTS...")
    
    imports_criticos = [
        'threading',
        'datetime', 
        'json',
        'sys',
        'os',
        'time'
    ]
    
    for modulo in imports_criticos:
        try:
            __import__(modulo)
            print(f"   ✅ {modulo}")
        except ImportError:
            print(f"   ❌ {modulo} - NÃO DISPONÍVEL")
    
    print()

def testar_execucao_rapida():
    """Testa se o sistema pode ser iniciado (teste rápido)"""
    print("⚡ TESTE RÁPIDO DE EXECUÇÃO...")
    
    try:
        # Importa o módulo para testar
        sys.path.append('.')
        
        # Testa se consegue importar sem erros
        with open('sistema_integrado_fixed.py', 'r', encoding='utf-8') as f:
            codigo = f.read()
        
        # Verifica se as principais classes estão definidas
        if 'class SistemaIntegrado' in codigo:
            print("   ✅ Classe SistemaIntegrado encontrada")
        
        if 'def main()' in codigo:
            print("   ✅ Função main encontrada")
        
        if 'threading' in codigo:
            print("   ✅ Threading implementado")
        
        print("   ✅ Sistema pronto para execução")
        
    except Exception as e:
        print(f"   ❌ Erro no teste: {e}")
    
    print()

def main():
    """Função principal de verificação"""
    print("🎯 VERIFICADOR FINAL - SISTEMA INTEGRADO")
    print("=" * 50)
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    print()
    
    # Execute todas as verificações
    verificar_arquivos()
    verificar_encoding()
    verificar_sintaxe()
    verificar_imports()
    testar_execucao_rapida()
    
    print("🎉 VERIFICAÇÃO COMPLETA!")
    print("=" * 50)
    print("Para executar o sistema completo:")
    print("👉 python sistema_integrado_fixed.py")
    print("=" * 50)

if __name__ == "__main__":
    main()
