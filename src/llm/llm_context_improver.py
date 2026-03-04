from llm.clients.base_llm_client import BaseLLMClient


class LLMContextImprover:
    """Improves user context using LLM."""

    def __init__(self, llm: BaseLLMClient) -> None:
        self.llm = llm

    async def improve_with_llm(
        self,
        current_context: str,
        context_request_clarification: str,
    ) -> str:
        """Use the LLM to rewrite/structure the context."""
        system_prompt: str = (
            "You are a helpful assistant that improves user context for better downstream analysis. "
            "Rewrite the user's context to be more structured, clear, and informative, based on the clarification request."
        )

        user_prompt: str = (
            f"CURRENT CONTEXT:\n{current_context}\n\n"
            f"CLARIFICATION REQUEST:\n{context_request_clarification}\n\n"
            "Rewrite the context so it directly addresses the clarification request while preserving the original intent, key facts, and tone. "
            "Return one coherent updated context paragraph (no markdowns, no trailing commas)."
            "It should later be used as input for an analytical summarize, so prioritize clarity, relevance, and informativeness."
        )

        improved_context: str = await self.llm.generate(
            system=system_prompt,
            user=user_prompt,
        )

        return improved_context.strip()
