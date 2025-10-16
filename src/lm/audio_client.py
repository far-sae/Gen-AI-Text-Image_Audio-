import os
import logging
from openai import OpenAI
from .base import BaseClient
from src.utils.retry_helper import retry_on_exception

logger = logging.getLogger(__name__)

class OpenAIAudioClient(BaseClient):
    def __init__(self, api_key_env: str, model: str = "gpt-4o-mini-tts", voice: str = "alloy"):
        self.api_key = os.getenv(api_key_env)
        if not self.api_key:
            raise ValueError(f"Missing API key in environment variable: {api_key_env}")
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.voice = voice

    @retry_on_exception()
    def generate(self, prompt: str, output_path: str = "data/outputs/speech.mp3"):
        """
        Generate audio from text and save it to output_path.
        Returns a dictionary with 'file_path'.
        """
        try:
            speech = self.client.audio.speech.create(
                model=self.model,
                voice=self.voice,
                input=prompt
            )
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(speech.read())
            return {"file_path": output_path}
        except Exception:
            logger.exception("Audio generation failed")
            raise

    def health(self):
        return bool(self.api_key)
