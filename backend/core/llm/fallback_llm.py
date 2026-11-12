from core.llm.providers.base_llm import BaseLLM

from core.llm.providers.gemini_provider import (
    GeminiProvider
)

from core.llm.providers.groq_provider import (
    GroqProvider
)

from core.llm.providers.cohere_provider import (
    CohereProvider
)

from core.llm.providers.openrouter_provider import (
    OpenRouterProvider
)


class FallbackLLM(BaseLLM):
    """
    Automatic LLM Failover.

    Priority

    1. Gemini
    2. Groq
    3. Cohere
    4. OpenRouter
    """

    def __init__(self):

        self.providers = [

            (
                "Gemini",
                GeminiProvider()
            ),

            (
                "Groq",
                GroqProvider()
            ),

            (
                "Cohere",
                CohereProvider()
            ),

            (
                "OpenRouter",
                OpenRouterProvider()
            )

        ]

    # --------------------------------------------------
    # Determine whether fallback should occur
    # --------------------------------------------------

    @staticmethod
    def _should_fallback(error: Exception) -> bool:

        message = str(error).lower()

        fallback_keywords = [

            "401",
            "403",
            "429",
            "500",
            "502",
            "503",

            "resource_exhausted",
            "quota",
            "quota exceeded",
            "rate limit",
            "rate_limit",
            "too many requests",

            "timeout",
            "timed out",
            "connection",
            "network",

            "service unavailable",
            "internal server error",

            "authentication",
            "unauthorized",
            "forbidden",

            "invalid api key",
            "insufficient_quota"

        ]

        return any(

            keyword in message

            for keyword in fallback_keywords

        )

        # --------------------------------------------------
    # Generate
    # --------------------------------------------------

    def generate(
        self,
        prompt: str
    ) -> dict:

        last_exception = None

        for provider_name, provider in self.providers:

            try:

                print("\n" + "=" * 60)
                print(f"Trying {provider_name} Provider")
                print("=" * 60)

                response = provider.generate(
                    prompt
                )

                print(f"✓ {provider_name} succeeded.")

                return {

                    "response": response,

                    "provider": provider_name.lower()

                }

            except Exception as e:

                last_exception = e

                print(f"✗ {provider_name} failed.")
                print(e)

                if not self._should_fallback(e):

                    print("\nNon-provider error detected.")
                    print("Stopping fallback immediately.")

                    raise

                print("\nProvider unavailable.")
                print("Trying next provider...")

        raise RuntimeError(

            "\nAll configured LLM providers failed.\n\n"

            f"Last Error:\n{last_exception}"

        )