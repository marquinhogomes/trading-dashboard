"""
Configurações Reais Extraídas do calculo_entradas_v55.py
Este módulo contém TODAS as configurações, parâmetros e listas reais do sistema original
"""

from datetime import datetime, timedelta
import pytz
import MetaTrader5 as mt5

# ═══════════════════════════════════════════════════════════════════════════════
# 📊 LISTAS DE ATIVOS REAIS (EXTRAÍDAS DO CÓDIGO ORIGINAL)
# ═══════════════════════════════════════════════════════════════════════════════

DEPENDENTE_REAL = [
    'ABEV3', 'ALOS3', 'ASAI3','BBAS3', 'BBDC4', 'BBSE3', 'BPAC11', 'BRAP4', 
    'BRFS3', 'BRKM5', 'CPFE3', 'CPLE6', 'CSAN3', 'CSNA3', 'CYRE3', 'ELET3', 
    'ELET6', 'EMBR3', 'ENEV3', 'ENGI11', 'EQTL3', 'EZTC3', 'FLRY3', 'GOAU4', 
    'HYPE3', 'IGTI11', 'IRBR3', 'ITSA4', 'ITUB4', 'KLBN11', 'MRFG3', 'NTCO3', 
    'PETR3', 'PETR4', 'PETZ3', 'PRIO3', 'RAIL3', 'RADL3', 'RECV3', 'RENT3', 
    'RDOR3', 'SANB11', 'SLCE3', 'SMTO3', 'SUZB3', 'TAEE11', 'TIMS3', 'TOTS3', 
    'UGPA3', 'VALE3', 'VBBR3', 'VIVT3', 'WEGE3', 'YDUQ3'
]

INDEPENDENTE_REAL = [
    'ABEV3', 'ALOS3', 'ASAI3', 'BBAS3',  'BBDC4', 'BBSE3', 'BPAC11', 'BRAP4', 
    'BRFS3', 'BRKM5', 'CPFE3', 'CPLE6', 'CSAN3', 'CSNA3', 'CYRE3', 'ELET3', 
    'ELET6', 'EMBR3', 'ENEV3', 'ENGI11', 'EQTL3', 'EZTC3', 'FLRY3', 'GOAU4', 
    'HYPE3', 'IGTI11', 'IRBR3', 'ITSA4', 'ITUB4', 'KLBN11', 'MRFG3', 'NTCO3', 
    'PETR3', 'PETR4', 'PETZ3', 'PRIO3', 'RAIL3', 'RADL3', 'RECV3', 'RENT3', 
    'RDOR3', 'SANB11', 'SLCE3', 'SMTO3', 'SUZB3', 'TAEE11', 'TIMS3', 'TOTS3', 
    'UGPA3', 'VALE3', 'VBBR3', 'VIVT3', 'WEGE3', 'YDUQ3'
]

# Símbolos de índices
IBOV_SYMBOL = 'IBOV'
WIN_SYMBOL = 'WIN$'
MINI_IND = 'WINM25'
MINI_DOL = 'WDOM25'

# ═══════════════════════════════════════════════════════════════════════════════
# 🏭 SEGMENTAÇÃO POR SETORES (REAL)
# ═══════════════════════════════════════════════════════════════════════════════

SEGMENTOS_REAIS = {
    'ABEV3': 'Bebidas',         'ALOS3': 'Saúde',           'ASAI3': 'Varejo Alimentar',
    'BBAS3': 'Bancos',          'BBDC4': 'Bancos',          'BBSE3': 'Seguros',
    'BPAC11': 'Bancos',         'BRAP4': 'Holding',         'BRFS3': 'Alimentos',
    'BRKM5': 'Química',         'CPFE3': 'Energia',         'CPLE6': 'Energia',
    'CSAN3': 'Siderurgia',      'CSNA3': 'Siderurgia',      'CYRE3': 'Construção',
    'ELET3': 'Energia',         'ELET6': 'Energia',         'EMBR3': 'Aeroespacial',
    'ENEV3': 'Energia',         'ENGI11': 'Energia',        'EQTL3': 'Energia',
    'EZTC3': 'Construção',      'FLRY3': 'Saúde',           'GOAU4': 'Siderurgia',      
    'HYPE3': 'Farmacêutica',    'IGTI11': 'Financeiro',     'IRBR3': 'Seguros',         
    'ITSA4': 'Financeiro',      'ITUB4': 'Bancos',          'KLBN11': 'Papel e Celulose',
    'MRFG3': 'Alimentos',       'NTCO3': 'Higiene/Beleza',  'PETR3': 'Petróleo',
    'PETR4': 'Petróleo',        'PETZ3': 'Varejo',          'PRIO3': 'Petróleo',
    'RAIL3': 'Logística',       'RADL3': 'Varejo',          'RECV3': 'Petróleo',
    'RENT3': 'Locação',         'RDOR3': 'Saúde',           'SANB11': 'Bancos',
    'SLCE3': 'Agro',            'SMTO3': 'Agro',            'SUZB3': 'Papel e Celulose',
    'TAEE11': 'Energia',        'TIMS3': 'Telecom',         'TOTS3': 'Tecnologia',
    'UGPA3': 'Distribuição',    'VALE3': 'Mineração',       'VBBR3': 'Transporte',
    'VIVT3': 'Telecom',         'WEGE3': 'Industrial',      'YDUQ3': 'Educação'
}

# ═══════════════════════════════════════════════════════════════════════════════
# ⏰ CONFIGURAÇÕES DE HORÁRIOS (REAIS)
# ═══════════════════════════════════════════════════════════════════════════════

# Horários principais do sistema
INICIA_APP = 9                          # App inicia às 9h (pré-abertura)
FINALIZA_APP = 24                       # App finaliza às 18h (pós-fechamento)
INICIA_PREGAO = 10                      # Pregão oficial: 10h
FINALIZA_PREGAO = 24                    # Pregão oficial: 17h
CAPTURA_SALDO_INICIAL_MINUTO = 3        # Captura saldo às 10:03h
CAPTURA_BID_ASK_MINUTO = 4              # Captura preços às 10:04h

# Horários para operações e ajustes
FINALIZA_ORDENS = 24                    # Para de enviar NOVAS ordens às 15h
AJUSTA_ORDENS = 24                      # Ajustes às 15h
AJUSTA_ORDENS_MINUTO = 10               # Ajustes às 15:10h
HORARIO_AJUSTE_STOPS = 24               # 15h - Ajustar stops de posições abertas
HORARIO_REMOVE_PENDENTES = 24           # 15h - Remover ordens pendentes
HORARIO_FECHAMENTO_TOTAL = 24           # 16h - Fechamento forçado

# Janelas de tempo para diferentes atividades
JANELA_ANALISE_POSICOES = (10, 24)      # 10h-17h: Monitorar posições
JANELA_NOVAS_OPERACOES = (10, 24)       # 10h-16h: Aceitar novas operações
JANELA_AJUSTES_DINAMICOS = (10, 24)     # 10h-17h: Ajustes dinâmicos
JANELA_BREAK_EVEN = (10, 24)            # 10h-17h: Break-even automático

# ═══════════════════════════════════════════════════════════════════════════════
# 💰 PARÂMETROS DE TRADING (REAIS)
# ═══════════════════════════════════════════════════════════════════════════════

# Limites de operações
LIMITE_OPERACOES = 6
INDEP_LIMITE_OPERACOES = 6

# Valores de operação
VALOR_OPERACAO = 10000          # Valor para operações dependentes
VALOR_OPERACAO_IND = 5000       # Valor para operações independentes

# Limites de lucro e prejuízo
LIMITE_LUCRO = 120
LIMITE_PREJUIZO = 120

# Parâmetros estatísticos
PVALOR = 0.05                   # P-valor para testes estatísticos
APETITE_PERC_MEDIA = 1.0        # Apetite percentual da média

# Desvios para operações dependentes
DESVIO_GAIN_COMPRA = 1.012      # Desvio para gain em compras
DESVIO_LOSS_COMPRA = 0.988      # Desvio para loss em compras
DESVIO_GAIN_VENDA = 0.988       # Desvio para gain em vendas
DESVIO_LOSS_VENDA = 1.012       # Desvio para loss em vendas

# Desvios para operações independentes
DESVIO_GAIN_COMPRA_IND = 1.03   # Desvio para gain em compras independentes
DESVIO_LOSS_COMPRA_IND = 0.97   # Desvio para loss em compras independentes
DESVIO_GAIN_VENDA_IND = 0.97    # Desvio para gain em vendas independentes
DESVIO_LOSS_VENDA_IND = 1.03    # Desvio para loss em vendas independentes

# ═══════════════════════════════════════════════════════════════════════════════
# 📊 PARÂMETROS DE ANÁLISE (REAIS)
# ═══════════════════════════════════════════════════════════════════════════════

# Períodos para análise
PERIODO_REAL = [70, 100, 120, 140, 160, 180, 200, 220, 240, 250]

# Prefixos e contadores
PREFIXO = "2"
SERIE_ID_COUNTER = 200000

# Filtros de análise (configuração real do sistema)
FILTER_PARAMS_REAL = {
    'r2_min': 0.5,                          # R² mínimo para correlação
    'beta_max': 1.5,                        # Beta máximo permitido
    'coef_var_max': 5000.0,                 # Coeficiente de variação máximo
    'adf_p_value_max': 0.05,                # P-valor máximo para teste ADF
    'use_coint_test': True,                 # Usar teste de cointegração
    'use_adf_critical': False,              # Usar valor crítico ADF
    'enable_cointegration_filter': True,    # Habilitar filtro de cointegração
}

# ═══════════════════════════════════════════════════════════════════════════════
# 🔧 MAPEAMENTOS TÉCNICOS
# ═══════════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════════
# 🚀 CONFIGURAÇÕES AVANÇADAS (EXTRAÍDAS DO ORIGINAL)
# ═══════════════════════════════════════════════════════════════════════════════

# Configurações GARCH e volatilidade
USE_GARCH = True                        # Usar GARCH para calcular price min/max
GARCH_FALLBACK_MULTIPLIER = 0.02        # Multiplicador para fallback quando GARCH falha (2%)

# Configurações de Cache e Threading
ARIMA_CACHE = {}
LSTM_CACHE = {}
CACHE_REG = {}

# Configurações de Arquivos
ARQUIVO_ABERTURA_DEPENDENTE = "abertura_dependente.json"
ARQUIVO_ABERTURA_INDEPENDENTE = "abertura_independente.json"
ARQUIVO_SALDO_INICIAL = "saldo_inicial.json"

# Configurações de Modelo IA
MODELO_IA_PATH = "modelo_ia.keras"
SCALER_IA_PATH = "scaler_ia.save"

# ═══════════════════════════════════════════════════════════════════════════════
# 📈 CONFIGURAÇÕES DE ANÁLISE ESTATÍSTICA (REAIS)
# ═══════════════════════════════════════════════════════════════════════════════

# Mapeamentos de timeframe
MAPA_TIMEFRAMES_PARA_MT5 = {
    "M15": 15,      # mt5.TIMEFRAME_M15
    "H1": 16385,    # mt5.TIMEFRAME_H1  
    "D1": 16408,    # mt5.TIMEFRAME_D1
    1: 15,          # M15
    2: 16385,       # H1
    3: 16408,       # D1
    15: 15,         # M15 direto
    16385: 16385,   # H1 direto
    16408: 16408    # D1 direto
}

MAPA_NOMES_TIMEFRAMES = {
    1: "M15", 2: "H1", 3: "D1",
    15: "M15", 16385: "H1", 16408: "D1",
    "M15": "M15", "H1": "H1", "D1": "D1"
}

# Mapeamento MT5 para Pandas frequência
MT5_TO_PANDAS_FREQ = {
    mt5.TIMEFRAME_M1: '1T',
    mt5.TIMEFRAME_M2: '2T',
    mt5.TIMEFRAME_M3: '3T',
    mt5.TIMEFRAME_M5: '5T',
    mt5.TIMEFRAME_M10: '10T',
    mt5.TIMEFRAME_M15: '15T',
    mt5.TIMEFRAME_M30: '30T',
    mt5.TIMEFRAME_H1: '1H',
    mt5.TIMEFRAME_H2: '2H',
    mt5.TIMEFRAME_H3: '3H',
    mt5.TIMEFRAME_H4: '4H',
    mt5.TIMEFRAME_H6: '6H',
    mt5.TIMEFRAME_H8: '8H',
    mt5.TIMEFRAME_H12: '12H',
    mt5.TIMEFRAME_D1: '1D',
    mt5.TIMEFRAME_W1: '1W',
    mt5.TIMEFRAME_MN1: '1M'
}

# ═══════════════════════════════════════════════════════════════════════════════
# 🎯 CONFIGURAÇÕES PARA INTERFACE STREAMLIT
# ═══════════════════════════════════════════════════════════════════════════════

def get_real_config_for_streamlit():
    """
    Retorna configurações reais formatadas para uso no Streamlit
    """
    return {
        # Listas de ativos
        'pairs_dependente': DEPENDENTE_REAL,
        'pairs_independente': INDEPENDENTE_REAL,
        'pairs_combined': list(set(DEPENDENTE_REAL + INDEPENDENTE_REAL)),
        'segmentos': SEGMENTOS_REAIS,
        
        # Índices
        'ibov_symbol': IBOV_SYMBOL,
        'win_symbol': WIN_SYMBOL,
        'mini_ind': MINI_IND,
        'mini_dol': MINI_DOL,
        
        # Horários
        'horarios': {
            'inicia_app': INICIA_APP,
            'finaliza_app': FINALIZA_APP,
            'inicia_pregao': INICIA_PREGAO,
            'finaliza_pregao': FINALIZA_PREGAO,
            'captura_saldo_minuto': CAPTURA_SALDO_INICIAL_MINUTO,
            'captura_bid_ask_minuto': CAPTURA_BID_ASK_MINUTO,
            'finaliza_ordens': FINALIZA_ORDENS,
            'ajusta_ordens': AJUSTA_ORDENS,
        },
        
        # Parâmetros de trading
        'trading': {
            'limite_operacoes': LIMITE_OPERACOES,
            'limite_operacoes_ind': INDEP_LIMITE_OPERACOES,
            'valor_operacao': VALOR_OPERACAO,
            'valor_operacao_ind': VALOR_OPERACAO_IND,
            'limite_lucro': LIMITE_LUCRO,
            'limite_prejuizo': LIMITE_PREJUIZO,
            'pvalor': PVALOR,
            'apetite_perc_media': APETITE_PERC_MEDIA,
        },
        
        # Desvios
        'desvios': {
            'gain_compra': DESVIO_GAIN_COMPRA,
            'loss_compra': DESVIO_LOSS_COMPRA,
            'gain_venda': DESVIO_GAIN_VENDA,
            'loss_venda': DESVIO_LOSS_VENDA,
            'gain_compra_ind': DESVIO_GAIN_COMPRA_IND,
            'loss_compra_ind': DESVIO_LOSS_COMPRA_IND,
            'gain_venda_ind': DESVIO_GAIN_VENDA_IND,
            'loss_venda_ind': DESVIO_LOSS_VENDA_IND,
        },
        
        # Análise
        'analise': {
            'periodos': PERIODO_REAL,
            'prefixo': PREFIXO,
            'filter_params': FILTER_PARAMS_REAL.copy(),
        },
        
        # Mapeamentos
        'mt5_freq_map': MT5_TO_PANDAS_FREQ.copy()
    }

def get_setores_disponiveis():
    """Retorna lista de setores únicos"""
    return sorted(list(set(SEGMENTOS_REAIS.values())))

def get_pares_por_setor(setor):
    """Retorna pares de um setor específico"""
    return [par for par, par_setor in SEGMENTOS_REAIS.items() if par_setor == setor]

def is_horario_operacao(hora_atual=None):
    """Verifica se está no horário de operação"""
    if hora_atual is None:
        hora_atual = datetime.now().hour
    return INICIA_PREGAO <= hora_atual <= FINALIZA_PREGAO

def get_janela_ativa(hora_atual=None):
    """Retorna qual janela de operação está ativa"""
    if hora_atual is None:
        hora_atual = datetime.now().hour
    
    janelas = {
        'analise_posicoes': JANELA_ANALISE_POSICOES,
        'novas_operacoes': JANELA_NOVAS_OPERACOES,
        'ajustes_dinamicos': JANELA_AJUSTES_DINAMICOS,
        'break_even': JANELA_BREAK_EVEN
    }
    
    ativas = []
    for nome, (inicio, fim) in janelas.items():
        if inicio <= hora_atual <= fim:
            ativas.append(nome)
    
    return ativas

# ═══════════════════════════════════════════════════════════════════════════════
# 🔄 FUNÇÕES AUXILIARES DO SISTEMA REAL
# ═══════════════════════════════════════════════════════════════════════════════

def pares_mesmo_segmento(df, segmentos=None):
    """
    Filtra DataFrame de pares para manter apenas aqueles do mesmo segmento.
    Função original extraída do calculo_entradas_v55.py
    """
    if segmentos is None:
        segmentos = SEGMENTOS_REAIS
    
    return df[
        df.apply(lambda x: segmentos.get(x['Dependente']) == segmentos.get(x['Independente']), axis=1)
    ].copy()

def get_timeframe_mt5(timeframe_input):
    """
    Converte entrada de timeframe para valor MT5
    """
    return MAPA_TIMEFRAMES_PARA_MT5.get(timeframe_input, 15)  # Default M15

def get_timeframe_name(timeframe_input):
    """
    Converte entrada de timeframe para nome legível
    """
    return MAPA_NOMES_TIMEFRAMES.get(timeframe_input, str(timeframe_input))

def get_pandas_freq(mt5_timeframe):
    """
    Converte timeframe MT5 para frequência Pandas
    """
    return MT5_TO_PANDAS_FREQ.get(mt5_timeframe, '15T')

def extrair_valor(valor):
    """
    Extrai valor numérico de diferentes tipos de objetos.
    Função original extraída do calculo_entradas_v55.py
    """
    # Se o objeto tiver atributo 'iloc', tente acessar o primeiro elemento
    if hasattr(valor, 'iloc'):
        try:
            return float(valor.iloc[0])
        except Exception:
            return float(valor)
    # Se for um numpy array, verifique sua dimensão
    if hasattr(valor, 'shape'):
        if valor.shape == ():
            return float(valor)
        else:
            return float(valor[0])
    # Caso contrário, tente converter diretamente
    return float(valor)

# ═══════════════════════════════════════════════════════════════════════════════
# 🎯 CONFIGURAÇÕES DE VALIDAÇÃO E CONTROLE DE QUALIDADE
# ═══════════════════════════════════════════════════════════════════════════════

def validar_configuracao():
    """
    Valida se todas as configurações estão corretas
    """
    erros = []
    
    # Validar ativos
    if not DEPENDENTE_REAL or not INDEPENDENTE_REAL:
        erros.append("Listas de ativos dependentes/independentes vazias")
    
    # Validar segmentos
    dependentes_sem_segmento = [ativo for ativo in DEPENDENTE_REAL if ativo not in SEGMENTOS_REAIS]
    if dependentes_sem_segmento:
        erros.append(f"Ativos dependentes sem segmento: {dependentes_sem_segmento}")
    
    # Validar parâmetros
    if LIMITE_OPERACOES <= 0 or VALOR_OPERACAO <= 0:
        erros.append("Parâmetros de trading inválidos")
    
    # Validar horários
    if INICIA_PREGAO >= FINALIZA_PREGAO:
        erros.append("Horários de pregão inválidos")
    
    if erros:
        raise ValueError(f"Configuração inválida: {'; '.join(erros)}")
    
    return True

# ═══════════════════════════════════════════════════════════════════════════════
# 📊 INFORMAÇÕES DO SISTEMA
# ═══════════════════════════════════════════════════════════════════════════════

SYSTEM_INFO = {
    'version': '5.5.0',
    'source': 'calculo_entradas_v55.py',
    'source_file': 'calculo_entradas_v55.py',  # Adicionar chave que estava faltando
    'config_type': 'REAL',  # Adicionar tipo de configuração
    'total_dependentes': len(DEPENDENTE_REAL),
    'total_independentes': len(INDEPENDENTE_REAL), 
    'total_setores': len(set(SEGMENTOS_REAIS.values())),
    'extracted_date': '2025-06-18',
    'integration_complete': True
}

# Validar configuração ao importar
try:
    validar_configuracao()
    print(f"✅ Config real validada: {SYSTEM_INFO['total_dependentes']} dependentes, {SYSTEM_INFO['total_setores']} setores")
except Exception as e:
    print(f"❌ Erro na validação da configuração: {e}")

# ═══════════════════════════════════════════════════════════════════════════════
# 🔧 CONSTANTES FINAIS
# ═══════════════════════════════════════════════════════════════════════════════

# Timezone padrão
TIMEZONE_BRASIL = "America/Sao_Paulo"

# Cache global para resultados
GLOBAL_CACHE = {
    'analysis_results': {},
    'trading_signals': [],
    'market_data': {},
    'last_update': None
}
