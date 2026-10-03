import logging
import re
from datetime import datetime, timezone
from html import unescape
from urllib.parse import quote_plus
from xml.etree import ElementTree

import requests
import yfinance as yf

logger = logging.getLogger(__name__)

class NewsTools:
    def __init__(self, provider):
        logger.info("Initializing NewsTools provider=%s", type(provider).__name__)
        self.provider = provider

    def search_news(self, ticker: str) -> list[dict]:
        logger.info("Tool search_news ticker=%s", ticker)

        if not ticker or not ticker.strip():
            raise ValueError("ticker cannot be empty")

        ticker = ticker.strip().upper()
        provider_search = getattr(self.provider, "search", None)

        try:
            if callable(provider_search):
                articles = provider_search(ticker)
            else:
                stock = yf.Ticker(ticker)
                get_news = getattr(stock, "get_news", None)
                try:
                    articles = get_news(count=10) if callable(get_news) else stock.news
                except Exception as yahoo_error:
                    logger.warning(
                        "Yahoo news unavailable ticker=%s error=%s; trying RSS search",
                        ticker,
                        yahoo_error,
                    )
                    articles = []

                if not articles:
                    try:
                        company_name = (
                            stock.info.get("longName")
                            or stock.info.get("shortName")
                            or ticker
                        )
                    except Exception:
                        company_name = ticker

                    query = quote_plus(f'"{company_name}" when:1y')
                    locale = "IN" if ticker.endswith((".NS", ".BO")) else "US"
                    rss_url = (
                        "https://news.google.com/rss/search"
                        f"?q={query}&hl=en-{locale}&gl={locale}&ceid={locale}:en"
                    )
                    response = requests.get(rss_url, timeout=10)
                    response.raise_for_status()
                    rss_root = ElementTree.fromstring(response.content)
                    articles = [
                        {
                            "title": item.findtext("title"),
                            "pubDate": item.findtext("pubDate"),
                            "source": item.findtext("source") or "Google News",
                            "link": item.findtext("link"),
                            "description": unescape(item.findtext("description") or ""),
                        }
                        for item in rss_root.findall("./channel/item")[:10]
                    ]

            normalized_articles = []
            for article in articles or []:
                if not isinstance(article, dict):
                    continue

                content = article.get("content")
                if not isinstance(content, dict):
                    content = article

                title = content.get("title") or article.get("title")
                if not title:
                    continue

                provider = content.get("provider") or article.get("provider")
                if isinstance(provider, dict):
                    source = provider.get("displayName") or provider.get("name")
                else:
                    source = provider
                source = (
                    source
                    or content.get("publisher")
                    or article.get("publisher")
                    or content.get("source")
                    or article.get("source")
                    or "Yahoo Finance"
                )

                published = (
                    content.get("pubDate")
                    or content.get("publishedAt")
                    or content.get("date")
                    or article.get("pubDate")
                    or article.get("providerPublishTime")
                    or article.get("date")
                )
                if isinstance(published, (int, float)):
                    date = datetime.fromtimestamp(
                        published,
                        tz=timezone.utc,
                    ).isoformat()
                elif isinstance(published, datetime):
                    date = published.isoformat()
                else:
                    date = str(published) if published else "Not available"

                canonical_url = (
                    content.get("canonicalUrl")
                    or content.get("clickThroughUrl")
                    or article.get("link")
                    or article.get("url")
                )
                if isinstance(canonical_url, dict):
                    canonical_url = canonical_url.get("url")

                summary = (
                    content.get("summary")
                    or content.get("description")
                    or article.get("summary")
                    or article.get("description")
                    or title
                )
                summary = " ".join(re.sub(r"<[^>]+>", " ", str(summary)).split())

                normalized_articles.append(
                    {
                        "title": str(title),
                        "date": date,
                        "source": str(source),
                        "impact": article.get("impact") or content.get("impact") or "neutral",
                        "summary": summary,
                        "url": str(canonical_url) if canonical_url else None,
                    }
                )

            logger.info(
                "News search completed ticker=%s articles=%s",
                ticker,
                len(normalized_articles),
            )
            return normalized_articles
        except Exception as exc:
            logger.exception("Failed to fetch news ticker=%s", ticker)
            raise RuntimeError(f"Unable to fetch news for {ticker}") from exc
