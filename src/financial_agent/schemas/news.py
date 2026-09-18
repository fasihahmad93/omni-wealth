from pydantic import BaseModel

class NewsItem(BaseModel):
    title: str
    date: str
    source: str
    impact: str
    summary: str

class NewsAnalysis(BaseModel):
    ticker: str
    sentiment: str
    items: list[NewsItem] = []
    key_risks: list[str] = []
    key_catalysts: list[str] = []
