import hashlib
from pathlib import Path

CACHE_DIR = Path("data/cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def cache_write(key: str, content: bytes):
    h = hashlib.sha256(key.encode()).hexdigest()
    p = CACHE_DIR / h
    p.write_bytes(content)
    return str(p)

def cache_read(key: str):
    h = hashlib.sha256(key.encode()).hexdigest()
    p = CACHE_DIR / h
    return p.read_bytes() if p.exists() else None
