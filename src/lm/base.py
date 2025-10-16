from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseClient(ABC):
    """Abstract base client for text/image/audio providers."""

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def health(self) -> bool:
        raise NotImplementedError
