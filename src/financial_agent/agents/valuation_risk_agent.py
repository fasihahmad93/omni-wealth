import logging
from financial_agent.schemas.valuation import ValuationRiskAnalysis

logger = logging.getLogger(__name__)

class ValuationRiskAgent:
    def __init__(self, tools):
        logger.info("Initializing ValuationRiskAgent")
        self.tools = tools

    def analyze(self, ticker: str) -> ValuationRiskAnalysis:
        logger.info("ValuationRiskAgent analyzing ticker=%s", ticker)
        raw = self.tools.get_valuation_risk(ticker)
        risk_view = "high" if raw["max_drawdown"] < -0.30 else "moderate"
        result = ValuationRiskAnalysis(
            ticker=ticker,
            pe=raw["pe"],
            forward_pe=raw["forward_pe"],
            ev_ebitda=raw["ev_ebitda"],
            beta=raw["beta"],
            max_drawdown=raw["max_drawdown"],
            valuation_view=raw["valuation_view"],
            risk_view=risk_view,
            key_risks=["Historical drawdown is not a forecast of future losses"],
        )
        logger.info(
            "ValuationRiskAgent output ticker=%s valuation_view=%s risk_view=%s pe=%s max_drawdown=%s",
            ticker,
            result.valuation_view,
            result.risk_view,
            result.pe,
            result.max_drawdown,
        )
        return result
