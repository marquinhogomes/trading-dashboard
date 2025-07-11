#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para verificar correção do gráfico de equity
Simula a situação onde há operações fechadas no MT5 mas o gráfico não aparece
"""

import MetaTrader5 as mt5
from datetime import datetime, timedelta

def testar_coleta_equity():
    """Testa a coleta de dados de equity do MT5"""
    print("=" * 60)
    print("TESTE: COLETA DE DADOS DE EQUITY DO MT5")
    print("=" * 60)
    
    # Tenta conectar ao MT5
    print("1. Testando conexão com MT5...")
    if not mt5.initialize():
        print("❌ Falha ao inicializar MT5")
        return False
    
    print("✅ MT5 conectado com sucesso")
    
    # Obtém informações da conta atual
    print("\n2. Verificando informações da conta...")
    account_info = mt5.account_info()
    if not account_info:
        print("❌ Não foi possível obter informações da conta")
        return False
    
    print(f"✅ Conta: {account_info.login}")
    print(f"   📊 Equity atual: R$ {account_info.equity:,.2f}")
    print(f"   💰 Balance atual: R$ {account_info.balance:,.2f}")
    print(f"   📈 Profit atual: R$ {account_info.profit:+,.2f}")
    
    # Verifica se há operações fechadas recentes
    print("\n3. Verificando operações fechadas recentes...")
    data_fim = datetime.now()
    data_inicio = data_fim - timedelta(days=7)  # Últimos 7 dias
    
    deals = mt5.history_deals_get(data_inicio, data_fim)
    
    if not deals:
        print("⚠️ Nenhuma operação encontrada nos últimos 7 dias")
        print("💡 Isso pode explicar por que o gráfico não aparece")
    else:
        print(f"✅ {len(deals)} operações encontradas nos últimos 7 dias")
        
        # Mostra algumas operações
        deals_com_profit = [d for d in deals if hasattr(d, 'profit') and d.profit != 0]
        print(f"   📊 {len(deals_com_profit)} operações com lucro/prejuízo")
        
        if deals_com_profit:
            lucro_total = sum([d.profit for d in deals_com_profit])
            print(f"   💰 Lucro/prejuízo total: R$ {lucro_total:+,.2f}")
            
            print("\n   🔍 Últimas 5 operações:")
            for i, deal in enumerate(sorted(deals_com_profit, key=lambda x: x.time, reverse=True)[:5]):
                data_deal = datetime.fromtimestamp(deal.time)
                print(f"      {i+1}. {data_deal.strftime('%d/%m %H:%M')} - {deal.symbol} - R$ {deal.profit:+.2f}")
    
    # Testa criação de dados para o gráfico
    print("\n4. Simulando criação de dados para gráfico...")
    
    equity_historico = []
    
    # Ponto atual
    equity_historico.append({
        'timestamp': datetime.now(),
        'equity': account_info.equity,
        'balance': account_info.balance,
        'profit': account_info.profit
    })
    
    # Se há deals, reconstroi histórico simplificado
    if deals:
        deals_com_profit = [d for d in deals if hasattr(d, 'profit') and d.profit != 0]
        if deals_com_profit:
            lucro_total_deals = sum([d.profit for d in deals_com_profit])
            equity_inicial = account_info.equity - lucro_total_deals
            
            # Ponto inicial
            equity_historico.insert(0, {
                'timestamp': data_inicio,
                'equity': equity_inicial,
                'balance': account_info.balance - lucro_total_deals,
                'profit': 0.0
            })
            
            # Pontos intermediários (simplificado)
            lucro_acumulado = 0
            for deal in sorted(deals_com_profit, key=lambda x: x.time)[-3:]:  # Últimos 3
                lucro_acumulado += deal.profit
                equity_historico.append({
                    'timestamp': datetime.fromtimestamp(deal.time),
                    'equity': equity_inicial + lucro_acumulado,
                    'balance': account_info.balance - lucro_total_deals + lucro_acumulado,
                    'profit': lucro_acumulado
                })
    
    print(f"✅ Criados {len(equity_historico)} pontos para o gráfico")
    print("   📊 Pontos do gráfico:")
    for i, ponto in enumerate(equity_historico):
        print(f"      {i+1}. {ponto['timestamp'].strftime('%d/%m %H:%M')} - Equity: R$ {ponto['equity']:,.2f}")
    
    # Conclusões
    print("\n" + "=" * 60)
    print("CONCLUSÕES DO TESTE")
    print("=" * 60)
    
    if len(equity_historico) >= 2:
        print("✅ SUCESSO: Dados suficientes para criar o gráfico")
        print("💡 O gráfico deveria aparecer com estes dados")
        
        # Mostra variação
        equity_inicial = equity_historico[0]['equity']
        equity_final = equity_historico[-1]['equity']
        variacao = equity_final - equity_inicial
        variacao_pct = (variacao / equity_inicial * 100) if equity_inicial > 0 else 0
        
        print(f"📈 Variação de equity: R$ {variacao:+,.2f} ({variacao_pct:+.2f}%)")
        
    else:
        print("⚠️ PROBLEMA: Poucos dados para criar gráfico significativo")
        print("💡 Possíveis soluções:")
        print("   1. Aguardar mais operações")
        print("   2. Mostrar apenas valor atual")
        print("   3. Criar pontos sintéticos baseados no histórico")
    
    # Teste de detecção do problema
    print(f"\n🔍 DIAGNÓSTICO DO PROBLEMA REPORTADO:")
    print(f"   • MT5 conectado: ✅")
    print(f"   • Equity atual disponível: ✅ R$ {account_info.equity:,.2f}")
    print(f"   • Operações nos últimos 7 dias: {'✅' if deals else '❌'} {len(deals) if deals else 0}")
    print(f"   • Operações com P&L: {'✅' if deals_com_profit else '❌'} {len(deals_com_profit) if 'deals_com_profit' in locals() else 0}")
    print(f"   • Pontos para gráfico: {'✅' if len(equity_historico) >= 2 else '⚠️'} {len(equity_historico)}")
    
    if len(equity_historico) >= 2:
        print("\n✅ RESULTADO: Com as correções, o gráfico DEVERIA aparecer")
    else:
        print("\n⚠️ RESULTADO: Pode ser necessário aguardar mais dados ou usar valores atuais")
    
    mt5.shutdown()
    return True

if __name__ == "__main__":
    testar_coleta_equity()
