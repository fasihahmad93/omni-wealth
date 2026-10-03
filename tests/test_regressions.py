from pathlib import Path
import sys
from types import SimpleNamespace

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from financial_agent.agents.decision_agent import DecisionAgent
from financial_agent.agents.news_agent import NewsAgent
from financial_agent.data.providers.demo_provider import (
    DemoFundamentalDataProvider,
    DemoMarketDataProvider,
    DemoNewsProvider,
)
from financial_agent.data.providers.yahoo_finance import YahooFinanceMarketDataProvider
from financial_agent.tools.news_tools import NewsTools
from financial_agent.tools.valuation_risk_tools import ValuationRiskTools


def test_demo_providers_supply_offline_fundamental_and_news_data():
    fundamentals = DemoFundamentalDataProvider().get_fundamentals("TEST")
    news = DemoNewsProvider().search("TEST")

    assert fundamentals["roe"] > 0
    assert fundamentals["free_cash_flow"] > 0
    assert news[0]["impact"] == "positive"


def test_mixed_market_and_unavailable_inputs_do_not_create_sell_signal():
    result = DecisionAgent().decide(
        "TEST",
        {"trend": "mixed"},
        SimpleNamespace(business_quality="not available"),
        SimpleNamespace(sentiment="not available"),
        SimpleNamespace(valuation_view="not available"),
    )

    assert result.decision == "HOLD"
    assert "0 positive and 0 negative" in result.thesis
    assert not any("below the 200-day" in risk for risk in result.risks)


def test_news_sentiment_is_unavailable_without_impact_labels():
    class UnclassifiedNewsTools:
        def search_news(self, ticker):
            return [
                {
                    "title": "A headline without sentiment metadata",
                    "date": "2026-10-03",
                    "source": "Test",
                    "impact": "not available",
                    "summary": "Sentiment was not classified.",
                }
            ]

    result = NewsAgent(UnclassifiedNewsTools()).analyze("TEST")
    assert result.sentiment == "not available"


def test_news_rss_fallback_normalizes_articles(monkeypatch):
    class FakeStock:
        info = {"longName": "Example Corporation"}

        def get_news(self, count=10):
            return []

    class FakeResponse:
        content = b"""<rss><channel><item>
            <title>Example Corporation reports results</title>
            <pubDate>Sat, 03 Oct 2026 09:00:00 GMT</pubDate>
            <source>Example News</source>
            <link>https://example.test/story</link>
            <description><![CDATA[<p>Revenue grew.</p>]]></description>
        </item></channel></rss>"""

        def raise_for_status(self):
            return None

    monkeypatch.setattr("financial_agent.tools.news_tools.yf.Ticker", lambda ticker: FakeStock())
    monkeypatch.setattr("financial_agent.tools.news_tools.requests.get", lambda *args, **kwargs: FakeResponse())

    articles = NewsTools(object()).search_news("EXAMPLE")

    assert len(articles) == 1
    assert articles[0]["source"] == "Example News"
    assert articles[0]["impact"] == "not available"
    assert articles[0]["summary"] == "Revenue grew."
    assert articles[0]["url"] == "https://example.test/story"


def test_yahoo_valuation_metrics_use_reported_fields(monkeypatch):
    class FakeStock:
        info = {
            "trailingPE": 24.5,
            "forwardPE": 20.0,
            "enterpriseToEbitda": 13.2,
            "beta": 0.9,
            "sectorTrailingPE": 27.0,
        }

    monkeypatch.setattr("financial_agent.data.providers.yahoo_finance.yf.Ticker", lambda ticker: FakeStock())
    metrics = YahooFinanceMarketDataProvider().get_valuation_metrics("TEST")

    assert metrics == {
        "pe": 24.5,
        "forward_pe": 20.0,
        "ev_ebitda": 13.2,
        "beta": 0.9,
        "sector_pe": 27.0,
    }


def test_valuation_metrics_missing_from_provider_remain_unavailable():
    class Provider(DemoMarketDataProvider):
        def get_valuation_metrics(self, ticker):
            return {
                "pe": None,
                "forward_pe": None,
                "ev_ebitda": None,
                "beta": None,
                "sector_pe": None,
            }

    result = ValuationRiskTools(Provider()).get_valuation_risk("TEST")

    assert result["pe"] is None
    assert result["ev_ebitda"] is None
    assert result["valuation_view"] == "not available"
