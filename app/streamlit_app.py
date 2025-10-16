
import streamlit as st
from dotenv import load_dotenv
import os
from io import BytesIO
import base64

# load environment
load_dotenv()

from src.lm.gpt_client import GPTClient

# Simple password auth (set STREAMLIT_PASSWORD in env). Not production-grade.
def check_password():
    pwd = os.getenv('STREAMLIT_PASSWORD')
    if not pwd:
        return True  # no password set, allow
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if st.session_state.get('authenticated'):
        return True
    with st.sidebar:
        st.write('Protected app — enter password')
        entered = st.text_input('Password', type='password')
        if st.button('Login'):
            if entered == pwd:
                st.session_state.authenticated = True
                st.experimental_rerun()
            else:
                st.error('Incorrect password')
                return False
if not check_password():
    st.stop()
from src.lm.hf_image_client import OpenAIImageClient
from src.lm.audio_client import OpenAIAudioClient

st.set_page_config(page_title="Generative AI Demo", layout="wide")

st.title("🎛️ Generative AI — Text · Image · Audio (OpenAI)")
st.write("A simple Streamlit dashboard to demo text, image and audio generation via OpenAI.")

# Load config values (fallbacks)
MODEL_TEXT = os.getenv("OPENAI_TEXT_MODEL", "gpt-4o-mini")
MODEL_IMAGE = os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-1")
MODEL_AUDIO = os.getenv("OPENAI_AUDIO_MODEL", "gpt-4o-mini-tts")

tabs = st.tabs(["Text", "Image", "Audio"])

with tabs[0]:
    st.header("📝 Text Generation")
    prompt = st.text_area("Enter prompt", value="Write a friendly 3-sentence intro to generative AI.")
    max_tokens = st.slider("Max tokens", 50, 2048, 256)
    temp = st.slider("Temperature", 0.0, 1.5, 0.7, step=0.05)
    col1, col2 = st.columns([1, 3])
    with col1:
        run = st.button("Generate Text")
    with col2:
        model = st.text_input("Model", value=MODEL_TEXT)

    if run:
        client = GPTClient(api_key_env="OPENAI_API_KEY", model=model, max_tokens=max_tokens, temperature=temp)
        with st.spinner("Generating..."):
            try:
                out = client.generate(prompt)
                st.subheader("Output")
                st.write(out.get("text"))
                st.subheader("Raw Response (collapsed)")
                st.json(out.get("raw") or {})
            except Exception as e:
                st.error(f"Error: {e}")

with tabs[1]:
    st.header("🎨 Image Generation")
    img_prompt = st.text_area("Image prompt", value="A watercolor painting of a fox reading a book under moonlight")
    size = st.selectbox("Size", ["512x512", "768x768", "1024x1024"], index=2)
    steps = st.slider("Quality steps (provider-specific)", 10, 100, 30)
    col1, col2 = st.columns([1, 3])
    with col1:
        gen_img = st.button("Generate Image")
    with col2:
        img_model = st.text_input("Image model", value=MODEL_IMAGE)

    if gen_img:
        img_client = OpenAIImageClient(api_key_env="OPENAI_API_KEY", model=img_model, size=size)
        with st.spinner("Generating image..."):
            try:
                res = img_client.generate(img_prompt, size=size)
                img_bytes = res.get("image_bytes")
                if img_bytes:
                    st.image(img_bytes, use_column_width=True)
                    # download link
                    b64 = base64.b64encode(img_bytes).decode()
                    href = f'<a href="data:file/png;base64,{b64}" download="generated.png">Download image</a>'
                    st.markdown(href, unsafe_allow_html=True)
                else:
                    st.warning("No image bytes returned. Check API / model.")
            except Exception as e:
                st.error(f"Image generation error: {e}")

with tabs[2]:
    st.header("🔊 Audio Generation (TTS)")
    audio_text = st.text_area("Text to speak", value="Hello — this is a demo of OpenAI text-to-speech.")
    voice = st.text_input("Voice name (provider-specific)", value="alloy")
    out_path = st.text_input("Output path", value="data/outputs/speech.mp3")
    col1, col2 = st.columns([1,3])
    with col1:
        gen_audio = st.button("Generate Audio")
    with col2:
        audio_model = st.text_input("Audio model", value=MODEL_AUDIO)

    if gen_audio:
        audio_client = OpenAIAudioClient(api_key_env="OPENAI_API_KEY", model=audio_model, voice=voice)
        with st.spinner("Generating audio..."):
            try:
                res = audio_client.generate(audio_text, output_path=out_path)
                file_path = res.get("file_path") or out_path
                if os.path.exists(file_path):
                    audio_bytes = open(file_path, "rb").read()
                    st.audio(audio_bytes)
                    b64 = base64.b64encode(audio_bytes).decode()
                    href = f'<a href="data:audio/mpeg;base64,{b64}" download="{os.path.basename(file_path)}">Download audio</a>'
                    st.markdown(href, unsafe_allow_html=True)
                else:
                    st.warning("Audio file was not created. Check API response.")
            except Exception as e:
                st.error(f"Audio generation error: {e}")

st.markdown("---")
st.write("Tip: set your OPENAI_API_KEY in a .env file or environment before running this app.")
