#!/usr/bin/env python3
"""
Teste de Diagnóstico: Coleta de Dados de Equity do MT5
====================================================

Este script testa se o dashboard consegue coletar e exibir dados de equity
do MT5 corretamente, incluindo a nova função obter_equity_historico_mt5.
"""

import sys
import os
import json
from datetime import datetime, timedelta

# Adiciona o diretório atual ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def simular_mt5():
    """Simula dados do MT5 para teste"""
    class MockAccountInfo:
        def __init__(self):
            self.equity = 25750.50
            self.balance = 25000.00
            self.profit = 750.50
    
    class MockDeal:
        def __init__(self, time_offset_hours, profit):
            base_time = datetime.now() - timedelta(days=2)
            self.time = int((base_time + timedelta(hours=time_offset_hours)).timestamp())
            self.profit = profit
    
    # Simula deals dos últimos dias
    mock_deals = [
        MockDeal(0, 150.00),
        MockDeal(4, -75.50),
        MockDeal(8, 200.25),
        MockDeal(12, 100.00),
        MockDeal(16, -50.00),
        MockDeal(20, 300.00),
        MockDeal(24, 125.75)
    ]
    
    return MockAccountInfo(), mock_deals

def testar_obter_equity_historico():
    """Testa a função obter_equity_historico_mt5"""
    print("🧪 TESTE: Função obter_equity_historico_mt5")
    print("=" * 50)
    
    try:
        # Importa a função do dashboard
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "dashboard", 
            "dashboard_trading_pro_real.py"
        )
        dashboard = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(dashboard)
        
        # Cria um sistema mock para teste
        class SistemaMock:
            def __init__(self):
                self.mt5_connected = True
                self.equity_historico = []
            
            def log(self, msg):
                print(f"[LOG] {msg}")
        
        sistema_mock = SistemaMock()
        
        # Substitui mt5 por versão mock
        import MetaTrader5 as mt5
        
        account_info_mock, deals_mock = simular_mt5()
        
        original_account_info = mt5.account_info
        original_history_deals_get = mt5.history_deals_get
        
        mt5.account_info = lambda: account_info_mock
        mt5.history_deals_get = lambda start, end: deals_mock
        
        try:
            # Testa a função
            resultado = dashboard.obter_equity_historico_mt5(sistema_mock)
            
            print(f"✅ Função executada com sucesso!")
            print(f"📊 Pontos de equity obtidos: {len(resultado)}")
            
            if resultado:
                print("\n📈 Histórico de Equity:")
                for i, ponto in enumerate(resultado):
                    timestamp = ponto['timestamp']
                    equity = ponto['equity']
                    balance = ponto['balance']
                    profit = ponto['profit']
                    
                    print(f"  {i+1}. {timestamp.strftime('%H:%M:%S')} - "
                          f"Equity: R$ {equity:,.2f} | "
                          f"Balance: R$ {balance:,.2f} | "
                          f"Profit: R$ {profit:+,.2f}")
                
                # Análise da curva
                equity_inicial = resultado[0]['equity']
                equity_final = resultado[-1]['equity']
                variacao = equity_final - equity_inicial
                
                print(f"\n📊 Análise da Curva:")
                print(f"  • Equity Inicial: R$ {equity_inicial:,.2f}")
                print(f"  • Equity Final: R$ {equity_final:,.2f}")
                print(f"  • Variação Total: R$ {variacao:+,.2f}")
                print(f"  • Variação %: {(variacao/equity_inicial)*100:+.2f}%")
                
                return True
            else:
                print("❌ Nenhum ponto de equity foi obtido")
                return False
                
        finally:
            # Restaura funções originais
            mt5.account_info = original_account_info
            mt5.history_deals_get = original_history_deals_get
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def testar_conexao_mt5_real():
    """Testa conexão real com MT5 se disponível"""
    print("\n🔌 TESTE: Conexão Real com MT5")
    print("=" * 50)
    
    try:
        import MetaTrader5 as mt5
        
        # Tenta conectar
        if not mt5.initialize():
            print("❌ MT5 não está disponível")
            return False
        
        print("✅ MT5 conectado com sucesso!")
        
        # Obtém informações da conta
        account_info = mt5.account_info()
        if account_info:
            print(f"📊 Dados da Conta:")
            print(f"  • Equity: R$ {account_info.equity:,.2f}")
            print(f"  • Balance: R$ {account_info.balance:,.2f}")
            print(f"  • Profit: R$ {account_info.profit:+,.2f}")
        
        # Testa histórico de deals
        data_fim = datetime.now()
        data_inicio = data_fim - timedelta(days=7)
        
        deals = mt5.history_deals_get(data_inicio, data_fim)
        if deals:
            print(f"📈 Deals encontrados: {len(deals)} nos últimos 7 dias")
            
            if len(deals) > 0:
                lucro_total = sum([deal.profit for deal in deals if hasattr(deal, 'profit')])
                print(f"💰 Lucro total dos deals: R$ {lucro_total:+,.2f}")
        else:
            print("📊 Nenhum deal encontrado nos últimos 7 dias")
        
        mt5.shutdown()
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão com MT5: {str(e)}")
        return False

def testar_funcionalidade_dashboard():
    """Testa se a funcionalidade do dashboard está correta"""
    print("\n🎛️  TESTE: Funcionalidade do Dashboard")
    print("=" * 50)
    
    try:
        # Verifica se o arquivo do dashboard existe
        dashboard_path = "dashboard_trading_pro_real.py"
        if not os.path.exists(dashboard_path):
            print(f"❌ Arquivo {dashboard_path} não encontrado")
            return False
        
        print(f"✅ Arquivo {dashboard_path} encontrado")
        
        # Verifica se as funções necessárias existem
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        funcoes_necessarias = [
            'render_equity_chart',
            'obter_equity_historico_mt5'
        ]
        
        for funcao in funcoes_necessarias:
            if f"def {funcao}" in conteudo:
                print(f"✅ Função {funcao} encontrada")
            else:
                print(f"❌ Função {funcao} NÃO encontrada")
                return False
        
        # Verifica se a correção do equity está implementada
        if "# CORREÇÃO: Se não há dados no histórico mas MT5 está conectado" in conteudo:
            print("✅ Correção de coleta automática implementada")
        else:
            print("⚠️  Correção de coleta automática pode não estar implementada")
        
        if "🔄 Atualizar" in conteudo:
            print("✅ Botão de atualização manual implementado")
        else:
            print("⚠️  Botão de atualização manual pode não estar implementado")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar dashboard: {str(e)}")
        return False

def main():
    """Função principal do teste"""
    print("🧪 DIAGNÓSTICO DE EQUITY DO DASHBOARD")
    print("=" * 60)
    print(f"⏰ Executado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    resultados = {
        'teste_funcionalidade_dashboard': False,
        'teste_funcao_equity': False,
        'teste_conexao_mt5': False,
        'timestamp': datetime.now().isoformat()
    }
    
    # Teste 1: Funcionalidade do Dashboard
    resultados['teste_funcionalidade_dashboard'] = testar_funcionalidade_dashboard()
    
    # Teste 2: Função de Equity
    resultados['teste_funcao_equity'] = testar_obter_equity_historico()
    
    # Teste 3: Conexão real com MT5 (opcional)
    resultados['teste_conexao_mt5'] = testar_conexao_mt5_real()
    
    # Resumo
    print("\n📋 RESUMO DOS TESTES")
    print("=" * 50)
    
    total_testes = len([k for k in resultados.keys() if k != 'timestamp'])
    testes_aprovados = sum([1 for k, v in resultados.items() if k != 'timestamp' and v])
    
    for teste, resultado in resultados.items():
        if teste != 'timestamp':
            status = "✅ APROVADO" if resultado else "❌ FALHOU"
            print(f"  • {teste.replace('_', ' ').title()}: {status}")
    
    print(f"\n🎯 RESULTADO GERAL: {testes_aprovados}/{total_testes} testes aprovados")
    
    if testes_aprovados == total_testes:
        print("🎉 TODOS OS TESTES PASSARAM! O gráfico de equity deve funcionar.")
    elif testes_aprovados >= 2:
        print("⚠️  A maioria dos testes passou. Verifique os pontos que falharam.")
    else:
        print("❌ FALHAS CRÍTICAS detectadas. Correções necessárias.")
    
    # Salva relatório
    relatorio_path = f"relatorio_teste_equity_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    try:
        with open(relatorio_path, 'w', encoding='utf-8') as f:
            json.dump(resultados, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Relatório salvo em: {relatorio_path}")
    except Exception as e:
        print(f"❌ Erro ao salvar relatório: {str(e)}")

if __name__ == "__main__":
    main()
