import requests

from config.settings import settings

from core.llm.providers.base_llm import BaseLLM


class OpenRouterProvider(BaseLLM):
    """
    OpenRouter LLM Provider.

    Responsible only for communicating with
    the OpenRouter API.
    """

    def __init__(self):

        self.url = "https://openrouter.ai/api/v1/chat/completions"

        self.headers = {

            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",

            "Content-Type": "application/json",

            "HTTP-Referer": "https://medical-rag.local",

            "X-Title": "Advanced Multimodal Medical RAG"

        }

    def generate(
        self,
        prompt: str
    ) -> str:
        """
        Generate a response using OpenRouter.

        Parameters
        ----------
        prompt : str
            Final prompt sent to OpenRouter.

        Returns
        -------
        str
            Generated response.
        """

        try:

            print("\n" + "=" * 80)
            print("OPENROUTER CONFIGURATION")
            print("=" * 80)
            print(f"URL   : {self.url}")
            print(f"MODEL : {settings.OPENROUTER_MODEL}")
            print("=" * 80)

            payload = {

                "model": settings.OPENROUTER_MODEL,

                "messages": [

                    {
                        "role": "user",
                        "content": prompt
                    }

                ],

                "temperature": settings.OPENROUTER_TEMPERATURE,

                "top_p": settings.OPENROUTER_TOP_P,

                "max_tokens": settings.OPENROUTER_MAX_OUTPUT_TOKENS

            }

            response = requests.post(

                self.url,

                headers=self.headers,

                json=payload,

                timeout=120

            )

            print("\n" + "=" * 80)
            print("OPENROUTER RESPONSE")
            print("=" * 80)
            print("Status Code :", response.status_code)
            print("Body :")
            print(response.text)
            print("=" * 80)

            result = response.json()

            # ------------------------------------------
            # API Error
            # ------------------------------------------

            if response.status_code != 200:

                error_message = result.get(

                    "error",

                    {}

                ).get(

                    "message",

                    "Unknown OpenRouter Error"

                )

                raise RuntimeError(error_message)

            # ------------------------------------------
            # Success
            # ------------------------------------------

            return result["choices"][0]["message"]["content"]

        except Exception as e:

            raise RuntimeError(

                f"OpenRouter generation failed: {str(e)}"

            )