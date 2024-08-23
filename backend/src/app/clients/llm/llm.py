import tiktoken
from langchain_openai import ChatOpenAI

from src.app.clients.llm.helper import langfuse_handler


class LLM(object):
    def __init__(
        self,
        model: str,
        api_key: str,
        max_tokens: int = 4096,
        temperature: float = 0,
        langfuse_enabled: bool = False,
    ):
        self.model = model
        self.api_key = api_key
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.langfuse_enabled = langfuse_enabled
        self.llm = self.get_llm_model()

        # encoding
        self.encoding = tiktoken.get_encoding("o200k_base")

    def get_llm_model(self):
        return ChatOpenAI(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            api_key=self.api_key,
        )

    async def get_chat_response(
        self,
        messages,
    ):
        # setting config
        if self.langfuse_enabled:
            config = {"callback": [langfuse_handler]}
        else:
            config = {}

        # process
        async for chunk in self.llm.astream(messages, config=config):
            yield chunk.content

    def num_tokens_from_message(
        self,
        message: str,
    ) -> int:
        return len(self.encoding.encode(message))

    def reduce_tokens_from_message(
        self,
        message: str,
        token_limits: int,
    ):
        message = self.encoding.encode(message)[:token_limits]
        return self.encoding.decode(message)
