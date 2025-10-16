from .handlers.api_handler import API
from .utils.logger import setup_logging

setup_logging()

def demo():
    api = API()
    text = "OpenAI models are powerful and can summarize, translate, and generate text."
    out = api.summarize(text)
    print("SUMMARY:", out.get("text"))

if __name__ == "__main__":
    demo()
