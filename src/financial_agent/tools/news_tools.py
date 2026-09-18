import logging

logger = logging.getLogger(__name__)

class NewsTools:
    def __init__(self, provider):
        logger.info("Initializing NewsTools provider=%s", type(provider).__name__)
        self.provider = provider

    def search_news(self, ticker: str) -> list[dict]:
        logger.info("Tool search_news ticker=%s", ticker)
        return self.provider.search(ticker)
