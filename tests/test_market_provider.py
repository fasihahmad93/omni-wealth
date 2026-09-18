import pandas as pd
import pytest

from src.financial_agent.data.providers.demo_provider import (
    DemoMarketDataProvider,
)


def test_demo_provider_returns_history():
    provider = DemoMarketDataProvider(periods=100)

    result = provider.get_history("ASIANPAINT.NS")

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 100
    assert "close" in result.columns
    assert "volume" in result.columns


def test_demo_provider_returns_price():
    provider = DemoMarketDataProvider(periods=100)

    price = provider.get_price("ASIANPAINT.NS")

    assert isinstance(price, float)
    assert price > 0


def test_demo_provider_rejects_invalid_periods():
    with pytest.raises(ValueError):
        DemoMarketDataProvider(periods=0)