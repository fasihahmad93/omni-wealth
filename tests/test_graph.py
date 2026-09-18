import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from financial_agent.graph.financial_graph import build_orchestrator, run_financial_analysis

def test_build_orchestrator():
    assert build_orchestrator() is not None

def test_run_financial_analysis():
    result = run_financial_analysis("TEST")
    assert result["decision"].decision in {"BUY", "HOLD", "SELL"}
