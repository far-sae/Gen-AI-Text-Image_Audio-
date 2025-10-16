from src.lm.gpt_client import GPTClient
client = GPTClient(api_key_env="OPENAI_API_KEY", model="gpt-4o-mini")
print("This example requires OPENAI_API_KEY env var and network access.")
