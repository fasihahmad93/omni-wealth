import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from financial_agent.agents.market_agent import MarketAgent
from financial_agent.agents.fundamental_agent import FundamentalAgent
from financial_agent.config.settings import setup_logging
from financial_agent.data.providers.factory import (
    create_market_data_provider,
)
from financial_agent.tools.market_tools import MarketTools
from financial_agent.tools.fundamental_tools import FundamentalTools


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

    market_result = market_agent.analyze(ticker)
    fundamental_result = fundamental_agent.analyze(ticker)

    print("\nMarket Analysis")
    print("=" * 50)

    for key, value in market_result.items():
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

    logger.info(
        "Financial agent completed ticker=%s",
        ticker,
    )


if __name__ == "__main__":
    main()