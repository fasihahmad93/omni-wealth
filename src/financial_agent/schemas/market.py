from pydantic import BaseModel, Field

class MarketSnapshot(BaseModel):
    ticker: str
    current_price: float
    return_1m: float
    return_3m: float
    return_1y: float
    volume: float
    average_volume: float
    rsi: float
    macd: float
    sma_50: float
    sma_200: float
    volatility: float

class MarketAnalysis(BaseModel):
    ticker: str
    trend: str
    momentum: str
    volatility_regime: str
    snapshot: MarketSnapshot
    key_signals: list[str] = Field(default_factory=list)
