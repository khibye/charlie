import asyncio
import json
from collections.abc import Iterator
from typing import Any

from loguru import logger

from .clients.base_llm_client import BaseLLMClient
from .prompts import (
    DEFAULT_ANALYSIS_SYSTEM_PROMPT,
    DEFAULT_SUMMARIZE_SYSTEM_PROMPT,
    get_summarize_batch_user_prompt,
    get_synthesize_summarize_user_prompt,
)


class LLMSummarizeCreator:
    """Creates an analytical summarize from raw data + user context.

    IMPORTANT: This class is intentionally a skeleton.
    We'll later implement a map/reduce-style pipeline (batch summaries -> global synthesis).
    """

    def __init__(self, llm: BaseLLMClient) -> None:
        self.llm = llm

    async def create_summarize(
        self,
        fetched_data: list[str],
        user_context: str,
    ) -> str:
        """Main entry point.

        Orchestrates a simple map/reduce pipeline:
        - Split raw documents into batches
        - Summarize each batch into structured insights (map)
        - Synthesize final prose summarize from all batch summaries (reduce)

        NOTE: iter_batches / summarize_batch / synthesize_summarize are treated as black boxes.
        """

        # Fast path: no data
        if not fetched_data:
            return "No data available for the selected filters."

        # A conservative default that works reasonably on CPU inference.
        # TODO: We'll make this adaptive later (e.g., by token estimation).

        semaphore: asyncio.Semaphore = asyncio.Semaphore(3)
        batch_size: int = 850

        tasks = [
            asyncio.create_task(
                self.summarize_batch(
                    batch=batch,
                    user_context=user_context,
                    semaphore=semaphore,
                )
            )
            for batch in self.iter_batches(fetched_data=fetched_data, batch_size=batch_size)
        ]

        results = await asyncio.gather(*tasks)

        batch_summaries: list[dict[str, Any]] = []
        for summary in results:
            if summary:
                batch_summaries.append(summary)

        if not batch_summaries:
            return "Insufficient signal to generate an summarize from the available data."

        summarize = await self.synthesize_summarize(
            batch_summaries=batch_summaries,
            user_context=user_context,
        )

        return summarize

    def iter_batches(
        self,
        *,
        fetched_data: list[str],
        batch_size: int,
    ) -> Iterator[list[str]]:
        """Yield data in batches. TODO: (We will later make this more sophisticated.)"""
        if batch_size <= 0:
            raise ValueError("batch_size must be a positive integer")

        total: int = len(fetched_data)

        for start in range(0, total, batch_size):
            end = min(start + batch_size, total)
            yield fetched_data[start:end]

    async def summarize_batch(
        self,
        batch: list[str],
        user_context: str,
        semaphore: asyncio.Semaphore,
    ) -> dict[str, Any]:
        async with semaphore:
            logger.info(f"Starting batch of {len(batch)} documents")
            """Map step: turn a batch into structured insights."""
            # Prepare a compact, indexed representation of the batch so we can cite items later.
            indexed_docs: list[dict[str, Any]] = []
            for i, content in enumerate(batch):
                indexed_docs.append({"_idx": i, "content": content})

            # We request structured JSON so downstream synthesis can be robust.
            user_prompt: str = get_summarize_batch_user_prompt(
                user_context=user_context,
                indexed_docs=indexed_docs,
            )

            if hasattr(self.llm, "generate"):
                text: str = await self.llm.generate(
                    system=DEFAULT_ANALYSIS_SYSTEM_PROMPT, user=user_prompt
                )
            else:
                raise TypeError(
                    "BaseLLMClient must expose an async method named generate(system=..., user=...), "
                    "which returns the generated text as a string."
                )

            # Parse strict JSON. If parsing fails, return a minimal structure with the raw text
            # so the pipeline can still proceed.
            try:
                result: dict[str, Any] = json.loads(text)
            except json.JSONDecodeError:
                return {
                    "themes": [],
                    "indirect_signals": [],
                    "notable_entities": {"people": [], "companies": [], "places": [], "files": []},
                    "notable_dates": [],
                    "anomalies": [],
                    "open_questions": ["Model returned non-JSON output for this batch."],
                    "evidence": [],
                    "_raw": text,
                }

            if not isinstance(result, dict):
                return {
                    "themes": [],
                    "indirect_signals": [],
                    "notable_entities": {"people": [], "companies": [], "places": [], "files": []},
                    "notable_dates": [],
                    "anomalies": [],
                    "open_questions": ["Model returned JSON but not an object for this batch."],
                    "evidence": [],
                    "_raw": text,
                }

            logger.info(f"Completed batch of {len(batch)} documents")
            return result

    async def synthesize_summarize(
        self,
        batch_summaries: list[dict[str, Any]],
        user_context: str,
    ) -> str:
        """Reduce step: combine structured batch summaries into final prose."""

        # Fast path: no summaries
        if not batch_summaries:
            return "No insights available to synthesize an summarize."

        # We will pass structured summaries to the model and ask it to write prose.
        # Keep it JSON so the model can reliably read the structure.
        summaries_json: str = json.dumps(batch_summaries, ensure_ascii=False)

        user_prompt = get_synthesize_summarize_user_prompt(
            user_context=user_context,
            summaries_json=summaries_json,
        )

        if hasattr(self.llm, "generate"):
            return await self.llm.generate(system=DEFAULT_SUMMARIZE_SYSTEM_PROMPT, user=user_prompt)
        else:
            raise TypeError(
                "BaseLLMClient must expose an async method named generate(system=..., user=...), "
                "which returns the generated text as a string."
            )
