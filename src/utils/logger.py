import logging
import yaml
import logging.config
from pathlib import Path

def setup_logging(config_path="config/logging_config.yaml"):
    p = Path(config_path)
    if p.exists():
        cfg = yaml.safe_load(p.read_text())
        logging.config.dictConfig(cfg)
    else:
        logging.basicConfig(level=logging.INFO)
