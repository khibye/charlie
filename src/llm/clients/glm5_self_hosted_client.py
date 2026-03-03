from openai import AsyncOpenAI

from llm.clients.base_llm_client import BaseLLMClient


class GLM5SelfHostedClient(BaseLLMClient):
    """Client for GLM-5 running in a self-hosted manner, accessed via OpenAI-compatible API - https://chat.z.ai."""

    def __init__(
        self,
        model_id: str = "glm-5",
        api_key: str | None = "33c3a0bc61024ab5b30a759e85d7a57e.SYNtg8E2zwey7IWS",
    ) -> None:
        self.model_id = model_id
        self.client = AsyncOpenAI(api_key=api_key, base_url="https://api.z.ai/api/paas/v4/")

    async def generate(self, system: str | None, user: str) -> str:
        messages: list[dict[str, str]] = []

        if system:
            messages.append({"role": "system", "content": system})

        messages.append({"role": "user", "content": user})

        response = await self.client.chat.completions.create(
            model=self.model_id,
            messages=messages,
            max_tokens=800,
            temperature=0.7,
        )

        return response.choices[0].message.content
