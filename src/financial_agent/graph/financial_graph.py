import logging
from financial_agent.agents.market_agent import MarketAgent
from financial_agent.agents.fundamental_agent import FundamentalAgent
from financial_agent.agents.news_agent import NewsAgent
from financial_agent.agents.valuation_risk_agent import ValuationRiskAgent
from financial_agent.agents.decision_agent import DecisionAgent
from financial_agent.agents.orchestrator import OrchestratorAgent
from financial_agent.data.providers.demo_provider import (
    DemoMarketDataProvider,
    DemoFundamentalDataProvider,
    DemoNewsProvider,
)
from financial_agent.tools.market_tools import MarketTools
from financial_agent.tools.fundamental_tools import FundamentalTools
from financial_agent.tools.news_tools import NewsTools
from financial_agent.tools.valuation_risk_tools import ValuationRiskTools

logger = logging.getLogger(__name__)

def build_orchestrator() -> OrchestratorAgent:
    logger.info("Building financial agent components")
    market_provider = DemoMarketDataProvider()
    fundamental_provider = DemoFundamentalDataProvider()
    news_provider = DemoNewsProvider()

    return OrchestratorAgent(
        market_agent=MarketAgent(MarketTools(market_provider)),
        fundamental_agent=FundamentalAgent(FundamentalTools(fundamental_provider)),
        news_agent=NewsAgent(NewsTools(news_provider)),
        valuation_risk_agent=ValuationRiskAgent(ValuationRiskTools(market_provider)),
        decision_agent=DecisionAgent(),
    )

def run_financial_analysis(ticker: str) -> dict:
    logger.info("Running financial analysis ticker=%s", ticker)
    orchestrator = build_orchestrator()
    return orchestrator.run(ticker)
