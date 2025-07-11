"""
Configurações avançadas do sistema de trading
"""

# Configurações de conexão MetaTrader 5
MT5_CONFIG = {
    'timeout': 60000,  # Timeout de conexão em ms
    'retries': 3,      # Número de tentativas de reconexão
    'path': None,      # Caminho do terminal (None = padrão)
}

# Configurações de análise
ANALYSIS_CONFIG = {
    'default_timeframe': 'D1',
    'min_data_points': 100,
    'max_data_points': 2000,
    'cache_duration': 300,  # 5 minutos
    'parallel_processing': True,
    'max_workers': 4,
}

# Configurações de risco
RISK_CONFIG = {
    'max_daily_loss': 0.05,     # 5% do capital
    'max_positions': 10,
    'max_exposure_per_pair': 0.02,  # 2% por par
    'emergency_stop_loss': 0.10,    # 10% stop de emergência
    'correlation_limit': 0.8,       # Limite de correlação entre posições
}

# Configurações de trading
TRADING_CONFIG = {
    'magic_number_base': 123456,
    'comment_prefix': 'TradingSystem_',
    'slippage': 3,
    'deviation': 20,
    'execution_timeout': 30,
    'min_free_margin': 1000,  # Margem mínima livre
}

# Configurações de sinais
SIGNAL_CONFIG = {
    'zscore_entry': 2.0,
    'zscore_exit': 0.5,
    'min_confidence': 0.7,
    'signal_cooldown': 300,  # 5 minutos entre sinais do mesmo par
    'volume_filter': True,
    'spread_filter': True,
}

# Configurações de cointegração
COINTEGRATION_CONFIG = {
    'max_p_value': 0.05,
    'min_test_period': 100,
    'lookback_period': 252,  # 1 ano de dados
    'retest_frequency': 24,  # Re-testar a cada 24 horas
}

# Configurações de modelos
MODEL_CONFIG = {
    'arima_max_order': (5, 2, 5),
    'garch_max_order': (3, 3),
    'validation_split': 0.2,
    'cross_validation_folds': 5,
    'model_retrain_frequency': 168,  # Re-treinar a cada 7 dias
}

# Configurações de interface
UI_CONFIG = {
    'refresh_interval': 30,  # segundos
    'max_log_entries': 1000,
    'chart_theme': 'plotly_white',
    'auto_scroll_logs': True,
    'sound_alerts': False,
}

# Configurações de notificações
NOTIFICATION_CONFIG = {
    'email_enabled': False,
    'telegram_enabled': False,
    'discord_enabled': False,
    'alert_levels': ['ERROR', 'WARNING'],
    'position_alerts': True,
    'pnl_alerts': True,
}

# Pares de ações padrão organizados por setor
DEFAULT_PAIRS_BY_SECTOR = {
    'Petróleo e Gás': ['PETR3', 'PETR4', 'PRIO3', 'RECV3'],
    'Mineração': ['VALE3', 'CSNA3', 'GOAU4', 'USIM5', 'GGBR4'],
    'Bancos': ['ITUB4', 'BBDC4', 'SANB11', 'BPAC11', 'BBAS3'],
    'Varejo': ['MGLU3', 'LREN3', 'AMER3', 'LAME4', 'VVAR3'],
    'Utilities': ['ELET3', 'ELET6', 'CMIG4', 'CPFE3', 'ETO'],
    'Telecomunicações': ['VIVT3', 'TIMP3', 'TIMS3'],
    'Transporte': ['RAIL3', 'CCRO3', 'EZTC3'],
    'Alimentação': ['JBSS3', 'BRFS3', 'MRFG3'],
    'Siderurgia': ['USIM5', 'CSNA3', 'GGBR4', 'GOAU4'],
    'Tecnologia': ['TOTS3', 'LWSA3', 'MELI34'],
    'Papel e Celulose': ['SUZB3', 'KLBN11', 'FIBR3'],
    'Construção': ['MRVE3', 'CYRELA', 'EZTC3'],
    'Saúde': ['RDOR3', 'HAPV3', 'QUAL3'],
    'Educação': ['COGN3', 'YDUQ3'],
    'Logística': ['LOGN3', 'RENT3'],
}

# Filtros de qualidade para pares
PAIR_QUALITY_FILTERS = {
    'min_volume_daily': 10000000,    # Volume diário mínimo
    'max_spread_percent': 0.5,       # Spread máximo em %
    'min_market_cap': 5000000000,    # Capitalização mínima
    'min_liquidity_ratio': 0.1,     # Índice de liquidez mínimo
    'exclude_otc': True,             # Excluir ações OTC
    'exclude_penny_stocks': True,    # Excluir penny stocks
}

# Configurações de backtesting
BACKTEST_CONFIG = {
    'initial_capital': 100000,
    'commission_rate': 0.0005,  # 0.05% por operação
    'slippage_rate': 0.0001,    # 0.01% de slippage
    'min_test_period': 252,     # Mínimo 1 ano
    'walk_forward_steps': 30,   # Passos para walk-forward
    'out_of_sample_ratio': 0.3, # 30% para teste out-of-sample
}

# Configurações de logging
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '{time:YYYY-MM-DD HH:mm:ss} | {level} | {name} | {message}',
    'rotation': '100 MB',
    'retention': '30 days',
    'compression': 'gz',
}

# Configurações de performance
PERFORMANCE_CONFIG = {
    'enable_multiprocessing': True,
    'max_cpu_usage': 80,        # % máximo de CPU
    'max_memory_usage': 4096,   # MB máximo de RAM
    'gc_frequency': 3600,       # Garbage collection a cada hora
    'optimize_pandas': True,
}

# Configurações de segurança
SECURITY_CONFIG = {
    'encrypt_credentials': True,
    'session_timeout': 3600,    # 1 hora
    'max_login_attempts': 3,
    'audit_trail': True,
    'backup_frequency': 86400,  # 24 horas
}

# Configurações de API (para integrações futuras)
API_CONFIG = {
    'rate_limit': 100,          # Requests por minuto
    'timeout': 30,              # Timeout em segundos
    'retries': 3,
    'backoff_factor': 1.0,
}

# Timeframes disponíveis
TIMEFRAMES = {
    'M1': {'name': '1 Minuto', 'seconds': 60},
    'M5': {'name': '5 Minutos', 'seconds': 300},
    'M15': {'name': '15 Minutos', 'seconds': 900},
    'M30': {'name': '30 Minutos', 'seconds': 1800},
    'H1': {'name': '1 Hora', 'seconds': 3600},
    'H4': {'name': '4 Horas', 'seconds': 14400},
    'D1': {'name': '1 Dia', 'seconds': 86400},
    'W1': {'name': '1 Semana', 'seconds': 604800},
    'MN1': {'name': '1 Mês', 'seconds': 2592000},
}

# Indicadores técnicos disponíveis
TECHNICAL_INDICATORS = {
    'trend': ['SMA', 'EMA', 'MACD', 'ADX', 'Parabolic SAR'],
    'momentum': ['RSI', 'Stochastic', 'Williams %R', 'CCI'],
    'volatility': ['Bollinger Bands', 'ATR', 'Keltner Channels'],
    'volume': ['OBV', 'Volume SMA', 'VWAP'],
    'statistical': ['Z-Score', 'Correlation', 'Beta', 'Sharpe Ratio']
}

# Configurações de alertas por nível
ALERT_LEVELS = {
    'INFO': {'color': 'blue', 'icon': 'ℹ️', 'sound': None},
    'WARNING': {'color': 'yellow', 'icon': '⚠️', 'sound': 'warning.wav'},
    'ERROR': {'color': 'red', 'icon': '❌', 'sound': 'error.wav'},
    'SUCCESS': {'color': 'green', 'icon': '✅', 'sound': 'success.wav'},
    'TRADE': {'color': 'purple', 'icon': '📈', 'sound': 'trade.wav'},
}

# Configurações de export/import
EXPORT_CONFIG = {
    'default_format': 'xlsx',
    'include_charts': True,
    'compress_files': True,
    'max_file_size': 100,  # MB
    'auto_backup': True,
    'cloud_sync': False,
}
