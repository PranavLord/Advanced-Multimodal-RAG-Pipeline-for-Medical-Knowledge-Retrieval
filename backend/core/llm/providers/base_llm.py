from abc import ABC, abstractmethod


class BaseLLM(ABC):
    """
    Abstract Base Class for all LLM providers.

    Every LLM implementation must inherit from this class
    and implement the generate() method.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str
    ) -> str:
        """
        Generate a response from the LLM.

        Parameters
        ----------
        prompt : str
            Final prompt sent to the language model.

        Returns
        -------
        str
            Generated response from the model.
        """
        pass