import cohere

from config.settings import settings

from core.llm.providers.base_llm import BaseLLM


class CohereProvider(BaseLLM):
    """
    Cohere LLM Provider.

    Responsible only for communicating with
    the Cohere API.
    """

    def __init__(self):

        self.client = cohere.ClientV2(
            api_key=settings.COHERE_API_KEY
        )

    def generate(
        self,
        prompt: str
    ) -> str:
        """
        Generate a response using Cohere.

        Parameters
        ----------
        prompt : str
            Final prompt sent to Cohere.

        Returns
        -------
        str
            Generated response.
        """

        try:

            response = self.client.chat(

                model=settings.COHERE_MODEL,

                messages=[

                    {
                        "role": "user",
                        "content": prompt
                    }

                ],

                temperature=settings.COHERE_TEMPERATURE,

                p=settings.COHERE_TOP_P,

                max_tokens=settings.COHERE_MAX_OUTPUT_TOKENS

            )

            return response.message.content[0].text

        except Exception as e:

            raise RuntimeError(
                f"Cohere generation failed: {str(e)}"
            )