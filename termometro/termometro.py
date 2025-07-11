
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import xgboost as xgb
from datetime import datetime, timedelta
import talib
import joblib

class IBOVPredictor:
    """
    Modelo preditivo para IBOV com janela de 1 minuto
    Combina análise técnica, machine learning e filtros de qualidade
    """
    def __init__(self):
        self.models = {}
        self.scaler = StandardScaler()
        self.feature_names = []
        self.is_trained = False
        
    def calculate_technical_indicators(self, df):
        """
        Calcula todos os indicadores técnicos necessários
        """
        data = df.copy()
        
        # Indicadores de Momentum
        data['rsi_2'] = talib.RSI(data['close'], timeperiod=2)
        data['rsi_5'] = talib.RSI(data['close'], timeperiod=5)
        data['rsi_14'] = talib.RSI(data['close'], timeperiod=14)
        
        # Stochastic
        data['stoch_k'], data['stoch_d'] = talib.STOCH(
            data['high'], data['low'], data['close'],
            fastk_period=5, slowk_period=3, slowd_period=3
        )
        
        # Williams %R
        data['williams_r'] = talib.WILLR(
            data['high'], data['low'], data['close'], timeperiod=14
        )
        
        # MACD
        data['macd'], data['macd_signal'], data['macd_hist'] = talib.MACD(
            data['close'], fastperiod=12, slowperiod=26, signalperiod=9
        )
        
        # Médias Móveis
        data['ema_9'] = talib.EMA(data['close'], timeperiod=9)
        data['ema_21'] = talib.EMA(data['close'], timeperiod=21)
        data['sma_20'] = talib.SMA(data['close'], timeperiod=20)
        
        # TEMA (Triple Exponential Moving Average)
        data['tema'] = talib.TEMA(data['close'], timeperiod=21)
        
        # Bollinger Bands
        data['bb_upper'], data['bb_middle'], data['bb_lower'] = talib.BBANDS(
            data['close'], timeperiod=20, nbdevup=2, nbdevdn=2
        )
        
        # Volume Indicators
        data['volume_sma'] = talib.SMA(data['volume'], timeperiod=20)
        data['ad_line'] = talib.AD(data['high'], data['low'], data['close'], data['volume'])
        data['obv'] = talib.OBV(data['close'], data['volume'])
        
        # Money Flow Index
        data['mfi'] = talib.MFI(
            data['high'], data['low'], data['close'], data['volume'], timeperiod=14
        )
        
        # Average True Range (Volatilidade)
        data['atr'] = talib.ATR(data['high'], data['low'], data['close'], timeperiod=14)
        
        # Commodity Channel Index
        data['cci'] = talib.CCI(data['high'], data['low'], data['close'], timeperiod=14)
        
        return data

    def engineer_features(self, df):
        """
        Engenharia de features avançada
        """
        data = df.copy()
        
        # Features de Preço
        data['returns_1min'] = data['close'].pct_change()
        data['returns_2min'] = data['close'].pct_change(2)
        data['returns_5min'] = data['close'].pct_change(5)
        
        data['high_low_ratio'] = (data['high'] - data['low']) / data['close']
        data['close_open_ratio'] = (data['close'] - data['open']) / data['open']
        
        # Features de Momentum Normalizadas
        data['rsi_2_norm'] = (data['rsi_2'] - 50) / 50
        data['rsi_5_norm'] = (data['rsi_5'] - 50) / 50
        data['stoch_norm'] = (data['stoch_k'] - 50) / 50
        data['williams_norm'] = (data['williams_r'] + 50) / 50
        
        # Features de Médias Móveis
        data['price_ema9_diff'] = (data['close'] - data['ema_9']) / data['ema_9']
        data['ema9_ema21_diff'] = (data['ema_9'] - data['ema_21']) / data['ema_21']
        
        # Features de Bollinger Bands
        data['bb_position'] = (data['close'] - data['bb_lower']) / (data['bb_upper'] - data['bb_lower'])
        data['bb_width'] = (data['bb_upper'] - data['bb_lower']) / data['bb_middle']
        
        # Features de Volume
        data['volume_ratio'] = data['volume'] / data['volume_sma']
        data['volume_spike'] = (data['volume'] > data['volume_sma'] * 2).astype(int)
        
        # VWAP
        data['vwap'] = (data['close'] * data['volume']).cumsum() / data['volume'].cumsum()
        data['vwap_distance'] = (data['close'] - data['vwap']) / data['vwap']
        
        # Features de Volatilidade
        data['volatility_20'] = data['returns_1min'].rolling(20).std()
        data['atr_normalized'] = data['atr'] / data['close']
        
        # Regime de Volatilidade
        vol_quantiles = data['volatility_20'].quantile([0.33, 0.66])
        data['volatility_regime'] = pd.cut(
            data['volatility_20'], 
            bins=[-np.inf, vol_quantiles.iloc[0], vol_quantiles.iloc[1], np.inf],
            labels=[0, 1, 2]  # 0=Baixa, 1=Média, 2=Alta
        ).astype(float)
        
        # Features de Padrões de Candlestick
        data['doji'] = talib.CDLDOJI(data['open'], data['high'], data['low'], data['close'])
        data['hammer'] = talib.CDLHAMMER(data['open'], data['high'], data['low'], data['close'])
        data['engulfing'] = talib.CDLENGULFING(data['open'], data['high'], data['low'], data['close'])
        
        # Features de Horário (assumindo dados durante horário de pregão)
        if 'datetime' in data.columns:
            data['hour'] = pd.to_datetime(data['datetime']).dt.hour
            data['minute'] = pd.to_datetime(data['datetime']).dt.minute
            data['session_factor'] = self._get_session_factor(data['hour'], data['minute'])
        
        # Features Lag (dados históricos)
        for lag in [1, 2, 3, 5]:
            data[f'returns_lag_{lag}'] = data['returns_1min'].shift(lag)
            data[f'volume_ratio_lag_{lag}'] = data['volume_ratio'].shift(lag)
            data[f'rsi_2_lag_{lag}'] = data['rsi_2_norm'].shift(lag)
        
        return data

    def _get_session_factor(self, hour, minute):
        """
        Fator baseado na sessão de negociação
        """
        time_factor = np.ones(len(hour))
        
        # Abertura (10:00-11:00) - Maior volatilidade
        opening_mask = (hour == 10)
        time_factor[opening_mask] = 1.2
        
        # Fechamento (17:00-18:00) - Maior volatilidade
        closing_mask = (hour >= 17)
        time_factor[closing_mask] = 1.2
        
        # Meio do dia (12:00-14:00) - Menor volatilidade
        midday_mask = ((hour >= 12) & (hour < 14))
        time_factor[midday_mask] = 0.8
        
        return time_factor

    def create_target(self, df, threshold=0.001):
        """
        Cria variável target para classificação
        threshold: 0.001 = 0.1% de movimento mínimo
        """
        data = df.copy()
        
        # Retorno futuro em 1 minuto
        data['future_return'] = data['close'].shift(-1) / data['close'] - 1
        
        # Classificação: 0=Baixa, 1=Neutro, 2=Alta
        conditions = [
            data['future_return'] < -threshold,
            (data['future_return'] >= -threshold) & (data['future_return'] <= threshold),
            data['future_return'] > threshold
        ]
        
        data['target'] = np.select(conditions, [0, 1, 2])
        
        return data

    def select_features(self, df):
        """
        Seleciona features relevantes para o modelo
        """
        feature_columns = [
            # Momentum
            'rsi_2_norm', 'rsi_5_norm', 'stoch_norm', 'williams_norm',
            'macd', 'macd_signal', 'macd_hist', 'cci',
            
            # Médias Móveis
            'price_ema9_diff', 'ema9_ema21_diff',
            
            # Bollinger
            'bb_position', 'bb_width',
            
            # Volume
            'volume_ratio', 'volume_spike', 'vwap_distance', 'mfi',
            
            # Volatilidade
            'atr_normalized', 'volatility_regime',
            
            # Padrões
            'doji', 'hammer', 'engulfing',
            
            # Features de Preço
            'high_low_ratio', 'close_open_ratio',
            'returns_1min', 'returns_2min', 'returns_5min',
            
            # Features Lag
            'returns_lag_1', 'returns_lag_2', 'returns_lag_3', 'returns_lag_5',
            'volume_ratio_lag_1', 'volume_ratio_lag_2', 'volume_ratio_lag_3',
            'rsi_2_lag_1', 'rsi_2_lag_2', 'rsi_2_lag_3'
        ]
        
        # Adicionar session_factor se disponível
        if 'session_factor' in df.columns:
            feature_columns.append('session_factor')
        
        # Filtrar apenas colunas que existem no DataFrame
        available_features = [col for col in feature_columns if col in df.columns]
        
        self.feature_names = available_features
        return df[available_features]

    def prepare_data(self, df):
        """
        Pipeline completo de preparação dos dados
        """
        print("Calculando indicadores técnicos...")
        data = self.calculate_technical_indicators(df)
        
        print("Engenharia de features...")
        data = self.engineer_features(data)
        
        print("Criando target...")
        data = self.create_target(data)
        
        print("Selecionando features...")
        X = self.select_features(data)
        y = data['target']
        
        # Remover linhas com NaN
        mask = ~(X.isnull().any(axis=1) | y.isnull())
        X = X[mask]
        y = y[mask]
        data_clean = data[mask]
        
        print(f"Dataset final: {len(X)} amostras, {len(X.columns)} features")
        print(f"Distribuição do target: {y.value_counts().to_dict()}")
        
        return X, y, data_clean

    def train_models(self, X, y):
        """
        Treina ensemble de modelos
        """
        print("Treinando modelos...")
        
        # Normalizar features
        X_scaled = self.scaler.fit_transform(X)
        
        # Random Forest
        self.models['rf'] = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=10,
            min_samples_leaf=5,
            random_state=42,
            n_jobs=-1
        )
        
        # XGBoost
        self.models['xgb'] = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42
        )
        
        # Gradient Boosting
        self.models['gb'] = GradientBoostingClassifier(
            n_estimators=100,
            max_depth=8,
            learning_rate=0.1,
            subsample=0.8,
            random_state=42
        )
        
        # Treinar modelos
        for name, model in self.models.items():
            print(f"Treinando {name}...")
            if name == 'rf':
                model.fit(X_scaled, y)
            else:
                model.fit(X, y)
        
        self.is_trained = True
        print("Treinamento concluído!")

    def predict(self, X):
        """
        Faz predições com ensemble de modelos
        """
        if not self.is_trained:
            raise ValueError("Modelo não foi treinado ainda!")
        
        X_scaled = self.scaler.transform(X)
        
        # Predições de cada modelo
        pred_rf = self.models['rf'].predict_proba(X_scaled)
        pred_xgb = self.models['xgb'].predict_proba(X)
        pred_gb = self.models['gb'].predict_proba(X)
        
        # Ensemble com pesos
        ensemble_pred = (
            0.4 * pred_rf +
            0.4 * pred_xgb +
            0.2 * pred_gb
        )
        
        # Classe predita e probabilidades
        predicted_class = np.argmax(ensemble_pred, axis=1)
        confidence = np.max(ensemble_pred, axis=1)
        
        return predicted_class, confidence, ensemble_pred

    def calculate_confidence_factors(self, df_current):
        """
        Calcula fatores de confiança para a predição
        """
        factors = {}
        
        # Fator de volatilidade
        current_vol = df_current['volatility_20'].iloc[-1]
        vol_regime = df_current['volatility_regime'].iloc[-1]
        factors['volatility'] = 0.8 if vol_regime == 1 else 0.6  # Prefere vol média
        
        # Fator de volume
        vol_ratio = df_current['volume_ratio'].iloc[-1]
        factors['volume'] = min(1.0, vol_ratio / 2.0)  # Volume alto = mais confiança
        
        # Fator de tendência (alinhamento de timeframes)
        short_trend = df_current['price_ema9_diff'].iloc[-1]
        medium_trend = df_current['ema9_ema21_diff'].iloc[-1]
        factors['trend_alignment'] = 1.0 if short_trend * medium_trend > 0 else 0.7
        
        # Fator de momentum
        rsi_2 = df_current['rsi_2'].iloc[-1]
        factors['momentum'] = 1.0 if 30 < rsi_2 < 70 else 0.8  # Evita extremos
        
        return factors

    def should_trade(self, prediction, confidence, confidence_factors, min_confidence=0.6):
        """
        Decide se deve fazer trade baseado em filtros de qualidade
        """
        # Confiança mínima do modelo
        if confidence < min_confidence:
            return False, f"Confiança baixa: {confidence:.3f}"
        
        # Classe neutra não gera sinal
        if prediction == 1:
            return False, "Predição neutra"
        
        # Fatores de confiança
        avg_factor = np.mean(list(confidence_factors.values()))
        if avg_factor < 0.7:
            return False, f"Fatores desfavoráveis: {avg_factor:.3f}"
        
        return True, "OK"

    def backtest(self, X, y, data, n_splits=5):
        """
        Realiza backtesting com validação temporal
        """
        print("Iniciando backtesting...")
        
        tscv = TimeSeriesSplit(n_splits=n_splits)
        results = []
        
        for fold, (train_idx, test_idx) in enumerate(tscv.split(X)):
            print(f"Fold {fold + 1}/{n_splits}")
            
            X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
            y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
            
            # Treinar modelos temporários
            temp_predictor = IBOVPredictor()
            temp_predictor.feature_names = self.feature_names
            temp_predictor.train_models(X_train, y_train)
            
            # Fazer predições
            predictions, confidences, _ = temp_predictor.predict(X_test)
            
            # Calcular métricas
            from sklearn.metrics import accuracy_score, precision_score, recall_score
            
            accuracy = accuracy_score(y_test, predictions)
            precision = precision_score(y_test, predictions, average='weighted')
            recall = recall_score(y_test, predictions, average='weighted')
            
            results.append({
                'fold': fold + 1,
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'n_test': len(y_test)
            })
            
            print(f"  Accuracy: {accuracy:.3f}, Precision: {precision:.3f}, Recall: {recall:.3f}")
        
        # Resultado médio
        avg_results = pd.DataFrame(results).mean()
        print(f"\nResultados médios do backtesting:")
        print(f"Accuracy: {avg_results['accuracy']:.3f}")
        print(f"Precision: {avg_results['precision']:.3f}")
        print(f"Recall: {avg_results['recall']:.3f}")
        
        return results

    def save_model(self, filepath):
        """
        Salva o modelo treinado
        """
        if not self.is_trained:
            raise ValueError("Modelo não foi treinado ainda!")
        
        model_data = {
            'models': self.models,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'is_trained': self.is_trained
        }
        
        joblib.dump(model_data, filepath)
        print(f"Modelo salvo em: {filepath}")

    def load_model(self, filepath):
        """
        Carrega modelo salvo
        """
        model_data = joblib.load(filepath)
        
        self.models = model_data['models']
        self.scaler = model_data['scaler']
        self.feature_names = model_data['feature_names']
        self.is_trained = model_data['is_trained']
        
        print(f"Modelo carregado de: {filepath}")

# Exemplo de uso prático

def generate_sample_data(n_samples=10000):
    """
    Gera dados sintéticos para demonstração
    Em uso real, substituir por dados reais do IBOV
    """
    dates = pd.date_range(start='2023-01-01 10:00:00', periods=n_samples, freq='1min')

    # Simular preços com random walk
    returns = np.random.normal(0, 0.001, n_samples)
    prices = 100000 * np.cumprod(1 + returns)

    # Simular OHLC
    noise = np.random.normal(0, 0.0005, n_samples)

    df = pd.DataFrame({
        'datetime': dates,
        'open': prices * (1 + noise),
        'high': prices * (1 + np.abs(noise) + 0.0002),
        'low': prices * (1 - np.abs(noise) - 0.0002),
        'close': prices,
        'volume': np.random.randint(1000000, 10000000, n_samples)
    })

    return df

def main():
    """
    Exemplo completo de uso do sistema
    """
    print("=== IBOV Predictor - Sistema de Predição ===\n")
    print("1. Carregando dados...")
    df = generate_sample_data(10000)
    print(f"Dataset: {len(df)} amostras")

    # 2. Inicializar modelo
    predictor = IBOVPredictor()

    # 3. Preparar dados
    print("\n2. Preparando dados...")
    X, y, data_clean = predictor.prepare_data(df)

    # 4. Split temporal para teste
    split_point = int(len(X) * 0.8)
    X_train, X_test = X[:split_point], X[split_point:]
    y_train, y_test = y[:split_point], y[split_point:]
    data_test = data_clean[split_point:]

    # 5. Treinar modelo
    print("\n3. Treinando modelo...")
    predictor.train_models(X_train, y_train)

    # 6. Fazer predições
    print("\n4. Fazendo predições...")
    predictions, confidences, probabilities = predictor.predict(X_test)

    # 7. Avaliar resultados
    print("\n5. Avaliando resultados...")
    from sklearn.metrics import classification_report
    print("\nRelatório de classificação:")
    print(classification_report(y_test, predictions, 
                            target_names=['Baixa', 'Neutro', 'Alta']))

    # 8. Exemplo de decisão de trading
    print("\n6. Exemplo de decisão de trading:")
    for i in range(5):
        idx = -(i+1)
        current_data = data_test.iloc[idx:idx+1]
        
        pred = predictions[idx]
        conf = confidences[idx]
        conf_factors = predictor.calculate_confidence_factors(
            data_test.iloc[:idx+1]
        )
        
        should_trade_result, reason = predictor.should_trade(
            pred, conf, conf_factors
        )
        
        signal_names = ['VENDA', 'NEUTRO', 'COMPRA']
        print(f"  Sinal: {signal_names[pred]} | Confiança: {conf:.3f} | "
            f"Trade: {'SIM' if should_trade_result else 'NÃO'} ({reason})")

    # 9. Salvar modelo
    print("\n7. Salvando modelo...")
    predictor.save_model('ibov_predictor_model.pkl')

    print("\n=== Sistema completo executado com sucesso! ===")

if __name__ == "__main__":
    main()