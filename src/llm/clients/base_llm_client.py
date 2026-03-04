from abc import ABC, abstractmethod
from collections.abc import AsyncIterator


class BaseLLMClient(ABC):
    """A minimal interface so we can swap models/providers without changing business logic."""

    @abstractmethod
    async def generate(self, system: str | None, user: str) -> str:
        """Return a single generated string."""
        raise NotImplementedError("unimplemented LLMClient interface method")

    @abstractmethod
    async def generate_stream(self, system: str | None, user: str) -> AsyncIterator[str]:
        """Yield generated text chunks."""
        raise NotImplementedError("unimplemented LLMClient interface method")
