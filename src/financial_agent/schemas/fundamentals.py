from pydantic import BaseModel

class FundamentalSnapshot(BaseModel):
    ticker: str
    revenue_growth: float
    earnings_growth: float
    roe: float
    roce: float
    debt_to_equity: float
    operating_cash_flow: float
    free_cash_flow: float
    net_margin: float

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
