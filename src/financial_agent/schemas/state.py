from typing import TypedDict, Any

class FinancialAgentState(TypedDict, total=False):
    ticker: str
    market_analysis: Any
    fundamental_analysis: Any
    news_analysis: Any
    valuation_analysis: Any
    decision: Any
    errors: list[str]
