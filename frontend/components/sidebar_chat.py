import streamlit as st

from services.api import BackendAPI
from components.loader import medical_loader


def render_chat_sidebar():

    with st.sidebar:

        # ==================================================
        # Patient
        # ==================================================

        st.markdown("### 👤 Current Patient")

        patient_name = st.session_state.get(
            "patient_name",
            "N/A"
        )

        if patient_name and patient_name != "N/A":
            patient_name = patient_name.strip().capitalize()

        age = st.session_state.get("patient_age")
        gender = st.session_state.get("patient_gender")

        details = []

        if age is not None:
            details.append(f"{age} Years")

        if gender:
            details.append(gender)

        detail_badges = "".join(

            [
                f"<span style='display:inline-flex;"
                f"align-items:center;"
                f"justify-content:center;"
                f"background:rgba(59,130,246,0.18);"
                f"color:#60A5FA;"
                f"border-radius:999px;"
                f"padding:6px 14px;"
                f"font-size:12px;"
                f"font-weight:600;"
                f"margin:4px 4px 0 0;'>"
                f"{item}</span>"

                for item in details
            ]

        )

        st.markdown(
            f"""
<div style='background:rgba(15,23,42,0.95);
padding:22px;
border-radius:28px;
border:1px solid rgba(148,163,184,0.14);
text-align:center;'>

<div style='font-size:22px;
font-weight:800;
color:#f8fafc;
margin-bottom:10px;'>

{patient_name}

</div>

<div style='color:#94a3b8;
font-size:13px;
margin-bottom:10px;'>

Patient Details

</div>

<div style='display:flex;
flex-wrap:wrap;
justify-content:center;
gap:8px;'>

{detail_badges}

</div>

</div>
""",
            unsafe_allow_html=True,
        )

        st.divider()

        # ==================================================
        # Uploaded Reports
        # ==========================================================

        st.markdown("### 📄 Uploaded Reports")

        uploaded_files = st.session_state.get(
            "uploaded_files",
            []
        )

        if uploaded_files:

            for file in uploaded_files:

                st.markdown(
                    f"""
<div style='display:flex;
align-items:center;
gap:10px;
padding:10px 0;
border-bottom:1px solid rgba(148,163,184,0.12);'>

<span style='font-size:16px;'>📄</span>

<span style='color:#f8fafc;
font-size:14px;'>

{file.name}

</span>

</div>
""",
                    unsafe_allow_html=True,
                )

        else:

            st.markdown(
                """
<div style='background:rgba(15,23,42,0.95);
padding:18px;
border-radius:24px;
border:1px solid rgba(148,163,184,0.14);
text-align:center;
color:#94a3b8;'>

No reports uploaded.

</div>
""",
                unsafe_allow_html=True,
            )

        st.divider()

        # ==================================================
        # Session Status
        # ==================================================

        st.markdown(
            """
<div style='background:#06202d;
padding:14px;
border-radius:16px;
border:1px solid rgba(16,185,129,0.18);
display:flex;
align-items:center;
justify-content:space-between;
color:#bef264;'>

<span>🟢 Active Session</span>

<span style='font-size:14px;
color:#d9f99d;'>

Live

</span>

</div>
""",
            unsafe_allow_html=True,
        )

        st.divider()

        # ==================================================
        # Generate Report
        # ==========================================================

        st.markdown("### 📋 Consultation Report")

        if st.button(
            "📄 Generate Final Report",
            use_container_width=True,
            type="primary"
        ):

            # Always use automatic failover
            provider = "auto"

            print("\n" + "=" * 60)
            print("FRONTEND REPORT REQUEST")
            print(f"Provider = {provider}")
            print("=" * 60)

            with medical_loader(
                message="Generating AI Clinical Report...",
                description="Analyzing uploaded medical reports and conversation history."
            ):

                response = BackendAPI.generate_report(
                    session_id=st.session_state["session_id"],
                    provider=provider
                )

                print("\n========== FRONTEND REPORT RESPONSE ==========")
                print(response)
                print("=============================================\n")

                st.session_state["report"] = response["report"]

                st.session_state["report_provider"] = response.get(
                    "provider",
                    provider
                )

                st.session_state["report_stats"] = response.get(
                    "stats",
                    {}
                )

                st.session_state["report_reasoning"] = response.get(
                    "reasoning",
                    {}
                )

            st.switch_page("pages/3_Report.py")

        st.divider()

        # ==================================================
        # Footer
        # ==========================================================

        st.markdown(
            """
<div style='color:#94a3b8;
font-size:12px;
padding-top:12px;'>

MedIntel AI • Version 2.0

</div>
""",
            unsafe_allow_html=True,
        )
