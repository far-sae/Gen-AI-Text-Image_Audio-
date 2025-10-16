# Generative AI Project

Modular multi-modal starter for text, image and audio generation.

## Quickstart
1. Create `.env` with API keys (OPENAI_API_KEY, STABILITY_API_KEY, etc.)
2. pip install -r requirements.txt
3. python src/main.py

## Structure
- config/: YAML model and prompt settings
- src/: code (clients, prompt engineering, utils, handlers)
- data/: storage for cache, prompts, outputs
- examples/: runnable scripts
- notebooks/: experiments

## Notes
- Replace placeholder endpoints in clients with official SDKs
- Add authentication, retries, and rate limiting for production


## Additional features added

- GitHub Actions CI workflow for tests and linting (.github/workflows/ci.yml)
- Pre-commit hooks (black, flake8)
- Retry helper using tenacity for robustness on transient failures
- Simple Streamlit password protection via `STREAMLIT_PASSWORD` environment variable (set in .env)
- Unit tests (tests/test_gpt_client.py) using unittest.mock

## How to run CI locally

1. Install pre-commit and hooks:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

2. Run tests:

```bash
pytest
```
