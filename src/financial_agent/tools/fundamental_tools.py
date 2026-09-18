import logging

logger = logging.getLogger(__name__)

class FundamentalTools:
    def __init__(self, provider):
        logger.info("Initializing FundamentalTools provider=%s", type(provider).__name__)
        self.provider = provider

    def get_fundamentals(self, ticker: str) -> dict:
        logger.info("Tool get_fundamentals ticker=%s", ticker)
        return self.provider.get_fundamentals(ticker)
