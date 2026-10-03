import logging
from financial_agent.schemas.news import NewsAnalysis, NewsItem

logger = logging.getLogger(__name__)

class NewsAgent:
    def __init__(self, tools):
        logger.info("Initializing NewsAgent")
        self.tools = tools

    def analyze(self, ticker: str) -> NewsAnalysis:
        logger.info("NewsAgent analyzing ticker=%s", ticker)
        raw_items = self.tools.search_news(ticker)
        items = [NewsItem(**item) for item in raw_items]
        positive = sum(item.impact == "positive" for item in items)
        negative = sum(item.impact == "negative" for item in items)
        known_neutral = any(item.impact == "neutral" for item in items)
        sentiment = (
            "positive"
            if positive > negative
            else "negative"
            if negative > positive
            else "neutral"
            if known_neutral or positive + negative > 0
            else "not available"
        )
        result = NewsAnalysis(
            ticker=ticker,
            sentiment=sentiment,
            items=items,
            key_risks=[item.summary for item in items if item.impact == "negative"],
            key_catalysts=[item.summary for item in items if item.impact == "positive"],
        )
        logger.info(
            "NewsAgent output ticker=%s sentiment=%s positive_items=%s negative_items=%s",
            ticker,
            result.sentiment,
            len(result.key_catalysts),
            len(result.key_risks),
        )
        return result
