from src.handlers.api_handler import API
api = API()
while True:
    q = input("You: ")
    if q.lower() in ("exit","quit"): break
    r = api.summarize(q)
    print("Bot:", r.get("text"))
