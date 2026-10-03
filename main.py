import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from financial_agent.agents.market_agent import MarketAgent
from financial_agent.agents.fundamental_agent import FundamentalAgent
from financial_agent.agents.news_agent import NewsAgent
from financial_agent.agents.valuation_risk_agent import ValuationRiskAgent
from financial_agent.agents.decision_agent import DecisionAgent
from financial_agent.config.settings import setup_logging
from financial_agent.data.providers.factory import (
    create_market_data_provider,
)
from financial_agent.tools.market_tools import MarketTools
from financial_agent.tools.fundamental_tools import FundamentalTools
from financial_agent.tools.news_tools import NewsTools
from financial_agent.tools.valuation_risk_tools import ValuationRiskTools


def main():
    setup_logging()

    logger = logging.getLogger(__name__)

    ticker = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "ASIANPAINT.NS"
    )

    logger.info(
        "Starting financial agent ticker=%s",
        ticker,
    )

    provider = create_market_data_provider(
        provider_name="yahoo"
    )

    market_tools = MarketTools(provider)
    market_agent = MarketAgent(market_tools)
    fundamental_tools = FundamentalTools(provider)
    fundamental_agent = FundamentalAgent(fundamental_tools)
    news_tools = NewsTools(provider)
    news_agent = NewsAgent(news_tools)
    valuation_tools = ValuationRiskTools(provider)
    valuation_agent = ValuationRiskAgent(valuation_tools)
    decision_agent = DecisionAgent()

    market_result = market_agent.analyze(ticker)
    fundamental_result = fundamental_agent.analyze(ticker)
    news_result = news_agent.analyze(ticker)
    valuation_result = valuation_agent.analyze(ticker)
    decision_result = decision_agent.decide(
        ticker,
        market_result,
        fundamental_result,
        news_result,
        valuation_result,
    )

    print("\nMarket Analysis")
    print("=" * 50)

    for key, value in market_result.model_dump().items():
        print(f"{key}: {value}")

    print("\nFundamental Analysis")
    print("=" * 50)
    for key, value in fundamental_result.model_dump().items():
        if key == "snapshot":
            print(f"{key}:")
            for metric, metric_value in value.items():
                displayed_value = (
                    "Not available" if metric_value is None else metric_value
                )
                print(f"  {metric}: {displayed_value}")
        else:
            displayed_value = "Not available" if value is None else value
            print(f"{key}: {displayed_value}")

    print("\nNews Analysis")
    print("=" * 50)
    print(f"ticker: {news_result.ticker}")
    print(f"sentiment: {news_result.sentiment}")
    if not news_result.items:
        print("No recent news articles found.")
    else:
        for index, article in enumerate(news_result.items, start=1):
            print(f"\n{index}. {article.title}")
            print(f"   date: {article.date}")
            print(f"   source: {article.source}")
            print(f"   impact: {article.impact}")
            print(f"   summary: {article.summary}")
            if article.url:
                print(f"   url: {article.url}")

    print("\nValuation and Risk Analysis")
    print("=" * 50)
    for key, value in valuation_result.model_dump().items():
        displayed_value = "Not available" if value is None else value
        print(f"{key}: {displayed_value}")

    print("\nInvestment Decision")
    print("=" * 50)
    print(f"ticker: {decision_result.ticker}")
    print(f"decision: {decision_result.decision}")
    print(f"thesis: {decision_result.thesis}")
    print(f"time horizon: {decision_result.time_horizon}")
    print("key reasons:")
    for reason in decision_result.key_reasons:
        print(f"  - {reason}")
    print("risks:")
    for risk in decision_result.risks:
        print(f"  - {risk}")

    logger.info(
        "Financial agent completed ticker=%s decision=%s",
        ticker,
        decision_result.decision,
    )


if __name__ == "__main__":
    main()