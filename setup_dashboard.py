#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup e Teste do Dashboard Trading Pro
Script para configuração inicial e verificação do sistema
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

class DashboardSetup:
    """Classe para configuração e teste do dashboard"""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.arquivos_necessarios = [
            'dashboard_trading_pro_real.py',
            'calculo_entradas_v55.py',
            'requirements_dashboard.txt',
            'launcher_dashboard.py'
        ]
        
    def verificar_arquivos(self):
        """Verifica se todos os arquivos necessários existem"""
        print("🔍 Verificando arquivos necessários...")
        
        arquivos_ok = []
        arquivos_faltando = []
        
        for arquivo in self.arquivos_necessarios:
            caminho = self.script_dir / arquivo
            if caminho.exists():
                arquivos_ok.append(arquivo)
                print(f"✅ {arquivo}")
            else:
                arquivos_faltando.append(arquivo)
                print(f"❌ {arquivo}")
        
        if arquivos_faltando:
            print(f"\n⚠️  Arquivos faltando: {', '.join(arquivos_faltando)}")
            return False
        
        print("✅ Todos os arquivos necessários estão presentes!")
        return True
    
    def verificar_python_version(self):
        """Verifica versão do Python"""
        print("🐍 Verificando versão do Python...")
        
        version = sys.version_info
        print(f"Python {version.major}.{version.minor}.{version.micro}")
        
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print("❌ Python 3.8+ é necessário!")
            return False
        
        print("✅ Versão do Python compatível!")
        return True
    
    def instalar_dependencias(self):
        """Instala dependências do requirements"""
        print("📦 Instalando dependências...")
        
        requirements_file = self.script_dir / 'requirements_dashboard.txt'
        
        if not requirements_file.exists():
            print("❌ Arquivo requirements_dashboard.txt não encontrado!")
            return False
        
        try:
            cmd = [sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print("✅ Dependências instaladas com sucesso!")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao instalar dependências: {e}")
            print(f"STDOUT: {e.stdout}")
            print(f"STDERR: {e.stderr}")
            return False
    
    def testar_imports(self):
        """Testa imports principais"""
        print("🧪 Testando imports principais...")
        
        imports_teste = [
            ('streamlit', 'Streamlit'),
            ('plotly', 'Plotly'),
            ('pandas', 'Pandas'),
            ('numpy', 'NumPy'),
            ('MetaTrader5', 'MetaTrader5'),
            ('scipy', 'SciPy'),
            ('statsmodels', 'Statsmodels')
        ]
        
        falhas = []
        
        for modulo, nome in imports_teste:
            try:
                __import__(modulo)
                print(f"✅ {nome}")
            except ImportError as e:
                print(f"❌ {nome}: {e}")
                falhas.append(nome)
        
        if falhas:
            print(f"\n⚠️  Imports falharam: {', '.join(falhas)}")
            return False
        
        print("✅ Todos os imports funcionando!")
        return True
    
    def criar_config_inicial(self):
        """Cria configuração inicial"""
        print("⚙️  Criando configuração inicial...")
        
        config = {
            "dashboard_config": {
                "port": 8501,
                "address": "localhost",
                "auto_refresh": True,
                "refresh_interval": 30
            },
            "trading_config": {
                "default_timeframe": "15 min",
                "default_period": 200,
                "default_zscore": 2.0,
                "max_positions": 6,
                "filters": {
                    "cointegration": True,
                    "r2_filter": True,
                    "beta_filter": True,
                    "zscore_filter": True
                }
            },
            "setup_info": {
                "setup_date": datetime.now().isoformat(),
                "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                "setup_completed": True
            }
        }
        
        config_file = self.script_dir / 'dashboard_config.json'
        
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Configuração criada: {config_file}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar configuração: {e}")
            return False
    
    def testar_dashboard(self):
        """Testa se o dashboard pode ser carregado"""
        print("🧪 Testando carregamento do dashboard...")
        
        try:
            # Testa import do dashboard
            sys.path.insert(0, str(self.script_dir))
            
            # Verifica se o arquivo principal existe e pode ser importado
            dashboard_file = self.script_dir / 'dashboard_trading_pro_real.py'
            
            if not dashboard_file.exists():
                print("❌ Arquivo dashboard_trading_pro_real.py não encontrado!")
                return False
            
            # Testa sintaxe do arquivo
            with open(dashboard_file, 'r', encoding='utf-8') as f:
                codigo = f.read()
            
            try:
                compile(codigo, str(dashboard_file), 'exec')
                print("✅ Sintaxe do dashboard válida!")
            except SyntaxError as e:
                print(f"❌ Erro de sintaxe no dashboard: {e}")
                return False
            
            print("✅ Dashboard pronto para execução!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao testar dashboard: {e}")
            return False
    
    def gerar_relatorio_setup(self):
        """Gera relatório do setup"""
        print("📋 Gerando relatório de setup...")
        
        relatorio = {
            "timestamp": datetime.now().isoformat(),
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "sistema_operacional": os.name,
            "diretorio": str(self.script_dir),
            "arquivos_verificados": self.arquivos_necessarios,
            "setup_status": "completo"
        }
        
        relatorio_file = self.script_dir / f'setup_relatorio_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        try:
            with open(relatorio_file, 'w', encoding='utf-8') as f:
                json.dump(relatorio, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Relatório salvo: {relatorio_file}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao salvar relatório: {e}")
            return False
    
    def executar_setup_completo(self):
        """Executa setup completo"""
        print("🚀 INICIANDO SETUP COMPLETO DO DASHBOARD")
        print("=" * 60)
        
        etapas = [
            ("Verificação de arquivos", self.verificar_arquivos),
            ("Verificação do Python", self.verificar_python_version),
            ("Instalação de dependências", self.instalar_dependencias),
            ("Teste de imports", self.testar_imports),
            ("Criação de configuração", self.criar_config_inicial),
            ("Teste do dashboard", self.testar_dashboard),
            ("Geração de relatório", self.gerar_relatorio_setup)
        ]
        
        etapas_ok = 0
        
        for i, (nome, funcao) in enumerate(etapas, 1):
            print(f"\n[{i}/{len(etapas)}] {nome}...")
            
            if funcao():
                etapas_ok += 1
                print(f"✅ [{i}/{len(etapas)}] {nome} - SUCESSO")
            else:
                print(f"❌ [{i}/{len(etapas)}] {nome} - FALHA")
                break
        
        print("\n" + "=" * 60)
        
        if etapas_ok == len(etapas):
            print("🎉 SETUP CONCLUÍDO COM SUCESSO!")
            print("\n📋 Próximos passos:")
            print("1. Execute: python launcher_dashboard.py")
            print("2. Ou: streamlit run dashboard_trading_pro_real.py")
            print("3. Acesse: http://localhost:8501")
            print("\n✨ Seu dashboard está pronto para uso!")
            return True
        else:
            print(f"❌ SETUP INCOMPLETO - {etapas_ok}/{len(etapas)} etapas concluídas")
            print("\n🔧 Corrija os problemas acima e execute novamente")
            return False

def main():
    """Função principal"""
    print("🏆 SETUP - DASHBOARD TRADING PROFESSIONAL")
    print("Configuração automática do sistema completo")
    print("=" * 50)
    
    setup = DashboardSetup()
    
    # Opção interativa
    print("\n🎯 Opções de setup:")
    print("1. Setup completo automático")
    print("2. Verificação rápida")
    print("3. Apenas instalar dependências")
    print("4. Sair")
    
    try:
        opcao = input("\nEscolha uma opção (1-4): ").strip()
        
        if opcao == "1":
            sucesso = setup.executar_setup_completo()
            
        elif opcao == "2":
            print("\n🔍 VERIFICAÇÃO RÁPIDA")
            arquivos_ok = setup.verificar_arquivos()
            python_ok = setup.verificar_python_version()
            imports_ok = setup.testar_imports()
            
            if arquivos_ok and python_ok and imports_ok:
                print("\n✅ Sistema pronto para uso!")
                sucesso = True
            else:
                print("\n❌ Problemas detectados - execute setup completo")
                sucesso = False
                
        elif opcao == "3":
            print("\n📦 INSTALAÇÃO DE DEPENDÊNCIAS")
            sucesso = setup.instalar_dependencias()
            
        elif opcao == "4":
            print("👋 Saindo...")
            return
            
        else:
            print("❌ Opção inválida!")
            return
        
        if sucesso:
            print(f"\n🎉 Operação concluída com sucesso!")
        else:
            print(f"\n❌ Operação concluída com problemas!")
            
    except KeyboardInterrupt:
        print("\n\n🛑 Setup cancelado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
    
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main()
