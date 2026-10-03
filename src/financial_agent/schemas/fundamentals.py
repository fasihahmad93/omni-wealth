from pydantic import BaseModel

class FundamentalSnapshot(BaseModel):
    ticker: str
    revenue_growth: float | None = None
    earnings_growth: float | None = None
    roe: float | None = None
    roce: float | None = None
    debt_to_equity: float | None = None
    operating_cash_flow: float | None = None
    free_cash_flow: float | None = None
    net_margin: float | None = None

class FundamentalAnalysis(BaseModel):
    ticker: str
    business_quality: str
    growth: str
    profitability: str
    balance_sheet: str
    cash_flow: str
    snapshot: FundamentalSnapshot
    strengths: list[str] = []
    risks: list[str] = []
