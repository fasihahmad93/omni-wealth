import logging
import sys

from src.financial_agent.agents.market_agent import MarketAgent
from src.financial_agent.config.settings import setup_logging
from src.financial_agent.data.providers.factory import (
    create_market_data_provider,
)
from src.financial_agent.tools.market_tools import MarketTools


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

    result = market_agent.analyze(ticker)

    print("\nMarket Analysis")
    print("=" * 50)

    for key, value in result.items():
        print(f"{key}: {value}")

    logger.info(
        "Financial agent completed ticker=%s",
        ticker,
    )


if __name__ == "__main__":
    main()