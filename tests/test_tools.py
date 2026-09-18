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

def test_market_get_price():
    assert MarketTools(DemoMarketDataProvider()).get_price("TEST") > 0

def test_market_snapshot():
    result = MarketTools(DemoMarketDataProvider()).get_market_snapshot("TEST")
    assert result["ticker"] == "TEST"
    assert "rsi" in result

def test_fundamental_tool():
    result = FundamentalTools(DemoFundamentalDataProvider()).get_fundamentals("TEST")
    assert result["roe"] > 0

def test_news_tool():
    result = NewsTools(DemoNewsProvider()).search_news("TEST")
    assert len(result) == 1

def test_valuation_risk_tool():
    result = ValuationRiskTools(DemoMarketDataProvider()).get_valuation_risk("TEST")
    assert result["pe"] > 0
