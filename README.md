# Financial Agent

A modular educational financial research system that combines deterministic financial analytics with LLM-based agents.

## Architecture

```text
User
  |
  v
Orchestrator Agent
  |
  +--> Market Agent ------> Market Tools ------> Analytics
  |
  +--> Fundamental Agent -> Fundamental Tools -> Analytics
  |
  +--> News Agent -------> News Tools --------> Evidence
  |
  +--> Valuation/Risk Agent ------------------> Analytics
  |
  v
Decision Agent
  |
  v
BUY / HOLD / SELL
```

## Design principles

1. Deterministic calculations stay in `analytics/`.
2. External data access stays in `tools/` and `data/`.
3. Agents reason over structured evidence.
4. Pydantic schemas define contracts between components.
5. LangGraph owns orchestration/state.
6. Every function contains useful logging.
7. Tests cover every public tool and agent method.

## Important

This repository is an educational/research framework, not financial advice or an automated trading system. The CLI uses Yahoo Finance and Google News RSS and requires a network connection. Demo providers power the offline orchestrator and tests. Yahoo may omit individual metrics; missing values are reported as unavailable.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python main.py RELIANCE.NS
pytest -q
```

The CLI defaults to `ASIANPAINT.NS` and prints market, fundamental, news, valuation/risk, and BUY/HOLD/SELL analyses. Pass a Yahoo Finance ticker as the first argument. The demo orchestrator runs without network access. The interfaces are designed so an Ollama/other LLM implementation can be plugged in later.
