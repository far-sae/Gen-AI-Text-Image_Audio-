import os
import logging
from openai import OpenAI
from .base import BaseClient
from src.utils.retry_helper import retry_on_exception

logger = logging.getLogger(__name__)

class GPTClient(BaseClient):
    def __init__(self, api_key_env: str, model: str, max_tokens=512, temperature=0.7):
        self.api_key = os.getenv(api_key_env)
        if not self.api_key:
            raise ValueError(f"Missing API key in environment variable: {api_key_env}")
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature

    @retry_on_exception()
    def generate(self, prompt: str, **kwargs):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=kwargs.get("max_tokens", self.max_tokens),
                temperature=kwargs.get("temperature", self.temperature)
            )
            text = response.choices[0].message.content.strip()
            return {"text": text, "raw": response.model_dump()}
        except Exception as e:
            logger.exception("GPTClient generate error")
            raise

    def health(self):
        return bool(self.api_key)
