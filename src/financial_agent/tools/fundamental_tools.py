import logging

import yfinance as yf

logger = logging.getLogger(__name__)

class FundamentalTools:
    def __init__(self, provider):
        logger.info("Initializing FundamentalTools provider=%s", type(provider).__name__)
        self.provider = provider

    def get_fundamentals(self, ticker: str) -> dict[str, float | None]:
        logger.info("Tool get_fundamentals ticker=%s", ticker)

        if not ticker or not ticker.strip():
            raise ValueError("ticker cannot be empty")

        ticker = ticker.strip().upper()
        provider_method = getattr(self.provider, "get_fundamentals", None)
        if callable(provider_method):
            return provider_method(ticker)

        try:
            stock = yf.Ticker(ticker)
            info = stock.info or {}
            if not info:
                raise ValueError(f"No fundamental data returned for ticker={ticker}")

            def latest_statement_value(statement, labels: tuple[str, ...]):
                if statement is None or statement.empty:
                    return None
                rows = {str(label).casefold(): label for label in statement.index}
                for label in labels:
                    row = rows.get(label.casefold())
                    if row is not None:
                        values = statement.loc[row].dropna()
                        if not values.empty:
                            return float(values.iloc[0])
                return None

            roce = info.get("returnOnCapitalEmployed")
            if roce is None:
                ebit = latest_statement_value(
                    stock.financials,
                    ("EBIT", "Operating Income"),
                )
                total_assets = latest_statement_value(
                    stock.balance_sheet,
                    ("Total Assets",),
                )
                current_liabilities = latest_statement_value(
                    stock.balance_sheet,
                    ("Current Liabilities", "Total Current Liabilities"),
                )
                capital_employed = (
                    total_assets - current_liabilities
                    if total_assets is not None and current_liabilities is not None
                    else None
                )
                roce = (
                    ebit / capital_employed
                    if ebit is not None and capital_employed
                    else None
                )

            def metric(name: str) -> float | None:
                value = info.get(name)
                if value is None:
                    logger.warning(
                        "Fundamental metric unavailable ticker=%s metric=%s",
                        ticker,
                        name,
                    )
                    return None
                return float(value)

            debt_to_equity_value = metric("debtToEquity")
            debt_to_equity = (
                debt_to_equity_value / 100
                if debt_to_equity_value is not None
                else None
            )
            fundamentals = {
                "revenue_growth": metric("revenueGrowth"),
                "earnings_growth": metric("earningsGrowth"),
                "roe": metric("returnOnEquity"),
                "roce": float(roce) if roce is not None else None,
                "debt_to_equity": debt_to_equity,
                "operating_cash_flow": metric("operatingCashflow"),
                "free_cash_flow": metric("freeCashflow"),
                "net_margin": metric("profitMargins"),
            }
            logger.info("Fetched stock fundamentals ticker=%s", ticker)
            return fundamentals
        except Exception as exc:
            logger.exception("Failed to fetch fundamentals ticker=%s", ticker)
            raise RuntimeError(f"Unable to fetch fundamentals for {ticker}") from exc
