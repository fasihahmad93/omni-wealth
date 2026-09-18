import logging
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

LOG_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOG_DIR / "financial_agent.log"

LOG_LEVEL = logging.INFO


def setup_logging() -> None:
    LOG_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    logging.basicConfig(
        level=LOG_LEVEL,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(
                LOG_FILE,
                encoding="utf-8",
            ),
        ],
        force=True,
    )

    logger = logging.getLogger(__name__)

    logger.info(
        "Logging initialized log_file=%s",
        LOG_FILE,
    )