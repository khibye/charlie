from ollama import AsyncClient

from llm.clients.base_llm_client import BaseLLMClient


class QwenLocalCPUClient(BaseLLMClient):
    """Skeleton client for Qwen2.5-7B-Instruct running locally on CPU."""

    def __init__(self, model_id: str = "qwen2.5:7b-instruct") -> None:
        self.model_id = model_id

    async def generate(self, system: str | None, user: str) -> str:
        messages: list[dict[str, str]] = []

        if system:
            messages.append({"role": "system", "content": system})

        messages.append({"role": "user", "content": user})

        response = await AsyncClient().chat(model=self.model_id, messages=messages)

        return getattr(getattr(response, "message", None), "content", None)
