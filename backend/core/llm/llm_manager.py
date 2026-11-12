from typing import Optional

from core.llm.llm_factory import LLMFactory


class LLMManager:
    """
    Handles LLM Selection.

    Modes
    -----
    Auto
        Gemini
            ↓
        Groq
            ↓
        Cohere
            ↓
        OpenRouter

    Manual
        Uses only the selected provider.
    """

    @staticmethod
    def generate(
        prompt: str,
        provider: Optional[str] = None
    ) -> dict:

        # ==================================================
        # Debug
        # ==================================================

        print("\n" + "=" * 60)
        print("LLM MANAGER")
        print(f"Incoming Provider : {provider}")
        print("=" * 60)

        # ==================================================
        # AUTO MODE
        # ==================================================

        if provider is None or provider.lower() == "auto":

            print("\nUsing Automatic LLM Failover...")

            llm = LLMFactory.get_llm("auto")

            result = llm.generate(prompt)

            # FallbackLLM already returns:
            # {
            #     "response": "...",
            #     "provider": "groq"
            # }

            return result

        # ==================================================
        # MANUAL MODE
        # ==================================================

        current_provider = provider.lower()

        try:

            print(
                f"\nTrying Provider : {current_provider.upper()}"
            )

            llm = LLMFactory.get_llm(
                current_provider
            )

            response = llm.generate(
                prompt
            )

            print(
                f"✓ Success : {current_provider.upper()}"
            )

            return {

                "response": response,

                "provider": current_provider

            }

        except Exception as e:

            print(
                f"✗ Failed : {current_provider.upper()}"
            )

            print(str(e))

            raise RuntimeError(

                f"{current_provider.upper()} generation failed.\n\n{e}"

            )