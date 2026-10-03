from pydantic import BaseModel, Field

class MarketSnapshot(BaseModel):
    ticker: str
    current_price: float
    return_1m: float | None = None
    return_3m: float | None = None
    return_1y: float | None = None
    volume: float | None = None
    average_volume: float | None = None
    rsi: float | None = None
    macd: float | None = None
    sma_50: float | None = None
    sma_200: float | None = None
    volatility: float | None = None

class MarketAnalysis(BaseModel):
    ticker: str
    trend: str
    momentum: str
    volatility_regime: str
    snapshot: MarketSnapshot
    key_signals: list[str] = Field(default_factory=list)
