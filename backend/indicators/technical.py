"""
Pure-NumPy / Pandas technical indicator library.
All functions accept a pandas DataFrame with columns:
    timestamp, open, high, low, close, volume
and return a Series or scalar.
"""
import numpy as np
import pandas as pd
from typing import Optional


# ── Helpers ───────────────────────────────────────────────────────────────────

def ohlcv_to_df(raw: list) -> pd.DataFrame:
    """Convert CCXT OHLCV list to a DataFrame."""
    df = pd.DataFrame(raw, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df = df.set_index("timestamp").sort_index()
    df = df.astype(float)
    return df


# ── Moving Averages ───────────────────────────────────────────────────────────

def ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(span=period, adjust=False).mean()


def sma(series: pd.Series, period: int) -> pd.Series:
    return series.rolling(period).mean()


def wma(series: pd.Series, period: int) -> pd.Series:
    weights = np.arange(1, period + 1)
    return series.rolling(period).apply(
        lambda x: np.dot(x, weights) / weights.sum(), raw=True
    )


# ── Oscillators ───────────────────────────────────────────────────────────────

def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain  = delta.clip(lower=0)
    loss  = (-delta).clip(lower=0)
    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def macd(series: pd.Series,
         fast: int = 12, slow: int = 26, signal: int = 9
         ) -> tuple[pd.Series, pd.Series, pd.Series]:
    """Returns (macd_line, signal_line, histogram)."""
    fast_ema   = ema(series, fast)
    slow_ema   = ema(series, slow)
    macd_line  = fast_ema - slow_ema
    signal_line = ema(macd_line, signal)
    histogram   = macd_line - signal_line
    return macd_line, signal_line, histogram


def stochastic(df: pd.DataFrame, k_period: int = 14,
               d_period: int = 3) -> tuple[pd.Series, pd.Series]:
    """Returns (%K, %D)."""
    low_min  = df["low"].rolling(k_period).min()
    high_max = df["high"].rolling(k_period).max()
    k = 100 * (df["close"] - low_min) / (high_max - low_min).replace(0, np.nan)
    d = k.rolling(d_period).mean()
    return k, d


# ── Volatility ────────────────────────────────────────────────────────────────

def bollinger_bands(series: pd.Series, period: int = 20,
                    std_dev: float = 2.0
                    ) -> tuple[pd.Series, pd.Series, pd.Series]:
    """Returns (upper, middle, lower)."""
    middle = sma(series, period)
    std    = series.rolling(period).std()
    upper  = middle + std_dev * std
    lower  = middle - std_dev * std
    return upper, middle, lower


def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    high = df["high"]
    low  = df["low"]
    prev_close = df["close"].shift(1)
    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low  - prev_close).abs(),
    ], axis=1).max(axis=1)
    return tr.ewm(span=period, adjust=False).mean()


def volatility_pct(series: pd.Series, period: int = 20) -> float:
    """Rolling std-dev as a % of the last close price."""
    last = series.iloc[-1]
    if last == 0:
        return 0.0
    return float(series.rolling(period).std().iloc[-1] / last * 100)


# ── Volume ────────────────────────────────────────────────────────────────────

def obv(df: pd.DataFrame) -> pd.Series:
    direction = df["close"].diff().apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))
    return (direction * df["volume"]).cumsum()


def vwap(df: pd.DataFrame) -> pd.Series:
    tp   = (df["high"] + df["low"] + df["close"]) / 3
    cvol = df["volume"].cumsum()
    return (tp * df["volume"]).cumsum() / cvol.replace(0, np.nan)


# ── Trend / Structure ─────────────────────────────────────────────────────────

def adx(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Average Directional Index (ADX).  Returns values in [0, 100]."""
    high  = df["high"]
    low   = df["low"]
    close = df["close"]

    # True Range
    prev_close = close.shift(1)
    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low  - prev_close).abs(),
    ], axis=1).max(axis=1)

    # Directional movement
    dm_plus  = high.diff().clip(lower=0)
    dm_minus = (-low.diff()).clip(lower=0)
    # Only keep the dominant direction
    dm_plus  = dm_plus.where(dm_plus > dm_minus, 0.0)
    dm_minus = dm_minus.where(dm_minus > dm_plus, 0.0)

    # Smoothed averages
    atr_s   = tr.ewm(span=period, adjust=False).mean()
    di_plus  = 100 * dm_plus.ewm(span=period, adjust=False).mean()  / atr_s.replace(0, np.nan)
    di_minus = 100 * dm_minus.ewm(span=period, adjust=False).mean() / atr_s.replace(0, np.nan)

    dx = 100 * (di_plus - di_minus).abs() / (di_plus + di_minus).replace(0, np.nan)
    return dx.ewm(span=period, adjust=False).mean().fillna(0)


def supertrend(df: pd.DataFrame, period: int = 10,
               multiplier: float = 3.0) -> pd.Series:
    """Simple Supertrend indicator; returns 1 (uptrend) or -1 (downtrend)."""
    _atr  = atr(df, period)
    upper = (df["high"] + df["low"]) / 2 + multiplier * _atr
    lower = (df["high"] + df["low"]) / 2 - multiplier * _atr
    st    = pd.Series(np.nan, index=df.index)
    trend = pd.Series(1, index=df.index)

    for i in range(1, len(df)):
        prev_upper = upper.iloc[i - 1]
        prev_lower = lower.iloc[i - 1]
        close      = df["close"].iloc[i]

        if close > prev_upper:
            trend.iloc[i] =  1
        elif close < prev_lower:
            trend.iloc[i] = -1
        else:
            trend.iloc[i] = trend.iloc[i - 1]
    return trend


# ── Composite signal scoring ──────────────────────────────────────────────────

def compute_signal_score(df: pd.DataFrame) -> dict:
    """
    Returns a dict with individual indicator signals (-1 / 0 / 1) and a
    weighted composite confidence score in [0, 1].

    score > 0.60  → BUY candidate
    score < 0.40  → SELL candidate
    otherwise     → NEUTRAL
    """
    close = df["close"]

    scores = {}

    # EMA crossover (fast 9 / slow 21)
    fast_ema_val = ema(close, 9).iloc[-1]
    slow_ema_val = ema(close, 21).iloc[-1]
    scores["ema_cross"] = 1 if fast_ema_val > slow_ema_val else -1

    # RSI
    rsi_val = rsi(close).iloc[-1]
    if rsi_val < 35:
        scores["rsi"] = 1
    elif rsi_val > 65:
        scores["rsi"] = -1
    else:
        scores["rsi"] = 0

    # MACD
    macd_line, signal_line, hist = macd(close)
    scores["macd"] = 1 if hist.iloc[-1] > 0 and hist.iloc[-2] <= 0 else (
                    -1 if hist.iloc[-1] < 0 and hist.iloc[-2] >= 0 else 0)

    # Bollinger Band squeeze
    upper, mid, lower = bollinger_bands(close)
    last_close = close.iloc[-1]
    if last_close < lower.iloc[-1]:
        scores["bb"] = 1
    elif last_close > upper.iloc[-1]:
        scores["bb"] = -1
    else:
        scores["bb"] = 0

    # OBV trend
    obv_s = obv(df)
    obv_ema = ema(obv_s, 10)
    scores["obv"] = 1 if obv_s.iloc[-1] > obv_ema.iloc[-1] else -1

    # Supertrend
    scores["supertrend"] = int(supertrend(df).iloc[-1])

    # Weighted composite (equal weights for simplicity; tune as needed)
    weights = {"ema_cross": 0.25, "rsi": 0.20, "macd": 0.20,
               "bb": 0.15, "obv": 0.10, "supertrend": 0.10}

    raw = sum(weights[k] * scores[k] for k in weights)   # range [-1, 1]
    confidence = (raw + 1) / 2                            # normalise to [0, 1]

    return {
        "signals":    scores,
        "confidence": round(float(confidence), 4),
        "rsi":        round(float(rsi_val), 2),
        "atr":        round(float(atr(df).iloc[-1]), 6),
        "volatility": round(volatility_pct(close), 4),
    }
