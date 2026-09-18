from pydantic import BaseModel

class ValuationRiskAnalysis(BaseModel):
    ticker: str
    pe: float
    forward_pe: float
    ev_ebitda: float
    beta: float
    max_drawdown: float
    valuation_view: str
    risk_view: str
    key_risks: list[str] = []
