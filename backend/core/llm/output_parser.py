import json


class OutputParser:
    """
    Cleans and formats the LLM response.
    """

    @staticmethod
    def parse(response: str) -> str:

        if not response:
            return ""

        cleaned = response.strip()

        # Try decoding if the model returned a JSON string
        try:
            cleaned = json.loads(cleaned)
        except Exception:
            pass

        cleaned = cleaned.replace("\\n", "\n")
        cleaned = cleaned.replace("\r\n", "\n")
        cleaned = cleaned.replace("\r", "\n")

        cleaned = "\n".join(
            line.rstrip()
            for line in cleaned.splitlines()
        )

        while "\n\n\n" in cleaned:
            cleaned = cleaned.replace("\n\n\n", "\n\n")

        return cleaned.strip()