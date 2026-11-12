from core.llm.prompting.prompts.general_prompt import (
    GENERAL_PROMPT
)

from core.llm.prompting.prompts.summary_prompt import (
    SUMMARY_PROMPT
)

from core.llm.prompting.prompts.diagnosis_prompt import (
    DIAGNOSIS_PROMPT
)

from core.llm.prompting.prompts.medication_prompt import (
    MEDICATION_PROMPT
)

from core.llm.prompting.prompts.followup_prompt import (
    FOLLOWUP_PROMPT
)

from core.llm.prompting.prompts.investigation_prompt import (
    INVESTIGATION_PROMPT
)

from core.llm.prompting.prompts.abnormal_findings_prompt import (
    ABNORMAL_FINDINGS_PROMPT
)

from core.llm.prompting.prompts.comparison_prompt import (
    COMPARISON_PROMPT
)

from core.llm.prompting.prompts.report_prompt import (
    REPORT_PROMPT
)


class PromptRegistry:
    """
    Registry for all available prompt templates.
    """

    PROMPTS = {

        "general": GENERAL_PROMPT,

        "summary": SUMMARY_PROMPT,

        "diagnosis": DIAGNOSIS_PROMPT,

        "medication": MEDICATION_PROMPT,

        "followup": FOLLOWUP_PROMPT,

        "investigation": INVESTIGATION_PROMPT,

        "abnormal_findings": ABNORMAL_FINDINGS_PROMPT,

        "comparison": COMPARISON_PROMPT,

        "report": REPORT_PROMPT

    }

    # --------------------------------------------------
    # Get Prompt
    # --------------------------------------------------

    @classmethod
    def get_prompt(
        cls,
        intent: str
    ) -> str:
        """
        Returns the prompt template for the
        detected intent.

        Falls back to GENERAL_PROMPT if the
        intent is unknown.
        """

        return cls.PROMPTS.get(

            intent,

            GENERAL_PROMPT

        )