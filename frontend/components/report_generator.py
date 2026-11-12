import streamlit as st

from services.api import BackendAPI


class ReportGenerator:
    """
    Handles generation of the AI Clinical Report
    from the backend.
    """

    @staticmethod
    def generate():
        """
        Generate the report once per session.

        Returns
        -------
        dict
            AI generated report.
        """

        # --------------------------------------------------
        # Already Generated
        # --------------------------------------------------

        if (
            "report" in st.session_state
            and st.session_state["report"]
        ):

            return st.session_state["report"]

        # --------------------------------------------------
        # Validate Session
        # --------------------------------------------------

        session_id = st.session_state.get("session_id")

        if not session_id:

            raise RuntimeError(
                "Session ID not found."
            )

        provider = st.session_state.get(
            "provider",
            "auto"
        )

        # --------------------------------------------------
        # Backend Call
        # --------------------------------------------------

        with st.spinner(
            "Generating AI Clinical Report..."
        ):

            response = BackendAPI.generate_report(

                session_id=session_id,

                provider=provider

            )

        report = response.get(
            "report",
            {}
        )

        used_provider = response.get(
            "provider",
            provider
        )

        # --------------------------------------------------
        # Cache
        # --------------------------------------------------

        st.session_state["report"] = report

        st.session_state["report_provider"] = used_provider

        st.session_state["report_stats"] = response.get(
            "stats",
            {}
        )

        st.session_state["report_reasoning"] = response.get(
            "reasoning",
            {}
        )

        return report