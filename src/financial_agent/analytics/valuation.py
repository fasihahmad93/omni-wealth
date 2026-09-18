import logging

logger = logging.getLogger(__name__)

def classify_valuation(pe: float, forward_pe: float, sector_pe: float = 30.0) -> str:
    logger.info("Classifying valuation pe=%s forward_pe=%s sector_pe=%s", pe, forward_pe, sector_pe)
    if pe <= sector_pe and forward_pe <= pe:
        return "reasonable"
    if pe <= sector_pe * 1.25:
        return "elevated"
    return "expensive"

def calculate_drawdown(prices) -> float:
    logger.info("Calculating maximum drawdown rows=%s", len(prices))
    running_max = prices.cummax()
    drawdowns = prices / running_max - 1
    return float(drawdowns.min())
