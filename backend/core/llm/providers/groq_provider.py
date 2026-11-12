from groq import Groq

from config.settings import settings

from core.llm.providers.base_llm import BaseLLM


class GroqProvider(BaseLLM):
    """
    Groq LLM Provider.

    Responsible only for communicating with
    the Groq API.
    """

    def __init__(self):

        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

    def generate(
        self,
        prompt: str
    ) -> str:
        """
        Generate a response using Groq.

        Parameters
        ----------
        prompt : str
            Final prompt sent to Groq.

        Returns
        -------
        str
            Generated response.
        """

        try:

            response = self.client.chat.completions.create(

                model=settings.GROQ_MODEL,

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=settings.GROQ_TEMPERATURE,

                top_p=settings.GROQ_TOP_P,

                max_tokens=settings.GROQ_MAX_OUTPUT_TOKENS

            )

            return response.choices[0].message.content

        except Exception as e:

            raise RuntimeError(
                f"Groq generation failed: {str(e)}"
            )