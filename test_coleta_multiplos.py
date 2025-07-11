#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste: Verificar coleta de dados históricos para múltiplos ativos
"""

import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime

def testar_coleta_multiplos_ativos():
    """Testa a coleta de dados para múltiplos ativos"""
    
    # Inicializa MT5
    if not mt5.initialize():
        print("❌ Falha ao inicializar MT5")
        return
    
    print("✅ MT5 inicializado com sucesso")
    
    # Lista de ativos para testar (baseado no que sabemos que funciona)
    ativos_teste = ['ABEV3', 'BBAS3', 'BBDC4', 'VALE3', 'PETR4', 'ITUB4', 'IBOV']
    periodo = 250
    timeframe = mt5.TIMEFRAME_D1
    
    print(f"\n🔍 Testando coleta de dados para {len(ativos_teste)} ativos...")
    print(f"📊 Período: {periodo} registros, Timeframe: Diário")
    print("=" * 60)
    
    dados_coletados = {}
    
    for simbolo in ativos_teste:
        print(f"🔧 Processando: {simbolo}")
        
        try:
            # Verifica se o símbolo existe
            symbol_info = mt5.symbol_info(simbolo)
            if symbol_info is None:
                print(f"❌ {simbolo}: Não encontrado no MT5")
                continue
            
            print(f"✅ {simbolo}: {symbol_info.description}")
            
            # Obtém dados históricos
            rates = mt5.copy_rates_from_pos(simbolo, timeframe, 0, periodo)
            
            if rates is not None and len(rates) > 0:
                df = pd.DataFrame(rates)
                df['time'] = pd.to_datetime(df['time'], unit='s')
                df.set_index('time', inplace=True)
                
                # Armazena dados
                dados_coletados[simbolo] = df
                print(f"✅ {simbolo}: {len(df)} registros coletados")
                
                # Mostra algumas estatísticas
                close_prices = df['close']
                print(f"   📈 Preço atual: R$ {close_prices.iloc[-1]:.2f}")
                print(f"   📊 Média período: R$ {close_prices.mean():.2f}")
                print(f"   📅 Data início: {df.index[0].strftime('%Y-%m-%d')}")
                print(f"   📅 Data fim: {df.index[-1].strftime('%Y-%m-%d')}")
                
            else:
                print(f"❌ {simbolo}: Nenhum dado histórico retornado")
                erro_mt5 = mt5.last_error()
                print(f"   ❌ Erro MT5: {erro_mt5}")
                
        except Exception as e:
            print(f"❌ {simbolo}: Erro - {str(e)}")
        
        print("-" * 40)
    
    print(f"\n📊 RESUMO DA COLETA:")
    print(f"✅ Ativos processados com sucesso: {len(dados_coletados)}")
    print(f"❌ Ativos com falha: {len(ativos_teste) - len(dados_coletados)}")
    
    if dados_coletados:
        print(f"\n✅ ATIVOS COM DADOS COLETADOS:")
        for simbolo, df in dados_coletados.items():
            print(f"   - {simbolo}: {len(df)} registros")
    
    # Simula o preprocessamento
    if dados_coletados:
        print(f"\n🔧 Simulando estrutura pós-preprocessamento...")
        
        # Simula como os dados ficariam após preprocessamento
        dados_preprocessados_mock = {}
        
        for simbolo, df in dados_coletados.items():
            dados_preprocessados_mock[simbolo] = {
                'close': {
                    'raw': df['close'].values,
                    'processed': df['close'].values  # Simplificado
                },
                'open': {
                    'raw': df['open'].values,
                    'processed': df['open'].values
                },
                'high': {
                    'raw': df['high'].values,
                    'processed': df['high'].values
                },
                'low': {
                    'raw': df['low'].values,
                    'processed': df['low'].values
                }
            }
        
        print(f"✅ Dados preprocessados simulados para: {list(dados_preprocessados_mock.keys())}")
        
        # Verifica se temos dados suficientes para análise
        for simbolo in dados_preprocessados_mock:
            close_data = dados_preprocessados_mock[simbolo]['close']
            if close_data and 'raw' in close_data:
                tamanho = len(close_data['raw']) if close_data['raw'] is not None else 0
                print(f"📊 {simbolo}: {tamanho} registros de close disponíveis")
    
    # Finaliza MT5
    mt5.shutdown()
    print(f"\n🔌 MT5 desconectado")

if __name__ == "__main__":
    testar_coleta_multiplos_ativos()
