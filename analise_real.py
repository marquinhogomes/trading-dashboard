#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de Análise Real - Análise de Cointegração e Seleção de Pares
Contém as funções principais extraídas do calculo_entradas_v55.py para análise de pares
"""

import pandas as pd
import numpy as np
import warnings
from datetime import datetime, timedelta
import MetaTrader5 as mt5
from typing import Dict, List, Optional, Tuple, Any
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, coint
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Suprimir warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# Importar configurações reais
try:
    from config_real import (
        DEPENDENTE_REAL, INDEPENDENTE_REAL, SEGMENTOS_REAIS, FILTER_PARAMS_REAL,
        get_timeframe_mt5, get_pandas_freq, pares_mesmo_segmento, extrair_valor,
        PERIODO_REAL, TIMEZONE_BRASIL
    )
    HAS_REAL_CONFIG = True
except ImportError as e:
    logger.error(f"Erro ao importar configurações reais: {e}")
    HAS_REAL_CONFIG = False

# ═══════════════════════════════════════════════════════════════════════════════
# 📊 FUNÇÕES DE ANÁLISE ESTATÍSTICA (EXTRAÍDAS DO ORIGINAL)
# ═══════════════════════════════════════════════════════════════════════════════

def calcular_residuo_zscore_timeframe(dados_preprocessados, linha_operacao=None, 
                                    enable_cointegration_filter=True, filter_params=None):
    """
    Calcula resíduo e z-score para pares de ativos com filtros estatísticos.
    Função principal extraída do calculo_entradas_v55.py
    
    Args:
        dados_preprocessados: DataFrame com dados dos ativos
        linha_operacao: Lista atual de operações
        enable_cointegration_filter: Aplicar filtro de cointegração
        filter_params: Parâmetros para filtros estatísticos
    
    Returns:
        DataFrame com análises de pares e z-scores
    """
    if filter_params is None:
        filter_params = FILTER_PARAMS_REAL.copy()
    
    logger.info("Iniciando análise de resíduo e z-score")
    
    # Verificar se temos dados suficientes
    if dados_preprocessados.empty:
        logger.warning("Dados preprocessados vazios")
        return pd.DataFrame()
    
    resultados = []
    total_pares = 0
    pares_aprovados = 0
    
    # Análise de pares dependente vs independente
    for dependente in DEPENDENTE_REAL:
        if dependente not in dados_preprocessados.columns:
            continue
            
        for independente in INDEPENDENTE_REAL:
            if independente not in dados_preprocessados.columns or dependente == independente:
                continue
            
            total_pares += 1
            
            try:
                # Extrair séries
                y = dados_preprocessados[dependente].dropna()
                x = dados_preprocessados[independente].dropna()
                
                # Alinhar séries
                data_comum = y.index.intersection(x.index)
                if len(data_comum) < 50:  # Mínimo de dados necessários
                    continue
                
                y_aligned = y.loc[data_comum]
                x_aligned = x.loc[data_comum]
                
                # Calcular regressão linear
                X_with_const = sm.add_constant(x_aligned)
                modelo = sm.OLS(y_aligned, X_with_const).fit()
                
                # Extrair parâmetros
                beta = extrair_valor(modelo.params.iloc[1])
                alpha = extrair_valor(modelo.params.iloc[0])
                r2 = extrair_valor(modelo.rsquared)
                  # Calcular resíduo
                residuo = y_aligned - (alpha + beta * x_aligned)
                
                # Garantir que residuo seja pandas Series
                if not isinstance(residuo, pd.Series):
                    if hasattr(residuo, '__len__') and len(residuo) > 0:
                        # Converter numpy array para pandas Series
                        residuo = pd.Series(residuo, index=y_aligned.index if hasattr(y_aligned, 'index') else range(len(residuo)))
                    else:
                        # Se for valor único, criar Series com um elemento
                        residuo = pd.Series([residuo], index=[0])
                
                # Calcular z-score
                if len(residuo) > 0:
                    zscore_atual = (residuo.iloc[-1] - residuo.mean()) / residuo.std()
                else:
                    zscore_atual = 0.0
                
                # Calcular coeficiente de variação
                coef_var = (residuo.std() / abs(residuo.mean())) * 100 if residuo.mean() != 0 else float('inf')
                
                # Aplicar filtros
                filtros_passaram = {}
                filtros_passaram['r2'] = r2 > filter_params.get('r2_min', 0.5)
                filtros_passaram['beta'] = abs(beta) < filter_params.get('beta_max', 1.5)
                filtros_passaram['coef_var'] = coef_var < filter_params.get('coef_var_max', 5000.0)
                
                # Teste de estacionariedade (ADF)
                adf_stat, adf_pvalue = None, None
                filtros_passaram['adf'] = True  # Default
                
                if len(residuo) > 10:
                    try:
                        adf_result = adfuller(residuo.dropna())
                        adf_stat = adf_result[0]
                        adf_pvalue = adf_result[1]
                        filtros_passaram['adf'] = adf_pvalue < filter_params.get('adf_p_value_max', 0.05)
                    except Exception as e:
                        logger.warning(f"Erro no teste ADF para {dependente}-{independente}: {e}")
                
                # Teste de cointegração (se habilitado)
                coint_stat, coint_pvalue = None, None
                filtros_passaram['coint'] = True  # Default
                
                if enable_cointegration_filter and filter_params.get('use_coint_test', True):
                    try:
                        coint_result = coint(y_aligned, x_aligned)
                        coint_stat = coint_result[0]
                        coint_pvalue = coint_result[1]
                        # Cointegração confirmada se p-valor < 0.05
                        filtros_passaram['coint'] = coint_pvalue < 0.05
                    except Exception as e:
                        logger.warning(f"Erro no teste de cointegração para {dependente}-{independente}: {e}")
                
                # Verificar se todos os filtros passaram
                todos_filtros_passaram = all(filtros_passaram.values())
                
                if todos_filtros_passaram:
                    pares_aprovados += 1
                
                # Adicionar resultado
                resultado = {
                    'Dependente': dependente,
                    'Independente': independente,
                    'Setor_Dep': SEGMENTOS_REAIS.get(dependente, 'N/A'),
                    'Setor_Ind': SEGMENTOS_REAIS.get(independente, 'N/A'),
                    'Alpha': alpha,
                    'Beta': beta,
                    'R2': r2,
                    'Zscore': zscore_atual,
                    'Coef_Var': coef_var,
                    'ADF_Stat': adf_stat,
                    'ADF_PValue': adf_pvalue,
                    'Coint_Stat': coint_stat,
                    'Coint_PValue': coint_pvalue,
                    'Filtros_OK': todos_filtros_passaram,
                    'Mesmo_Setor': SEGMENTOS_REAIS.get(dependente) == SEGMENTOS_REAIS.get(independente),
                    'Residuo_Mean': residuo.mean(),
                    'Residuo_Std': residuo.std(),
                    'Timestamp': datetime.now()
                }
                
                resultados.append(resultado)
                
            except Exception as e:
                logger.error(f"Erro na análise do par {dependente}-{independente}: {e}")
                continue
    
    # Criar DataFrame dos resultados
    df_resultados = pd.DataFrame(resultados)
    
    logger.info(f"Análise concluída: {total_pares} pares analisados, {pares_aprovados} aprovados nos filtros")
    
    return df_resultados

def encontrar_linha_monitorada(tabela_zscore_mesmo_segmento, linha_operacao=None, 
                              dados_preprocessados=None, filter_params=None, 
                              enable_cointegration_filter=True):
    """
    Encontra linha de operação baseada em critérios de z-score e filtros.
    Função extraída do calculo_entradas_v55.py
    
    Args:
        tabela_zscore_mesmo_segmento: DataFrame com análises de mesmo setor
        linha_operacao: Operações atuais
        dados_preprocessados: Dados do mercado
        filter_params: Parâmetros de filtro
        enable_cointegration_filter: Usar filtro de cointegração
    
    Returns:
        Lista de operações selecionadas
    """
    if filter_params is None:
        filter_params = FILTER_PARAMS_REAL.copy()
    
    if tabela_zscore_mesmo_segmento.empty:
        return linha_operacao or []
    
    logger.info("Procurando oportunidades de trading")
    
    # Filtrar apenas pares que passaram em todos os filtros
    candidatos = tabela_zscore_mesmo_segmento[
        tabela_zscore_mesmo_segmento['Filtros_OK'] == True
    ].copy()
    
    if candidatos.empty:
        logger.info("Nenhum candidato passou nos filtros")
        return linha_operacao or []
    
    # Ordenar por critérios de interesse (z-score absoluto, R², etc.)
    candidatos['Zscore_Abs'] = abs(candidatos['Zscore'])
    candidatos = candidatos.sort_values(['Zscore_Abs', 'R2'], ascending=[False, False])
    
    # Selecionar melhores oportunidades
    operacoes_selecionadas = []
    
    for _, row in candidatos.head(10).iterrows():  # Top 10 candidatos
        zscore = row['Zscore']
        
        # Critérios para entrada
        # Z-score > 2: Venda (spread está caro)
        # Z-score < -2: Compra (spread está barato)
        
        if abs(zscore) > 2.0:  # Threshold para entrada
            tipo_operacao = 'VENDA' if zscore > 0 else 'COMPRA'
            
            operacao = {
                'Dependente': row['Dependente'],
                'Independente': row['Independente'],
                'Tipo': tipo_operacao,
                'Zscore': zscore,
                'R2': row['R2'],
                'Beta': row['Beta'],
                'Timestamp': datetime.now(),
                'Status': 'SELECIONADA'
            }
            
            operacoes_selecionadas.append(operacao)
    
    logger.info(f"Selecionadas {len(operacoes_selecionadas)} operações")
    
    return operacoes_selecionadas

def aplicar_filtros_completos(df_analise, filter_params=None):
    """
    Aplica todos os filtros de qualidade na análise de pares.
    
    Args:
        df_analise: DataFrame com análise de pares
        filter_params: Parâmetros de filtro
    
    Returns:
        DataFrame filtrado
    """
    if filter_params is None:
        filter_params = FILTER_PARAMS_REAL.copy()
    
    df_filtrado = df_analise.copy()
    
    # Aplicar filtros
    filtros = {
        'R2': df_filtrado['R2'] > filter_params.get('r2_min', 0.5),
        'Beta': abs(df_filtrado['Beta']) < filter_params.get('beta_max', 1.5),
        'CoefVar': df_filtrado['Coef_Var'] < filter_params.get('coef_var_max', 5000.0),
        'ADF': df_filtrado['ADF_PValue'] < filter_params.get('adf_p_value_max', 0.05),
    }
    
    # Aplicar filtro de cointegração se habilitado
    if filter_params.get('enable_cointegration_filter', True):
        filtros['Coint'] = df_filtrado['Coint_PValue'] < 0.05
    
    # Combinar todos os filtros
    mask_final = pd.Series(True, index=df_filtrado.index)
    for nome_filtro, mask in filtros.items():
        mask_final = mask_final & mask.fillna(False)
    
    df_resultado = df_filtrado[mask_final].copy()
    
    logger.info(f"Filtros aplicados: {len(df_analise)} -> {len(df_resultado)} pares")
    
    return df_resultado

# ═══════════════════════════════════════════════════════════════════════════════
# 📈 FUNÇÕES DE DADOS DO MERCADO
# ═══════════════════════════════════════════════════════════════════════════════

def obter_dados_mt5(simbolos, timeframe='M15', periodo=100):
    """
    Obtém dados do MetaTrader5 para lista de símbolos.
    
    Args:
        simbolos: Lista de símbolos
        timeframe: Timeframe para análise
        periodo: Número de períodos
    
    Returns:
        DataFrame com dados de preços
    """
    try:
        tf_mt5 = get_timeframe_mt5(timeframe)
        dados_combinados = pd.DataFrame()
        
        for simbolo in simbolos:
            try:
                rates = mt5.copy_rates_from_pos(simbolo, tf_mt5, 0, periodo)
                if rates is None or len(rates) == 0:
                    logger.warning(f"Sem dados para {simbolo}")
                    continue
                
                df = pd.DataFrame(rates)
                df['time'] = pd.to_datetime(df['time'], unit='s')
                df.set_index('time', inplace=True)
                
                # Usar preço de fechamento
                dados_combinados[simbolo] = df['close']
                
            except Exception as e:
                logger.error(f"Erro ao obter dados para {simbolo}: {e}")
        
        return dados_combinados
        
    except Exception as e:
        logger.error(f"Erro ao obter dados do MT5: {e}")
        return pd.DataFrame()

def preprocessar_dados(dados_brutos):
    """
    Preprocessa dados brutos do mercado.
    
    Args:
        dados_brutos: DataFrame com dados brutos
    
    Returns:
        DataFrame preprocessado
    """
    if dados_brutos.empty:
        return pd.DataFrame()
    
    dados_proc = dados_brutos.copy()
    
    # Remover colunas com muitos NaNs
    threshold = len(dados_proc) * 0.7  # 70% de dados válidos
    dados_proc = dados_proc.dropna(thresh=threshold, axis=1)
    
    # Forward fill para preencher gaps
    dados_proc = dados_proc.fillna(method='ffill')
    
    # Remover linhas com NaNs restantes
    dados_proc = dados_proc.dropna()
    
    return dados_proc

# ═══════════════════════════════════════════════════════════════════════════════
# 🔄 FUNÇÕES DE MONITORAMENTO E CACHE
# ═══════════════════════════════════════════════════════════════════════════════

def executar_analise_completa(timeframe='M15', periodo=100, enable_cointegration=True):
    """
    Executa análise completa de pares.
    
    Args:
        timeframe: Timeframe para análise
        periodo: Períodos históricos
        enable_cointegration: Usar filtro de cointegração
    
    Returns:
        Dict com resultados da análise
    """
    logger.info(f"Iniciando análise completa - Timeframe: {timeframe}, Período: {periodo}")
    
    try:
        # 1. Obter dados do mercado
        simbolos_todos = list(set(DEPENDENTE_REAL + INDEPENDENTE_REAL))
        dados_brutos = obter_dados_mt5(simbolos_todos, timeframe, periodo)
        
        if dados_brutos.empty:
            logger.error("Não foi possível obter dados do mercado")
            return {'erro': 'Sem dados do mercado'}
        
        # 2. Preprocessar dados
        dados_preprocessados = preprocessar_dados(dados_brutos)
        
        # 3. Calcular análise de pares
        resultados_analise = calcular_residuo_zscore_timeframe(
            dados_preprocessados, 
            enable_cointegration_filter=enable_cointegration
        )
        
        # 4. Filtrar apenas mesmo setor
        resultados_mesmo_setor = pares_mesmo_segmento(resultados_analise, SEGMENTOS_REAIS)
        
        # 5. Encontrar oportunidades
        oportunidades = encontrar_linha_monitorada(
            resultados_mesmo_setor,
            dados_preprocessados=dados_preprocessados,
            enable_cointegration_filter=enable_cointegration
        )
        
        # 6. Compilar resultado
        resultado_final = {
            'timestamp': datetime.now(),
            'timeframe': timeframe,
            'periodo': periodo,
            'total_pares_analisados': len(resultados_analise),
            'pares_mesmo_setor': len(resultados_mesmo_setor),
            'pares_aprovados_filtros': len(resultados_analise[resultados_analise['Filtros_OK']] if not resultados_analise.empty else 0),
            'oportunidades_encontradas': len(oportunidades),
            'dados_mercado_shape': dados_preprocessados.shape,
            'analise_completa': resultados_analise,
            'analise_mesmo_setor': resultados_mesmo_setor,
            'oportunidades': oportunidades,
            'status': 'sucesso'
        }
        
        logger.info(f"Análise completa finalizada: {resultado_final['oportunidades_encontradas']} oportunidades")
        
        return resultado_final
        
    except Exception as e:
        logger.error(f"Erro na análise completa: {e}")
        return {'erro': str(e), 'status': 'erro'}

# ═══════════════════════════════════════════════════════════════════════════════
# 🎯 INTERFACE PARA STREAMLIT
# ═══════════════════════════════════════════════════════════════════════════════

def get_analise_para_streamlit(timeframe='M15', periodo=100, filtros_customizados=None):
    """
    Interface simplificada para uso no Streamlit.
    
    Returns:
        Dict formatado para exibição no Streamlit
    """
    # Usar filtros customizados se fornecidos
    if filtros_customizados:
        filter_params = {**FILTER_PARAMS_REAL, **filtros_customizados}
    else:
        filter_params = FILTER_PARAMS_REAL
    
    # Executar análise
    resultado = executar_analise_completa(timeframe, periodo, 
                                        filter_params.get('enable_cointegration_filter', True))
    
    if resultado.get('status') == 'erro':
        return resultado
    
    # Formatar para Streamlit
    analise_formatada = {
        'resumo': {
            'timestamp': resultado['timestamp'],
            'total_analisados': resultado['total_pares_analisados'],
            'aprovados_filtros': resultado['pares_aprovados_filtros'],
            'oportunidades': resultado['oportunidades_encontradas'],
            'timeframe': timeframe,
            'periodo': periodo
        },
        'tabela_analise': resultado['analise_completa'],
        'tabela_mesmo_setor': resultado['analise_mesmo_setor'],
        'oportunidades': resultado['oportunidades'],
        'parametros_usados': filter_params
    }
    
    return analise_formatada

# ═══════════════════════════════════════════════════════════════════════════════
# 📊 FUNÇÕES DE OBTENÇÃO DE DADOS MT5
# ═══════════════════════════════════════════════════════════════════════════════

def obter_dados_mt5_analise(lista_ativos, periodo=200, timeframe=mt5.TIMEFRAME_H1):
    """
    Obtém dados do MT5 para análise de pares
    
    Args:
        lista_ativos: Lista de ativos para obter dados
        periodo: Número de períodos para obter
        timeframe: Timeframe do MT5
    
    Returns:
        DataFrame com dados dos ativos ou DataFrame vazio se erro
    """
    try:
        # Verificar se MT5 está conectado
        if not mt5.initialize():
            logger.error("Falha ao inicializar MT5")
            return pd.DataFrame()
        
        # Preparar dados
        dados_dict = {}
        end_time = datetime.now()
        
        for ativo in lista_ativos:
            try:
                # Obter dados do ativo
                rates = mt5.copy_rates_from(ativo, timeframe, end_time, periodo)
                
                if rates is not None and len(rates) > 0:
                    # Converter para DataFrame
                    df = pd.DataFrame(rates)
                    df['time'] = pd.to_datetime(df['time'], unit='s')
                    df.set_index('time', inplace=True)
                    
                    # Usar preço de fechamento
                    dados_dict[ativo] = df['close']
                else:
                    logger.warning(f"Não foi possível obter dados para {ativo}")
                    
            except Exception as e:
                logger.error(f"Erro ao obter dados de {ativo}: {e}")
                continue
        
        if dados_dict:
            # Criar DataFrame combinado
            dados_df = pd.DataFrame(dados_dict)
            
            # Preencher valores faltantes
            dados_df = dados_df.fillna(method='ffill').fillna(method='bfill')
            
            logger.info(f"Dados obtidos para {len(dados_dict)} ativos com {len(dados_df)} períodos")
            return dados_df
        else:
            logger.warning("Nenhum dado obtido do MT5")
            return pd.DataFrame()
            
    except Exception as e:
        logger.error(f"Erro geral ao obter dados MT5: {e}")
        return pd.DataFrame()
    finally:
        # Não fechar conexão MT5 aqui para manter conectado para outras operações
        pass
