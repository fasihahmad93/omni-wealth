import logging
import pandas as pd

logger = logging.getLogger(__name__)

def calculate_sma(prices: pd.Series, window: int) -> float:
    logger.info("Calculating SMA window=%s rows=%s", window, len(prices))
    if window <= 0:
        raise ValueError("window must be positive")
    return float(prices.rolling(window).mean().iloc[-1])

def calculate_rsi(prices: pd.Series, period: int = 14) -> float:
    logger.info("Calculating RSI period=%s rows=%s", period, len(prices))
    if period <= 0:
        raise ValueError("period must be positive")
    delta = prices.diff()
    gains = delta.clip(lower=0)
    losses = -delta.clip(upper=0)
    avg_gain = gains.rolling(period).mean().iloc[-1]
    avg_loss = losses.rolling(period).mean().iloc[-1]
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return float(100 - (100 / (1 + rs)))

def calculate_macd(prices: pd.Series) -> float:
    logger.info("Calculating MACD rows=%s", len(prices))
    ema12 = prices.ewm(span=12, adjust=False).mean()
    ema26 = prices.ewm(span=26, adjust=False).mean()
    return float((ema12 - ema26).iloc[-1])

def calculate_volatility(prices: pd.Series, window: int = 20) -> float:
    logger.info("Calculating volatility window=%s rows=%s", window, len(prices))
    return float(prices.pct_change().rolling(window).std().iloc[-1])
