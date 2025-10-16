from typing import Dict
import yaml
import logging
logger = logging.getLogger(__name__)

class PromptEngine:
    def __init__(self, templates: Dict):
        self.templates = templates

    def format(self, key: str, **kwargs):
        tpl = self.templates.get(key, {}).get("template")
        if not tpl:
            raise ValueError(f"No template for key {key}")
        return tpl.format(**kwargs)
