import json
import streamlit as st

from services.api import BackendAPI

from components.sidebar_report import render_report_sidebar

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Clinical Report",
    page_icon="📄",
    layout="wide"
)

# ==========================================================
# Load CSS
# ==========================================================

with open("assets/styles.css") as css:
    st.markdown(
        f"<style>{css.read()}</style>",
        unsafe_allow_html=True
    )

# ==========================================================
# Validate Session
# ==========================================================

if "session_id" not in st.session_state:

    st.error("No active medical session found.")

    if st.button("🏠 Return Home"):
        st.switch_page("app.py")

    st.stop()

# ==========================================================
# Sidebar
# ==========================================================

render_report_sidebar()

def _build_fallback_report_stats(reasoning_context: dict | None = None) -> dict:
    reasoning_context = reasoning_context or {}

    uploaded_files = st.session_state.get("uploaded_files", [])
    messages = st.session_state.get("messages", [])
    documents = reasoning_context.get("documents", [])

    return {
        "uploaded_documents": len(uploaded_files),
        "documents_used": len(documents) or len(uploaded_files),
        "retrieved_chunks": sum(
            doc.get("chunk_count", 0)
            for doc in documents
        ),
        "evidence_chunks": sum(
            len(doc.get("evidence", []))
            for doc in documents
        ),
        "conversation_questions": len(
            [
                message
                for message in messages
                if message.get("role") == "user"
            ]
        ),
        "overall_confidence": int(
            (reasoning_context.get("highest_score", 0) or 0) * 100
        )
    }

# ==========================================================
# Generate Report from Backend
# ==========================================================

if "report" not in st.session_state:

    with st.spinner("Generating AI Clinical Report..."):

        try:

            response = BackendAPI.generate_report(

                session_id=st.session_state["session_id"],

                provider=st.session_state.get(
                    "provider",
                    "auto"
                )

            )

            print("\n========== REPORT PAGE RESPONSE ==========")
            print(response)
            print("========================================\n")

            st.session_state["report"] = response["report"]

            st.session_state["report_provider"] = response.get(
                "provider",
                "unknown"
            )

            st.session_state["report_stats"] = response.get(
                "stats",
                {}
            )

            st.session_state["report_reasoning"] = response.get(
                "reasoning",
                {}
            )

        except Exception as e:

            st.error(f"Unable to generate report.\n\n{e}")

            st.stop()

report = st.session_state["report"]

stats = st.session_state.get(
    "report_stats",
    {}
)

reasoning = st.session_state.get(
    "report_reasoning",
    {}
)

if not stats:
    print(
        "\n[REPORT PAGE DEBUG] report_stats missing from session_state. "
        "Using fallback values."
    )
    stats = _build_fallback_report_stats(reasoning)

if not reasoning:
    reasoning = {
        "documents": []
    }

# ==========================================================
# Header
# ==========================================================

st.title("📄 AI Clinical Summary Report")

st.caption(
    "Comprehensive AI-generated clinical summary based on all uploaded medical reports."
)

provider_used = st.session_state.get(
    "report_provider",
    "unknown"
)

st.info(f"🤖 Report generated using **{provider_used.upper()}**")

st.markdown("---")

# ==========================================================
# Dashboard Metrics
# ==========================================================

documents_count = stats.get(
    "uploaded_documents",
    len(st.session_state.get("uploaded_files", []))
)

questions = stats.get(
    "conversation_questions",
    len(
        [
            m
            for m in st.session_state.get("messages", [])
            if m.get("role") == "user"
        ]
    )
)

confidence = stats.get(
    "overall_confidence",
    int(reasoning.get("highest_score", 0) * 100)
)

evidence = stats.get(
    "evidence_chunks",
    sum(
        len(doc.get("evidence", []))
        for doc in reasoning.get("documents", [])
    )
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "📄 Documents Analysed",
        documents_count
    )

with c2:
    st.metric(
        "💬 Questions Asked",
        questions
    )

with c3:
    st.metric(
        "🎯 AI Confidence",
        f"{confidence}%"
    )

with c4:
    st.metric(
        "📚 Evidence Coverage",
        f"{evidence} Chunks"
    )

st.markdown("---")

# ==========================================================
# Executive Summary
# ==========================================================

st.markdown(
    """
<div class="report-card">

<div class="report-title">
📋 Executive Summary
</div>
""",
    unsafe_allow_html=True,
)

st.write(
    report.get(
        "executive_summary",
        "Executive summary not available."
    )
)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# Clinical Findings
# ==========================================================

st.markdown(
    """
<div class="report-card">

<div class="report-title">
🩺 Clinical Findings
</div>
""",
    unsafe_allow_html=True,
)

findings = report.get(
    "clinical_findings",
    []
)

if findings:

    for finding in findings:

        severity = finding.get(
            "severity",
            "info"
        ).lower()

        text = finding.get(
            "text",
            ""
        )

        if severity == "high":
            st.error(text)

        elif severity == "medium":
            st.warning(text)

        elif severity == "low":
            st.success(text)

        else:
            st.info(text)

else:

    st.info("No clinical findings available.")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# Clinical Interpretation
# ==========================================================

st.markdown(
    """
<div class="report-card">

<div class="report-title">
🧠 Clinical Interpretation
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(

    report.get(

        "clinical_interpretation",

        "Clinical interpretation will appear here."

    ),

    unsafe_allow_html=True,

)

st.markdown(
    "</div>",
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# Cross Document Reasoning
# ==========================================================

st.markdown(
    """
<div class="report-card">

<div class="report-title">
🔗 Cross Document Reasoning
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(

    report.get(

        "cross_document_reasoning",

        "Cross-document reasoning will appear here."

    ),

    unsafe_allow_html=True,

)

st.markdown(
    "</div>",
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# Medication Intelligence
# ==========================================================

st.markdown(
    """
<div class="report-card">

<div class="report-title">
💊 Medication Intelligence
</div>
""",
    unsafe_allow_html=True,
)

medications = report.get(
    "medications",
    []
)

if medications:

    for medicine in medications:

        with st.expander(

            medicine.get(
                "name",
                "Medication"
            ),

            expanded=False

        ):

            st.markdown(
                f"**Purpose**  \n{medicine.get('purpose','Not available.')}"
            )

            st.markdown(
                f"**Side Effects**  \n{medicine.get('side_effects','Not available.')}"
            )

            st.markdown(
                f"**Recommendation**  \n{medicine.get('recommendation','Not available.')}"
            )

else:

    st.info("No medications identified.")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# AI Recommendations
# ==========================================================

st.markdown(
    """
<div class="report-card">

<div class="report-title">
✅ AI Recommendations
</div>
""",
    unsafe_allow_html=True,
)

recommendations = report.get(
    "recommendations",
    []
)

if recommendations:

    for recommendation in recommendations:

        st.success(recommendation)

else:

    st.info("No recommendations available.")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# Evidence Sources
# ==========================================================

st.markdown(
    """
<div class="report-card">
<div class="report-title">
📚 Evidence Sources
</div>
""",
    unsafe_allow_html=True,
)

documents = reasoning.get(
    "documents",
    []
)

if documents:

    for document in documents:

        st.markdown(
            f"""
<div style="
background:#0f172a;
padding:18px;
border-radius:14px;
border:1px solid rgba(148,163,184,.15);
margin-bottom:16px;
">

<div style="
display:flex;
justify-content:space-between;
align-items:center;
margin-bottom:10px;
">

<b style="font-size:16px;color:white;">
📄 {document.get('document', 'Unknown Document')}
</b>

<span style="
background:#2563eb22;
padding:6px 12px;
border-radius:999px;
font-size:12px;
color:#60A5FA;
">

{document.get('importance', 'Unknown')}

</span>

</div>

<b>Similarity Score:</b>
{document.get('score', 0):.4f}

<br>

<b>Average Score:</b>
{document.get('average_score', 0):.4f}

<br>

<b>Evidence Chunks:</b>
{document.get('chunk_count', 0)}

<br><br>

<b>Supporting Evidence</b>

<ul>
"""
            +
            "".join(
                [
                    f"<li>{chunk.get('text', '')[:180]}...</li>"
                    for chunk in document.get("evidence", [])
                ]
            )
            +
            """
</ul>

</div>
""",
            unsafe_allow_html=True,
        )

else:

    st.info(
        "No evidence sources available."
    )

st.markdown("</div>", unsafe_allow_html=True)

# ==========================================================
# Navigation
# ==========================================================

left, center, right = st.columns([1, 1, 1])

with left:

    if st.button(
        "💬 Ask More Questions",
        use_container_width=True,
    ):
        st.switch_page("pages/2_Chat.py")

with center:

    report_json = {
        "provider": provider_used,
        "report": report,
        "statistics": stats,
        "reasoning": reasoning
    }

    st.download_button(
        label="⬇️ Download Report",
        data=json.dumps(
            report_json,
            indent=4
        ),
        file_name="clinical_report.json",
        mime="application/json",
        use_container_width=True,
    )

with right:

    if st.button(
        "🏠 Exit Session",
        use_container_width=True,
    ):

        keys = list(st.session_state.keys())

        for key in keys:
            del st.session_state[key]

        st.switch_page("app.py")

# ==========================================================
# Disclaimer
# ==========================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    """
<div style="
background:#0f172a;
border:1px solid rgba(148,163,184,.18);
padding:14px 18px;
border-radius:16px;
font-size:13px;
color:#cbd5e1;
text-align:center;
">

⚠️ <b>Medical Disclaimer:</b>
This AI-generated report is for informational purposes only and should not replace professional medical advice, diagnosis, or treatment.

</div>
""",
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)