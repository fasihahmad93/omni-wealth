import logging

logger = logging.getLogger(__name__)

class OrchestratorAgent:
    def __init__(self, market_agent, fundamental_agent, news_agent, valuation_risk_agent, decision_agent):
        logger.info("Initializing OrchestratorAgent")
        self.market_agent = market_agent
        self.fundamental_agent = fundamental_agent
        self.news_agent = news_agent
        self.valuation_risk_agent = valuation_risk_agent
        self.decision_agent = decision_agent

    def run(self, ticker: str) -> dict:
        logger.info("OrchestratorAgent starting ticker=%s", ticker)
        market = self.market_agent.analyze(ticker)
        fundamental = self.fundamental_agent.analyze(ticker)
        news = self.news_agent.analyze(ticker)
        valuation = self.valuation_risk_agent.analyze(ticker)
        decision = self.decision_agent.decide(ticker, market, fundamental, news, valuation)
        logger.info("OrchestratorAgent completed ticker=%s decision=%s", ticker, decision.decision)
        return {
            "ticker": ticker,
            "market_analysis": market,
            "fundamental_analysis": fundamental,
            "news_analysis": news,
            "valuation_analysis": valuation,
            "decision": decision,
            "errors": [],
        }
