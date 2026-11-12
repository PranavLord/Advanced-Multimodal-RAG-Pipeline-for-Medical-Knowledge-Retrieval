from core.llm.llm_factory import (
    LLMFactory
)

llm = LLMFactory.get_llm()

response = llm.generate(
    "Say Hello"
)

print(response)