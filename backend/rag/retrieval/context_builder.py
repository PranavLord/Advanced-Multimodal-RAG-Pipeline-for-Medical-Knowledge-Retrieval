class ContextBuilder:

    @staticmethod
    def build(
        matches
    ):

        contexts = []

        for match in matches:

            contexts.append(
                match.metadata["text"]
            )

        return "\n\n".join(
            contexts
        )