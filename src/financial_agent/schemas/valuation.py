from pydantic import BaseModel

class ValuationRiskAnalysis(BaseModel):
    ticker: str
    pe: float | None = None
    forward_pe: float | None = None
    ev_ebitda: float | None = None
    beta: float | None = None
    max_drawdown: float
    valuation_view: str
    risk_view: str
    key_risks: list[str] = []
