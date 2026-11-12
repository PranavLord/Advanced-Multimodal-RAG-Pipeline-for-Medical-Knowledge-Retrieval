from typing import Optional

from config.settings import settings

from core.llm.fallback_llm import (
    FallbackLLM
)

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


class LLMFactory:
    """
    Factory responsible for returning the
    appropriate Language Model provider.
    """

    @staticmethod
    def get_llm(
        provider: Optional[str] = None
    ):
        """
        Return the requested LLM provider.

        If no provider is supplied,
        use the default provider from settings.
        """

        provider = (
            provider
            or settings.LLM_PROVIDER
        ).lower()

        # ==================================================
        # Automatic Failover
        # ==================================================

        if provider == "auto":

            print("Using Automatic LLM Fallback")

            return FallbackLLM()

        # ==================================================
        # Gemini
        # ==================================================

        elif provider == "gemini":

            print("Using Gemini Provider")

            return GeminiProvider()

        # ==================================================
        # Groq
        # ==================================================

        elif provider == "groq":

            print("Using Groq Provider")

            return GroqProvider()

        # ==================================================
        # Cohere
        # ==================================================

        elif provider == "cohere":

            print("Using Cohere Provider")

            return CohereProvider()

        # ==================================================
        # OpenRouter
        # ==================================================

        elif provider == "openrouter":

            print("Using OpenRouter Provider")

            return OpenRouterProvider()

        # ==================================================
        # Invalid Provider
        # ==================================================

        raise ValueError(
            f"Unsupported LLM Provider: {provider}"
        )