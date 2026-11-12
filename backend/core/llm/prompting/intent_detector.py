class IntentDetector:
    """
    Detects the user's intent from the question.

    This determines which prompt template should
    be used by the Prompt Builder.
    """

    @staticmethod
    def detect(question: str) -> str:

        if not question:
            return "general"

        question = question.lower().strip()

        # ==================================================
        # Report Generation
        # ==================================================

        report_keywords = [

            "generate report",
            "final report",
            "medical report",
            "consultation report",
            "download report"

        ]

        if any(keyword in question for keyword in report_keywords):
            return "report"

        # ==================================================
        # Report Summary
        # ==================================================

        summary_keywords = [

            "summarize",
            "summary",
            "summarise",
            "overview",
            "brief",
            "report summary",
            "explain this report"

        ]

        if any(keyword in question for keyword in summary_keywords):
            return "summary"

        # ==================================================
        # Diagnosis
        # ==================================================

        diagnosis_keywords = [

            "diagnosis",
            "diagnoses",
            "disease",
            "condition",
            "what is wrong",
            "diagnosed with",
            "diagnostic"

        ]

        if any(keyword in question for keyword in diagnosis_keywords):
            return "diagnosis"

        # ==================================================
        # Medication
        # ==================================================

        medication_keywords = [

            "medicine",
            "medication",
            "drug",
            "tablet",
            "capsule",
            "prescription",
            "metformin",
            "insulin",
            "aspirin"

        ]

        if any(keyword in question for keyword in medication_keywords):
            return "medication"

        # ==================================================
        # Follow-up
        # ==================================================

        followup_keywords = [

            "follow up",
            "follow-up",
            "next step",
            "next steps",
            "recommendation",
            "recommendations",
            "what should i do",
            "doctor advised"

        ]

        if any(keyword in question for keyword in followup_keywords):
            return "followup"

        # ==================================================
        # Investigation
        # ==================================================

        investigation_keywords = [

            "test",
            "tests",
            "investigation",
            "investigations",
            "scan",
            "blood test",
            "mri",
            "ct",
            "x-ray",
            "xray",
            "ecg",
            "ultrasound"

        ]

        if any(keyword in question for keyword in investigation_keywords):
            return "investigation"

        # ==================================================
        # Abnormal Findings
        # ==================================================

        abnormal_keywords = [

            "abnormal",
            "high",
            "low",
            "elevated",
            "increased",
            "decreased",
            "glucose",
            "cholesterol",
            "creatinine",
            "hemoglobin",
            "blood sugar",
            "result"

        ]

        if any(keyword in question for keyword in abnormal_keywords):
            return "abnormal_findings"

        # ==================================================
        # Comparison
        # ==================================================

        comparison_keywords = [

            "difference",
            "compare",
            "comparison",
            "vs",
            "versus"

        ]

        if any(keyword in question for keyword in comparison_keywords):
            return "comparison"

        # ==================================================
        # Default
        # ==================================================

        return "general"