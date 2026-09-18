import logging

logger = logging.getLogger(__name__)

def classify_growth(revenue_growth: float, earnings_growth: float) -> str:
    logger.info("Classifying growth revenue=%s earnings=%s", revenue_growth, earnings_growth)
    if revenue_growth >= 0.15 and earnings_growth >= 0.15:
        return "strong"
    if revenue_growth >= 0 or earnings_growth >= 0:
        return "moderate"
    return "weak"

def classify_balance_sheet(debt_to_equity: float) -> str:
    logger.info("Classifying balance sheet debt_to_equity=%s", debt_to_equity)
    if debt_to_equity < 0.5:
        return "healthy"
    if debt_to_equity < 1.0:
        return "moderate"
    return "leveraged"

def classify_profitability(roe: float, roce: float) -> str:
    logger.info("Classifying profitability roe=%s roce=%s", roe, roce)
    if roe >= 0.20 and roce >= 0.20:
        return "strong"
    if roe >= 0.10 and roce >= 0.10:
        return "moderate"
    return "weak"
