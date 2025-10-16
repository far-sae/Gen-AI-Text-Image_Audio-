from src.lm.hf_image_client import HFImageClient
client = HFImageClient(api_key_env="STABILITY_API_KEY", model="stable-diffusion-v1")
print("This example requires STABILITY_API_KEY and a real endpoint.")
