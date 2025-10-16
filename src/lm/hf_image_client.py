import os
import logging
import base64
from openai import OpenAI
from .base import BaseClient
from src.utils.retry_helper import retry_on_exception

logger = logging.getLogger(__name__)

class OpenAIImageClient(BaseClient):
    def __init__(self, api_key_env: str, model: str = "gpt-image-1", size: str = "1024x1024"):
        self.api_key = os.getenv(api_key_env)
        if not self.api_key:
            raise ValueError(f"Missing API key in environment variable: {api_key_env}")
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.size = size

    @retry_on_exception()
    def generate(self, prompt: str, **kwargs):
        """
        Generate an image from a prompt.
        Returns a dict with 'image_bytes' and 'url'.
        """
        try:
            result = self.client.images.generate(
                model=self.model,
                prompt=prompt,
                size=kwargs.get("size", self.size)
            )
            image_base64 = result.data[0].b64_json
            image_bytes = base64.b64decode(image_base64)
            return {"image_bytes": image_bytes, "url": result.data[0].url}
        except Exception:
            logger.exception("Image generation failed")
            raise

    def health(self):
        return bool(self.api_key)
