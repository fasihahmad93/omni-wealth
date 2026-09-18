import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from financial_agent.data.providers.demo_provider import DemoMarketDataProvider, DemoFundamentalDataProvider, DemoNewsProvider
from financial_agent.tools.market_tools import MarketTools
from financial_agent.tools.fundamental_tools import FundamentalTools
from financial_agent.tools.news_tools import NewsTools
from financial_agent.tools.valuation_risk_tools import ValuationRiskTools
from financial_agent.agents.market_agent import MarketAgent
from financial_agent.agents.fundamental_agent import FundamentalAgent
from financial_agent.agents.news_agent import NewsAgent
from financial_agent.agents.valuation_risk_agent import ValuationRiskAgent
from financial_agent.agents.decision_agent import DecisionAgent
from financial_agent.agents.orchestrator import OrchestratorAgent

def components():
    market_provider = DemoMarketDataProvider()
    return (
        MarketAgent(MarketTools(market_provider)),
        FundamentalAgent(FundamentalTools(DemoFundamentalDataProvider())),
        NewsAgent(NewsTools(DemoNewsProvider())),
        ValuationRiskAgent(ValuationRiskTools(market_provider)),
        DecisionAgent(),
    )

def test_market_agent():
    result = components()[0].analyze("TEST")
    assert result.ticker == "TEST"

def test_fundamental_agent():
    result = components()[1].analyze("TEST")
    assert result.snapshot.roe > 0

def test_news_agent():
    result = components()[2].analyze("TEST")
    assert result.sentiment == "positive"

def test_valuation_risk_agent():
    result = components()[3].analyze("TEST")
    assert result.pe > 0

def test_decision_agent():
    market, fundamental, news, valuation, decision = components()
    result = decision.decide(
        "TEST",
        market.analyze("TEST"),
        fundamental.analyze("TEST"),
        news.analyze("TEST"),
        valuation.analyze("TEST"),
    )
    assert result.decision in {"BUY", "HOLD", "SELL"}

def test_orchestrator():
    market, fundamental, news, valuation, decision = components()
    orchestrator = OrchestratorAgent(market, fundamental, news, valuation, decision)
    result = orchestrator.run("TEST")
    assert result["decision"].decision in {"BUY", "HOLD", "SELL"}
