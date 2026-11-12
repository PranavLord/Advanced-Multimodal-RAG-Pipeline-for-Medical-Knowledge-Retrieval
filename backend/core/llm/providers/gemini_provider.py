from google import genai

from config.settings import settings

from core.llm.providers.base_llm import BaseLLM


class GeminiProvider(BaseLLM):
    """
    Gemini LLM Provider.

    Responsible only for communicating with
    the Gemini API.
    """

    def __init__(self):

        self.client = genai.Client(
            api_key=settings.GOOGLE_API_KEY
        )

    def generate(
        self,
        prompt: str
    ) -> str:
        """
        Generate a response using Gemini.

        Parameters
        ----------
        prompt : str
            Final prompt sent to Gemini.

        Returns
        -------
        str
            Generated response.
        """

        try:

            response = self.client.models.generate_content(

                model=settings.GEMINI_MODEL,

                contents=prompt,

                config={

                    "temperature": settings.GEMINI_TEMPERATURE,

                    "top_p": settings.GEMINI_TOP_P,

                    "max_output_tokens": settings.GEMINI_MAX_OUTPUT_TOKENS

                }

            )

            return response.text

        except Exception as e:

            raise RuntimeError(
                f"Gemini generation failed: {str(e)}"
            )