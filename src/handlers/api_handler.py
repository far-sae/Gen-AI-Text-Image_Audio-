from ..lm.gpt_client import GPTClient
from ..prompt_engineering.templates import PromptEngine
from ..utils.logger import setup_logging
import yaml, pathlib

setup_logging()

CONFIG = yaml.safe_load(pathlib.Path("config/model_config.yaml").read_text())
TEMPLATES = yaml.safe_load(pathlib.Path("config/prompt_templates.yaml").read_text())

class API:
    def __init__(self):
        text_conf = CONFIG["text"]
        self.text_client = GPTClient(api_key_env=text_conf["api_key_env"],
                                    model=text_conf["model"],
                                    max_tokens=text_conf["max_tokens"],
                                    temperature=text_conf["temperature"])
        self.prompter = PromptEngine(TEMPLATES)

    def summarize(self, text: str):
        prompt = self.prompter.format("summarize", input_text=text)
        return self.text_client.generate(prompt)
