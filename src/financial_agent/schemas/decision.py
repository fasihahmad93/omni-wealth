from typing import Literal
from pydantic import BaseModel

class InvestmentDecision(BaseModel):
    ticker: str
    decision: Literal["BUY", "HOLD", "SELL"]
    thesis: str
    key_reasons: list[str] = []
    risks: list[str] = []
    time_horizon: str = "1-3 years"
