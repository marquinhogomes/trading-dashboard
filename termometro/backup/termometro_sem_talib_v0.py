
import pandas as pd
import numpy as np
import warnings
import MetaTrader5 as mt5
warnings.filterwarnings("ignore")

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
from datetime import datetime, timedelta
import joblib
# Para balanceamento
from imblearn.over_sampling import SMOTE

# ==== Função para coletar dados do MT5 ==== #
def get_mt5_data(symbol='WIN$N', n_bars=10000, timeframe=mt5.TIMEFRAME_M1):
    if not mt5.initialize():
        raise RuntimeError("Não foi possível inicializar o MT5")
    utc_to = datetime.now()
    utc_from = utc_to - timedelta(minutes=n_bars)
    rates = mt5.copy_rates_range(symbol, timeframe, utc_from, utc_to)
    mt5.shutdown()
    if rates is None or len(rates) == 0:
        raise RuntimeError("Nenhum dado foi retornado do MT5")
    df = pd.DataFrame(rates)
    df['datetime'] = pd.to_datetime(df['time'], unit='s')
    df.rename(columns={
        'open':'open', 'high':'high', 'low':'low', 'close':'close', 'tick_volume':'volume'
    }, inplace=True)
    df = df[['datetime', 'open', 'high', 'low', 'close', 'volume']]
    return df

# ==== Indicadores Técnicos Personalizados ==== #
class TechnicalIndicators:
    @staticmethod
    def rsi(prices, period=14):
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    @staticmethod
    def sma(prices, period):
        return prices.rolling(window=period).mean()

    @staticmethod
    def ema(prices, period):
        return prices.ewm(span=period).mean()

    @staticmethod
    def macd(prices, fast=12, slow=26, signal=9):
        ema_fast = TechnicalIndicators.ema(prices, fast)
        ema_slow = TechnicalIndicators.ema(prices, slow)
        macd_line = ema_fast - ema_slow
        signal_line = TechnicalIndicators.ema(macd_line, signal)
        histogram = macd_line - signal_line
        return macd_line, signal_line, histogram

    @staticmethod
    def bollinger_bands(prices, period=20, std_dev=2):
        sma = TechnicalIndicators.sma(prices, period)
        std = prices.rolling(window=period).std()
        upper = sma + (std * std_dev)
        lower = sma - (std * std_dev)
        return upper, sma, lower

    @staticmethod
    def stochastic(high, low, close, k_period=14, d_period=3):
        lowest_low = low.rolling(window=k_period).min()
        highest_high = high.rolling(window=k_period).max()
        k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
        d_percent = k_percent.rolling(window=d_period).mean()
        return k_percent, d_percent

    @staticmethod
    def williams_r(high, low, close, period=14):
        highest_high = high.rolling(window=period).max()
        lowest_low = low.rolling(window=period).min()
        return -100 * ((highest_high - close) / (highest_high - lowest_low))

    @staticmethod
    def atr(high, low, close, period=14):
        high_low = high - low
        high_close = np.abs(high - close.shift())
        low_close = np.abs(low - close.shift())
        true_range = np.maximum(high_low, np.maximum(high_close, low_close))
        return true_range.rolling(window=period).mean()

    @staticmethod
    def cci(high, low, close, period=14):
        typical_price = (high + low + close) / 3
        sma_tp = typical_price.rolling(window=period).mean()
        mean_deviation = typical_price.rolling(window=period).apply(lambda x: np.mean(np.abs(x - x.mean())))
        return (typical_price - sma_tp) / (0.015 * mean_deviation)

    @staticmethod
    def mfi(high, low, close, volume, period=14):
        typical_price = (high + low + close) / 3
        money_flow = typical_price * volume
        positive_flow = money_flow.where(typical_price > typical_price.shift(), 0).rolling(window=period).sum()
        negative_flow = money_flow.where(typical_price < typical_price.shift(), 0).rolling(window=period).sum()
        money_ratio = positive_flow / negative_flow
        return 100 - (100 / (1 + money_ratio))

    @staticmethod
    def obv(close, volume):
        obv = np.where(close > close.shift(), volume, 
               np.where(close < close.shift(), -volume, 0))
        return pd.Series(obv, index=close.index).cumsum()

    @staticmethod
    def ad_line(high, low, close, volume):
        clv = ((close - low) - (high - close)) / (high - low)
        clv = clv.fillna(0)
        ad = (clv * volume).cumsum()
        return ad

# ==== Classe Principal do Sistema ==== #
class IBOVPredictor:
    def __init__(self):
        self.models = {}
        self.scaler = StandardScaler()
        self.feature_names = []
        self.is_trained = False
        self.ta = TechnicalIndicators()
        
    def calculate_technical_indicators(self, df):
        """
        Calcula todos os indicadores técnicos necessários
        """
        data = df.copy()
        
        # Indicadores de Momentum
        data['rsi_2'] = self.ta.rsi(data['close'], period=2)
        data['rsi_5'] = self.ta.rsi(data['close'], period=5)
        data['rsi_14'] = self.ta.rsi(data['close'], period=14)
        
        # Stochastic
        data['stoch_k'], data['stoch_d'] = self.ta.stochastic(
            data['high'], data['low'], data['close'], k_period=5, d_period=3
        )
        
        # Williams %R
        data['williams_r'] = self.ta.williams_r(
            data['high'], data['low'], data['close'], period=14
        )
        
        # MACD
        data['macd'], data['macd_signal'], data['macd_hist'] = self.ta.macd(
            data['close'], fast=12, slow=26, signal=9
        )
        
        # Médias Móveis
        data['ema_9'] = self.ta.ema(data['close'], period=9)
        data['ema_21'] = self.ta.ema(data['close'], period=21)
        data['sma_20'] = self.ta.sma(data['close'], period=20)
        
        # TEMA (usando EMA tripla)
        ema1 = self.ta.ema(data['close'], period=21)
        ema2 = self.ta.ema(ema1, period=21)
        ema3 = self.ta.ema(ema2, period=21)
        data['tema'] = 3 * ema1 - 3 * ema2 + ema3
        
        # Bollinger Bands
        data['bb_upper'], data['bb_middle'], data['bb_lower'] = self.ta.bollinger_bands(
            data['close'], period=20, std_dev=2
        )
        
        # Volume Indicators
        data['volume_sma'] = self.ta.sma(data['volume'], period=20)
        data['ad_line'] = self.ta.ad_line(data['high'], data['low'], data['close'], data['volume'])
        data['obv'] = self.ta.obv(data['close'], data['volume'])
        
        # Money Flow Index
        data['mfi'] = self.ta.mfi(
            data['high'], data['low'], data['close'], data['volume'], period=14
        )
        
        # Average True Range (Volatilidade)
        data['atr'] = self.ta.atr(data['high'], data['low'], data['close'], period=14)
        
        # Commodity Channel Index
        data['cci'] = self.ta.cci(data['high'], data['low'], data['close'], period=14)
        
        return data

    def engineer_features(self, df):
        """
        Engenharia de features avançada (expandida)
        """
        data = df.copy()
        # Features de Preço
        data['returns_1min'] = data['close'].pct_change()
        data['returns_2min'] = data['close'].pct_change(2)
        data['returns_5min'] = data['close'].pct_change(5)
        # Novas features: médias móveis longas
        data['ema_50'] = self.ta.ema(data['close'], period=50)
        data['ema_100'] = self.ta.ema(data['close'], period=100)
        data['sma_100'] = self.ta.sma(data['close'], period=100)
        data['ema50_ema100_diff'] = (data['ema_50'] - data['ema_100']) / data['ema_100']
        data['close_ema100_diff'] = (data['close'] - data['ema_100']) / data['ema_100']
        # Volatilidade longa
        data['volatility_100'] = data['returns_1min'].rolling(100).std()
        data['atr_50'] = self.ta.atr(data['high'], data['low'], data['close'], period=50)
        data['atr_100'] = self.ta.atr(data['high'], data['low'], data['close'], period=100)
        # Candle anterior
        data['prev_close'] = data['close'].shift(1)
        data['prev_open'] = data['open'].shift(1)
        data['prev_high'] = data['high'].shift(1)
        data['prev_low'] = data['low'].shift(1)
        # Martelo invertido
        body = abs(data['close'] - data['open'])
        upper_shadow = data['high'] - np.maximum(data['close'], data['open'])
        lower_shadow = np.minimum(data['close'], data['open']) - data['low']
        data['inverted_hammer'] = ((body <= (data['high'] - data['low']) * 0.3) & (upper_shadow >= body * 2) & (lower_shadow <= body * 0.5)).astype(int)
        # ...existing code for other features...
        data['high_low_ratio'] = (data['high'] - data['low']) / data['close']
        data['close_open_ratio'] = (data['close'] - data['open']) / data['open']
        data['rsi_2_norm'] = (data['rsi_2'] - 50) / 50
        data['rsi_5_norm'] = (data['rsi_5'] - 50) / 50
        data['stoch_norm'] = (data['stoch_k'] - 50) / 50
        data['williams_norm'] = (data['williams_r'] + 50) / 50
        data['price_ema9_diff'] = (data['close'] - data['ema_9']) / data['ema_9']
        data['ema9_ema21_diff'] = (data['ema_9'] - data['ema_21']) / data['ema_21']
        data['bb_position'] = (data['close'] - data['bb_lower']) / (data['bb_upper'] - data['bb_lower'])
        data['bb_width'] = (data['bb_upper'] - data['bb_lower']) / data['bb_middle']
        data['volume_ratio'] = data['volume'] / data['volume_sma']
        data['volume_spike'] = (data['volume'] > data['volume_sma'] * 2).astype(int)
        data['vwap'] = (data['close'] * data['volume']).cumsum() / data['volume'].cumsum()
        data['vwap_distance'] = (data['close'] - data['vwap']) / data['vwap']
        data['volatility_20'] = data['returns_1min'].rolling(20).std()
        data['atr_normalized'] = data['atr'] / data['close']
        vol_quantiles = data['volatility_20'].quantile([0.33, 0.66])
        data['volatility_regime'] = pd.cut(
            data['volatility_20'], 
            bins=[-np.inf, vol_quantiles.iloc[0], vol_quantiles.iloc[1], np.inf],
            labels=[0, 1, 2]  # 0=Baixa, 1=Média, 2=Alta
        ).astype(float)
        # Doji: corpo pequeno
        data['doji'] = (body <= (data['high'] - data['low']) * 0.1).astype(int)
        # Hammer: corpo pequeno no topo, sombra inferior longa
        data['hammer'] = ((body <= (data['high'] - data['low']) * 0.3) & (lower_shadow >= body * 2) & (upper_shadow <= body * 0.5)).astype(int)
        # Engulfing simplificado: candle atual engloba o anterior
        prev_body = abs(data['close'].shift(1) - data['open'].shift(1))
        data['engulfing'] = (body > prev_body * 1.5).astype(int)
        if 'datetime' in data.columns:
            data['hour'] = pd.to_datetime(data['datetime']).dt.hour
            data['minute'] = pd.to_datetime(data['datetime']).dt.minute
            data['session_factor'] = self._get_session_factor(data['hour'], data['minute'])
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

    def create_target(self, df, threshold=0.0003):
        """
        Cria variável target para classificação
        threshold: 0.0003 = 0.03% de movimento mínimo (mais exemplos nas classes extremas)
        """
        data = df.copy()
        data['future_return'] = data['close'].shift(-1) / data['close'] - 1
        conditions = [
            data['future_return'] < -threshold,
            (data['future_return'] >= -threshold) & (data['future_return'] <= threshold),
            data['future_return'] > threshold
        ]
        data['target'] = np.select(conditions, [0, 1, 2])
        return data

    def select_features(self, df):
        """
        Seleciona features relevantes para o modelo (expandido)
        """
        feature_columns = [
            # Momentum
            'rsi_2_norm', 'rsi_5_norm', 'stoch_norm', 'williams_norm',
            'macd', 'macd_signal', 'macd_hist', 'cci',
            # Médias Móveis
            'price_ema9_diff', 'ema9_ema21_diff',
            'ema_50', 'ema_100', 'sma_100', 'ema50_ema100_diff', 'close_ema100_diff',
            # Bollinger
            'bb_position', 'bb_width',
            # Volume
            'volume_ratio', 'volume_spike', 'vwap_distance', 'mfi',
            # Volatilidade
            'atr_normalized', 'volatility_regime', 'volatility_100', 'atr_50', 'atr_100',
            # Padrões
            'doji', 'hammer', 'engulfing', 'inverted_hammer',
            # Features de Preço
            'high_low_ratio', 'close_open_ratio',
            'returns_1min', 'returns_2min', 'returns_5min',
            # Candle anterior
            'prev_close', 'prev_open', 'prev_high', 'prev_low',
            # Features Lag
            'returns_lag_1', 'returns_lag_2', 'returns_lag_3', 'returns_lag_5',
            'volume_ratio_lag_1', 'volume_ratio_lag_2', 'volume_ratio_lag_3',
            'rsi_2_lag_1', 'rsi_2_lag_2', 'rsi_2_lag_3'
        ]
        if 'session_factor' in df.columns:
            feature_columns.append('session_factor')
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
        Treina ensemble de modelos com busca de hiperparâmetros e balanceamento
        """
        print("Treinando modelos...")
        # Balanceamento com SMOTE
        print("Aplicando SMOTE para balancear as classes...")
        smote = SMOTE(random_state=42)
        X_res, y_res = smote.fit_resample(X, y)
        print(f"Após SMOTE: {dict(pd.Series(y_res).value_counts())}")
        # Normalizar features
        X_scaled = self.scaler.fit_transform(X_res)
        from sklearn.utils.class_weight import compute_sample_weight
        from sklearn.model_selection import GridSearchCV, StratifiedKFold
        # Random Forest com GridSearchCV
        rf = RandomForestClassifier(class_weight='balanced', n_jobs=-1, random_state=42)
        rf_params = {
            'n_estimators': [100, 200],
            'max_depth': [8, 12],
            'min_samples_split': [5, 10],
            'min_samples_leaf': [2, 5]
        }
        rf_cv = GridSearchCV(rf, rf_params, cv=StratifiedKFold(n_splits=3, shuffle=True, random_state=42), scoring='f1_weighted', n_jobs=-1)
        print("Buscando melhores hiperparâmetros para RandomForest...")
        rf_cv.fit(X_scaled, y_res)
        self.models['rf'] = rf_cv.best_estimator_
        # XGBoost com GridSearchCV
        from collections import Counter
        class_counts = Counter(y_res)
        total = sum(class_counts.values())
        weights = {cls: total/count for cls, count in class_counts.items()}
        scale_pos_weight = weights.get(2, 1) / weights.get(0, 1) if weights.get(0, 1) > 0 else 1
        xgb_model = xgb.XGBClassifier(random_state=42, scale_pos_weight=scale_pos_weight, use_label_encoder=False, eval_metric='mlogloss')
        xgb_params = {
            'n_estimators': [100, 200],
            'max_depth': [4, 6],
            'learning_rate': [0.05, 0.1],
            'subsample': [0.8, 1.0],
            'colsample_bytree': [0.8, 1.0]
        }
        xgb_cv = GridSearchCV(xgb_model, xgb_params, cv=StratifiedKFold(n_splits=3, shuffle=True, random_state=42), scoring='f1_weighted', n_jobs=-1)
        print("Buscando melhores hiperparâmetros para XGBoost...")
        xgb_cv.fit(X_res, y_res)
        self.models['xgb'] = xgb_cv.best_estimator_
        # Gradient Boosting com GridSearchCV
        gb = GradientBoostingClassifier(random_state=42)
        gb_params = {
            'n_estimators': [100, 200],
            'max_depth': [6, 8],
            'learning_rate': [0.05, 0.1],
            'subsample': [0.8, 1.0]
        }
        gb_cv = GridSearchCV(gb, gb_params, cv=StratifiedKFold(n_splits=3, shuffle=True, random_state=42), scoring='f1_weighted', n_jobs=-1)
        print("Buscando melhores hiperparâmetros para GradientBoosting...")
        sample_weight = compute_sample_weight(class_weight='balanced', y=y_res)
        gb_cv.fit(X_res, y_res, sample_weight=sample_weight)
        self.models['gb'] = gb_cv.best_estimator_
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
        
        if len(df_current) == 0:
            return {'volatility': 0.5, 'volume': 0.5, 'trend_alignment': 0.5, 'momentum': 0.5}
        
        # Fator de volatilidade
        if 'volatility_20' in df_current.columns and not df_current['volatility_20'].isna().all():
            current_vol = df_current['volatility_20'].dropna().iloc[-1] if len(df_current['volatility_20'].dropna()) > 0 else 0.01
            vol_regime = df_current['volatility_regime'].dropna().iloc[-1] if len(df_current['volatility_regime'].dropna()) > 0 else 1
            factors['volatility'] = 0.8 if vol_regime == 1 else 0.6  # Prefere vol média
        else:
            factors['volatility'] = 0.7
        
        # Fator de volume
        if 'volume_ratio' in df_current.columns and not df_current['volume_ratio'].isna().all():
            vol_ratio = df_current['volume_ratio'].dropna().iloc[-1] if len(df_current['volume_ratio'].dropna()) > 0 else 1.0
            factors['volume'] = min(1.0, vol_ratio / 2.0)  # Volume alto = mais confiança
        else:
            factors['volume'] = 0.7
        
        # Fator de tendência (alinhamento de timeframes)
        if 'price_ema9_diff' in df_current.columns and 'ema9_ema21_diff' in df_current.columns:
            short_trend = df_current['price_ema9_diff'].dropna().iloc[-1] if len(df_current['price_ema9_diff'].dropna()) > 0 else 0
            medium_trend = df_current['ema9_ema21_diff'].dropna().iloc[-1] if len(df_current['ema9_ema21_diff'].dropna()) > 0 else 0
            factors['trend_alignment'] = 1.0 if short_trend * medium_trend > 0 else 0.7
        else:
            factors['trend_alignment'] = 0.7
        
        # Fator de momentum
        if 'rsi_2' in df_current.columns and not df_current['rsi_2'].isna().all():
            rsi_2 = df_current['rsi_2'].dropna().iloc[-1] if len(df_current['rsi_2'].dropna()) > 0 else 50
            factors['momentum'] = 1.0 if 30 < rsi_2 < 70 else 0.8  # Evita extremos
        else:
            factors['momentum'] = 0.8
        
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
        Realiza backtesting com validação cruzada estratificada
        """
        print("Iniciando backtesting...")
        from sklearn.model_selection import StratifiedKFold
        skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
        results = []
        for fold, (train_idx, test_idx) in enumerate(skf.split(X, y)):
            print(f"Fold {fold + 1}/{n_splits}")
            X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
            y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
            temp_predictor = IBOVPredictor()
            temp_predictor.feature_names = self.feature_names
            temp_predictor.train_models(X_train, y_train)
            predictions, confidences, _ = temp_predictor.predict(X_test)
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
    print("=== IBOV Predictor - Sistema de Predição (SEM TA-LIB) ===\n")
    print("1. Carregando dados...")
    df = get_mt5_data(symbol='WIN$N', n_bars=10000)
    print(f"Dataset real do MT5: {len(df)} amostras")

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
    predictor.save_model('ibov_predictor_model_sem_talib.pkl')

    print("\n=== Sistema completo executado com sucesso! ===")

if __name__ == "__main__":
    main()
