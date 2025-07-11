#!/usr/bin/env python3
"""
Script de teste para diagnosticar o problema na função executar_analise_real
"""

import pandas as pd
from datetime import datetime
import MetaTrader5 as mt5

def test_mt5_connection():
    """Testa conexão com MT5"""
    if not mt5.initialize():
        print("❌ Falha ao inicializar MT5")
        return False
    
    account_info = mt5.account_info()
    if account_info:
        print(f"✅ MT5 conectado - Conta: {account_info.login}")
        return True
    else:
        print("❌ Falha ao obter informações da conta")
        return False

def test_data_collection():
    """Testa coleta de dados históricos"""
    if not test_mt5_connection():
        return
    
    # Lista de símbolos para teste
    simbolos = ['ABEV3', 'BBAS3', 'PETR4', 'VALE3', 'IBOV']
    timeframe = mt5.TIMEFRAME_D1
    periodo = 250
    
    dados_coletados = {}
    
    print("\n🔍 Testando coleta de dados históricos...")
    
    for simbolo in simbolos:
        try:
            rates = mt5.copy_rates_from_pos(simbolo, timeframe, 0, periodo)
            
            if rates is not None and len(rates) > 0:
                df = pd.DataFrame(rates)
                df['time'] = pd.to_datetime(df['time'], unit='s')
                df.set_index('time', inplace=True)
                dados_coletados[simbolo] = df
                print(f"✅ {simbolo}: {len(df)} registros coletados")
            else:
                print(f"❌ {simbolo}: Sem dados")
                
        except Exception as e:
            print(f"❌ {simbolo}: Erro - {e}")
    
    return dados_coletados

def test_preprocessing(dados_coletados):
    """Testa pré-processamento dos dados"""
    if not dados_coletados:
        print("❌ Sem dados para pré-processar")
        return None
    
    print("\n🔄 Testando pré-processamento...")
    
    try:
        from calculo_entradas_v55 import preprocessar_dados
        
        simbolos = list(dados_coletados.keys())
        colunas = ['close', 'open', 'high', 'low']
        
        dados_preprocessados = preprocessar_dados(dados_coletados, simbolos, colunas, verbose=True)
        
        print(f"✅ Pré-processamento concluído para {len(dados_preprocessados)} símbolos")
        
        # Verifica estrutura dos dados
        for simbolo in dados_preprocessados:
            close_data = dados_preprocessados[simbolo].get('close', {})
            if close_data and 'raw' in close_data:
                raw_data = close_data['raw']
                ndiffs = close_data['ndiffs']
                print(f"📊 {simbolo}: {len(raw_data)} registros, ndiffs={ndiffs}")
            else:
                print(f"⚠️ {simbolo}: Estrutura de dados inválida")
        
        return dados_preprocessados
        
    except Exception as e:
        print(f"❌ Erro no pré-processamento: {e}")
        return None

def test_pair_analysis(dados_preprocessados):
    """Testa análise de um par específico"""
    if not dados_preprocessados:
        print("❌ Sem dados pré-processados para análise")
        return
    
    print("\n🧮 Testando análise de par específico...")
    
    try:
        from calculo_entradas_v55 import calcular_residuo_zscore_timeframe
        
        # Teste com par conhecido
        dep = 'PETR4'
        ind = 'VALE3'
        ibov = 'IBOV'
        win = 'IBOV'
        periodo = 250
        
        # Verifica se todos os símbolos estão disponíveis
        simbolos_necessarios = [dep, ind, ibov, win]
        for simbolo in simbolos_necessarios:
            if simbolo not in dados_preprocessados:
                print(f"❌ {simbolo} não encontrado nos dados pré-processados")
                return
        
        print(f"🔍 Analisando par {dep} x {ind}...")
        
        resultado = calcular_residuo_zscore_timeframe(
            dep=dep,
            ind=ind, 
            ibov=ibov,
            win=win,
            periodo=periodo,
            dados_preprocessados=dados_preprocessados,
            USE_SPREAD_FORECAST=True,
            zscore_threshold=3.0,
            verbose=True,
            enable_zscore_filter=False,
            enable_r2_filter=False,
            enable_beta_filter=False,
            enable_cointegration_filter=False
        )
        
        if resultado is None:
            print("❌ Função retornou None")
        else:
            alpha, beta, half_life, zscore, residuo, adf_p_value, pred_resid, resid_atual, zscore_forecast_compra, zscore_forecast_venda, zf_compra, zf_venda, nd_dep, nd_ind, coint_p_value, r2 = resultado
            
            print(f"✅ Análise concluída:")
            print(f"   - Z-Score: {zscore}")
            print(f"   - Alpha: {alpha}")
            print(f"   - Beta: {beta}")
            print(f"   - R²: {r2}")
            print(f"   - ADF p-value: {adf_p_value}")
            print(f"   - Coint p-value: {coint_p_value}")
            
    except Exception as e:
        print(f"❌ Erro na análise do par: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Executa todos os testes"""
    print("🧪 INICIANDO TESTES DIAGNÓSTICOS")
    print("=" * 50)
    
    # Teste 1: Coleta de dados
    dados_coletados = test_data_collection()
    
    if not dados_coletados:
        print("❌ Falhou na coleta de dados. Verificar conexão MT5.")
        return
    
    # Teste 2: Pré-processamento
    dados_preprocessados = test_preprocessing(dados_coletados)
    
    if not dados_preprocessados:
        print("❌ Falhou no pré-processamento. Verificar função preprocessar_dados.")
        return
    
    # Teste 3: Análise de par
    test_pair_analysis(dados_preprocessados)
    
    print("\n" + "=" * 50)
    print("🏁 TESTES CONCLUÍDOS")

if __name__ == "__main__":
    main()
