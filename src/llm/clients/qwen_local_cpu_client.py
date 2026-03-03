from llm.clients.base_llm_client import BaseLLMClient


class QwenLocalCPUClient(BaseLLMClient):
    """Skeleton client for Qwen2.5-7B-Instruct running locally on CPU.

    Implementation will be added later (e.g., via llama.cpp / transformers / vLLM).
    """

    def __init__(self, model_id: str = "Qwen/Qwen2.5-7B-Instruct") -> None:
        self.model_id = model_id

    async def generate(self, system: str | None, user: str) -> str:
        raise NotImplementedError("Wire Qwen local inference here")
