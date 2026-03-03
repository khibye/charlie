from collections.abc import AsyncIterator
from typing import Any

from consts.defaults import DEFAULT_PROMPT
from llm.clients.base_llm_client import BaseLLMClient


class ArticleLLMCreator:
    """Creates an analytical article from raw data + user context.

    IMPORTANT: This class is intentionally a skeleton.
    We'll later implement a map/reduce-style pipeline (batch summaries -> global synthesis).
    """

    def __init__(self, llm: BaseLLMClient) -> None:
        self.llm = llm

    async def create_article(
        self,
        fetched_data: list[dict[str, Any]],
        user_context: str,
        user_id: str,
        prompt: str = DEFAULT_PROMPT,
    ) -> str:
        """Main entry point."""
        raise NotImplementedError

    async def iter_batches(
        self,
        *,
        fetched_data: list[dict[str, Any]],
        batch_size: int,
    ) -> AsyncIterator[list[dict[str, Any]]]:
        """Yield data in batches. (We will later make this more sophisticated.)"""
        raise NotImplementedError

    async def summarize_batch(
        self,
        *,
        batch: list[dict[str, Any]],
        user_context: str,
        prompt: str = DEFAULT_PROMPT,
    ) -> dict[str, Any]:
        """Map step: turn a batch into structured insights."""
        raise NotImplementedError

    async def synthesize_article(
        self,
        *,
        batch_summaries: list[dict[str, Any]],
        user_context: str,
        prompt: str = DEFAULT_PROMPT,
    ) -> str:
        """Reduce step: combine structured batch summaries into final prose."""
        raise NotImplementedError
