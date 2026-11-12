from core.llm.prompting.prompt_builder import (
    PromptBuilder
)

contexts = [

    {
        "text":
        "Diagnosis: Right lower lobe pneumonia.",

        "chunk_index":
        1,

        "source":
        "sample.pdf"
    },

    {
        "text":
        "Medicine: Azithromycin 500 mg once daily.",

        "chunk_index":
        2,

        "source":
        "sample.pdf"
    },

    {
        "text":
        "Chest X-ray shows infiltrates.",

        "chunk_index":
        3,

        "source":
        "sample.pdf"
    }

]

question = (
    "What diagnosis does the patient have?"
)

prompt = PromptBuilder.build(
    contexts,
    question
)

print(prompt)