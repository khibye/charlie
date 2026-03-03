from abc import ABC, abstractmethod


class BaseLLMClient(ABC):
    """A minimal interface so we can swap models/providers without changing business logic."""

    @abstractmethod
    async def generate(self, system: str | None, user: str) -> str:
        """Return a single generated string."""
        raise NotImplementedError("unimplemented LLMClient interface method")
