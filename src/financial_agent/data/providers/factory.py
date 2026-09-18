import logging

from .base import MarketDataProvider
from .demo_provider import DemoMarketDataProvider
from .yahoo_finance import YahooFinanceMarketDataProvider

logger = logging.getLogger(__name__)


def create_market_data_provider(
    provider_name: str = "yahoo",
) -> MarketDataProvider:

    logger.info(
        "Creating market data provider provider=%s",
        provider_name,
    )

    provider_name = provider_name.lower()

    if provider_name == "yahoo":
        return YahooFinanceMarketDataProvider()

    if provider_name == "demo":
        return DemoMarketDataProvider()

    raise ValueError(
        f"Unsupported market data provider: {provider_name}"
    )