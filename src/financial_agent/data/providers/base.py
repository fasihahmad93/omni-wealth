import logging
from abc import ABC, abstractmethod

import pandas as pd

logger = logging.getLogger(__name__)


class MarketDataProvider(ABC):

    def __init__(self):
        logger.info(
            "Initializing market data provider=%s",
            self.__class__.__name__,
        )

    @abstractmethod
    def get_history(self, ticker: str) -> pd.DataFrame:
        logger.info(
            "Requesting historical market data ticker=%s",
            ticker,
        )
        raise NotImplementedError

    @abstractmethod
    def get_price(self, ticker: str) -> float:
        logger.info(
            "Requesting current market price ticker=%s",
            ticker,
        )
        raise NotImplementedError