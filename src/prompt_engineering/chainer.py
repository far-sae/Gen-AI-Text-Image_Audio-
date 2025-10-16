from typing import List

def chain_prompts(clients, prompts: List[str]):
    result = None
    for client, prompt in zip(clients, prompts):
        resp = client.generate(prompt)
        result = resp.get("text") or resp.get("image_bytes") or resp
    return result
