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

This repository is an educational/research framework, not financial advice or an automated trading system. The initial data providers are deliberately simple offline/demo providers so the system can be developed and tested without API credentials.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python main.py RELIANCE
pytest -q
```

The default demo runs without an LLM by using deterministic demo agents. The interfaces are designed so an Ollama/other LLM implementation can be plugged in later.
