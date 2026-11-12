from core.llm.generation_pipeline import (
    GenerationPipeline
)


pipeline = GenerationPipeline()

response = pipeline.generate(

    question="What diagnosis is mentioned in the report?"

)

print()

print("=" * 80)

print("FINAL RESPONSE")

print("=" * 80)

print()

print(response)