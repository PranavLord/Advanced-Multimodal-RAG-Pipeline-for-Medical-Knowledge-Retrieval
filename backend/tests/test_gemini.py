from core.llm.providers.gemini_provider import (
    GeminiProvider
)


llm = GeminiProvider()

prompt = """
Context:
Patient has right lower lobe pneumonia.

Question:
What diagnosis does the report mention?
"""

response = llm.generate(
    prompt
)

print(response)