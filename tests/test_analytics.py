import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import pandas as pd
from financial_agent.analytics.technical import calculate_sma, calculate_rsi, calculate_macd, calculate_volatility
from financial_agent.analytics.fundamentals import classify_growth, classify_balance_sheet, classify_profitability
from financial_agent.analytics.valuation import classify_valuation, calculate_drawdown

def test_calculate_sma():
    assert calculate_sma(pd.Series([1,2,3,4,5]), 3) == 4.0

def test_calculate_rsi():
    assert calculate_rsi(pd.Series(range(1, 30))) == 100.0

def test_calculate_macd():
    value = calculate_macd(pd.Series(range(1, 40)))
    assert value > 0

def test_calculate_volatility():
    value = calculate_volatility(pd.Series(range(1, 40)))
    assert value >= 0

def test_classify_growth():
    assert classify_growth(0.2, 0.2) == "strong"

def test_classify_balance_sheet():
    assert classify_balance_sheet(0.3) == "healthy"

def test_classify_profitability():
    assert classify_profitability(0.25, 0.25) == "strong"

def test_classify_valuation():
    assert classify_valuation(25, 22, 30) == "reasonable"

def test_calculate_drawdown():
    assert calculate_drawdown(pd.Series([100, 120, 90])) == -0.25
