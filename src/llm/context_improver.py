from llm.clients.base_llm_client import BaseLLMClient


class ContextImprover:
    """Two pipelines:

    1) manual: user edits stored context
    2) llm: turn natural language preference into a crisp, reusable context string
    """

    def __init__(self, llm: BaseLLMClient) -> None:
        self.llm = llm

    async def manual_update(
        self, user_id: str, country: str, city: str, new_context: str
    ) -> str:
        """Validate/sanitize the context and return the final stored version."""
        raise NotImplementedError

    async def improve_with_llm(self, natural_language_context: str) -> str:
        """Use the LLM to rewrite/structure the context."""
        raise NotImplementedError
