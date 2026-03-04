import os
from collections.abc import AsyncIterator

from openai import AsyncOpenAI

from llm.clients.base_llm_client import BaseLLMClient


class GLM5SelfHostedClient(BaseLLMClient):
    """Client for GLM-5 running in a self-hosted manner, accessed via OpenAI-compatible API - https://chat.z.ai."""

    def __init__(
        self,
        model_id: str = "GLM-5",
        api_key: str | None = os.getenv("API_KEY"),
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
        )

        return response.choices[0].message.content

    async def generate_stream(self, system: str | None, user: str) -> AsyncIterator[str]:
        messages: list[dict[str, str]] = []

        if system:
            messages.append({"role": "system", "content": system})

        messages.append({"role": "user", "content": user})

        response_stream = await self.client.chat.completions.create(
            model=self.model_id,
            messages=messages,
            stream=True,
        )

        async for chunk in response_stream:
            choices = getattr(chunk, "choices", None)
            if not choices:
                continue

            delta = getattr(choices[0], "delta", None)
            content = getattr(delta, "content", None) if delta else None

            if content:
                yield content
