from core.llm.providers.groq_provider import (
    GroqProvider
)

llm = GroqProvider()

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