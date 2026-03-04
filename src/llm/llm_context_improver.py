from llm.clients.base_llm_client import BaseLLMClient
from llm.prompts import DEFAULT_CONTEXT_IMPROVER_SYSTEM_PROMPT, get_context_improver_user_prompt


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

        user_prompt: str = get_context_improver_user_prompt(
            current_context=current_context,
            context_request_clarification=context_request_clarification,
        )

        improved_context: str = await self.llm.generate(
            system=DEFAULT_CONTEXT_IMPROVER_SYSTEM_PROMPT,
            user=user_prompt,
        )

        return improved_context.strip()
