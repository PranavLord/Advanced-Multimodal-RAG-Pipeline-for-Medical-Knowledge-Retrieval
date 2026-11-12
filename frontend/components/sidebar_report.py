import streamlit as st


def _build_fallback_report_stats(reasoning: dict | None = None) -> dict:
    reasoning = reasoning or {}
    uploaded_files = st.session_state.get("uploaded_files", [])
    messages = st.session_state.get("messages", [])
    documents = reasoning.get("documents", [])

    return {
        "uploaded_documents": len(uploaded_files),
        "documents_used": len(documents) or len(uploaded_files),
        "retrieved_chunks": sum(doc.get("chunk_count", 0) for doc in documents),
        "evidence_chunks": sum(len(doc.get("evidence", [])) for doc in documents),
        "conversation_questions": len(
            [m for m in messages if m.get("role") == "user"]
        ),
        "overall_confidence": int((reasoning.get("highest_score", 0) or 0) * 100),
    }


def render_report_sidebar():

    with st.sidebar:

        # ==================================================
        # Patient
        # ==================================================

        st.markdown("### 👤 Current Patient")

        patient_name = st.session_state.get("patient_name", "N/A")

        # Always capitalize only the first letter
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
                f"<span style='display:inline-flex;align-items:center;justify-content:center;background:rgba(59,130,246,0.18);color:#60A5FA;border-radius:999px;padding:6px 14px;font-size:12px;font-weight:600;margin:4px 4px 0 0;'>"                 f"{item}</span>"
                for item in details
            ]
        )

        st.markdown(
            f"""
<div style='background:rgba(15,23,42,0.95);padding:22px;border-radius:28px;border:1px solid rgba(148,163,184,0.14);text-align:center;'>
    <div style='font-size:22px;font-weight:800;color:#f8fafc;letter-spacing:0.2px;margin-bottom:10px;'>{patient_name}</div>
    <div style='color:#94a3b8;font-size:13px;margin-bottom:10px;'>Patient details</div>
    <div style='display:flex;flex-wrap:wrap;justify-content:center;gap:8px;'>
        {detail_badges}
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.divider()

        stats = st.session_state.get("report_stats", {})
        reasoning = st.session_state.get("report_reasoning", {})

        if not stats:
            print(
                "\n[REPORT SIDEBAR DEBUG] report_stats missing from session_state. "
                "Using fallback values."
            )
            stats = _build_fallback_report_stats(reasoning)

        if not reasoning:
            reasoning = {"documents": []}

        # ==================================================
        # AI Confidence
        # ==================================================

        st.markdown("### 📊 AI Confidence")

        confidence = stats.get("overall_confidence", 0)

        st.markdown(
            f"""
<div style='background:rgba(15,23,42,0.95);padding:20px;border-radius:26px;border:1px solid rgba(148,163,184,0.14);'>
    <div style='display:flex;align-items:center;justify-content:space-between;gap:12px;'>
        <div>
            <div style='font-size:32px;font-weight:800;color:#10B981;'>{confidence}%</div>
            <div style='color:#94a3b8;font-size:13px;margin-top:6px;'>High confidence in analysis</div>
        </div>
        <div style='width:56px;height:56px;border-radius:50%;background:rgba(16,185,129,0.16);display:flex;align-items:center;justify-content:center;'>
            <span style='font-size:22px;'>✔️</span>
        </div>
    </div>
    <div style='margin-top:16px;height:10px;background:rgba(148,163,184,0.22);border-radius:999px;overflow:hidden;'>
        <div style='width:{confidence}%;height:100%;background:linear-gradient(90deg,#22c55e,#06b6d4);'></div>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.divider()

        # ==================================================
        # Conversation
        # ==================================================

        st.markdown("### 💬 Conversation")

        questions = stats.get(
            "conversation_questions",
            len(
                [
                    m
                    for m in st.session_state.get(
                        "messages",
                        []
                    )
                    if m.get("role") == "user"
                ]
            )
        )

        st.markdown(
            f"""
<div style='background:rgba(15,23,42,0.95);padding:20px;border-radius:26px;border:1px solid rgba(148,163,184,0.14);text-align:center;'>
    <div style='font-size:14px;color:#94a3b8;margin-bottom:12px;'>Questions Asked</div>
    <div style='font-size:36px;font-weight:800;color:#f8fafc;'>{questions}</div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.divider()

        # ==================================================
        # Uploaded Reports
        # ==================================================

        st.markdown("### 📄 Documents")

        uploaded_files = st.session_state.get(
            "uploaded_files",
            []
        )

        uploaded_documents = stats.get("uploaded_documents", len(uploaded_files))
        documents_used = stats.get("documents_used", len(uploaded_files))

        st.markdown(
            f"""
<div style='display:grid;grid-template-columns:1fr 1fr;gap:12px;'>
    <div style='background:rgba(15,23,42,0.95);padding:18px;border-radius:24px;border:1px solid rgba(148,163,184,0.14);text-align:center;'>
        <div style='font-size:12px;color:#94a3b8;text-transform:uppercase;letter-spacing:0.12em;'>Uploaded</div>
        <div style='font-size:32px;font-weight:800;color:#f8fafc;margin-top:10px;'>{uploaded_documents}</div>
    </div>
    <div style='background:rgba(15,23,42,0.95);padding:18px;border-radius:24px;border:1px solid rgba(148,163,184,0.14);text-align:center;'>
        <div style='font-size:12px;color:#94a3b8;text-transform:uppercase;letter-spacing:0.12em;'>Used</div>
        <div style='font-size:32px;font-weight:800;color:#f8fafc;margin-top:10px;'>{documents_used}</div>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.divider()

        # ==================================================
        # Retrieval Stats
        # ==================================================

        st.markdown("### 🧠 Retrieval Chunks")

        retrieved_chunks = stats.get("retrieved_chunks", 0)
        evidence_chunks = stats.get("evidence_chunks", 0)

        st.markdown(
            f"""
<div style='display:grid;grid-template-columns:1fr 1fr;gap:12px;'>
    <div style='background:rgba(15,23,42,0.95);padding:18px;border-radius:24px;border:1px solid rgba(148,163,184,0.14);text-align:center;'>
        <div style='font-size:12px;color:#94a3b8;text-transform:uppercase;letter-spacing:0.12em;'>Retrieved Chunks</div>
        <div style='font-size:32px;font-weight:800;color:#f8fafc;margin-top:10px;'>{retrieved_chunks}</div>
    </div>
    <div style='background:rgba(15,23,42,0.95);padding:18px;border-radius:24px;border:1px solid rgba(148,163,184,0.14);text-align:center;'>
        <div style='font-size:12px;color:#94a3b8;text-transform:uppercase;letter-spacing:0.12em;'>Evidence Chunks</div>
        <div style='font-size:32px;font-weight:800;color:#f8fafc;margin-top:10px;'>{evidence_chunks}</div>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.divider()

        # ==================================================
        # Document Ranking
        # ==================================================

        st.markdown("### ⭐ Document Ranking")

        documents = reasoning.get("documents", [])

        if documents:

            for document in documents:

                score = int(round(document.get("score", 0) * 100))
                importance = document.get("importance", "Unknown")

                st.markdown(
                    f"""
<div style='background:rgba(15,23,42,0.95);padding:16px;border-radius:24px;border:1px solid rgba(148,163,184,0.14);margin-bottom:12px;'>
    <div style='display:flex;align-items:center;justify-content:space-between;gap:12px;'>
        <div>
            <div style='font-size:15px;font-weight:700;color:#f8fafc;margin-bottom:4px;'>{document.get("document", "Unknown Document")}</div>
            <div style='font-size:12px;color:#94a3b8;text-transform:uppercase;letter-spacing:0.12em;'>{importance}</div>
        </div>
        <div style='width:44px;height:44px;border-radius:50%;background:rgba(59,130,246,0.16);display:flex;align-items:center;justify-content:center;color:#7DD3FC;font-size:18px;'>
            ⭐
        </div>
    </div>
    <div style='margin-top:14px;height:10px;background:rgba(148,163,184,0.18);border-radius:999px;overflow:hidden;'>
        <div style='width:{score}%;height:100%;background:linear-gradient(90deg,#3b82f6,#06b6d4);'></div>
    </div>
    <div style='margin-top:10px;font-size:12px;color:#94a3b8;'>{score}% relevance</div>
</div>
""",
                    unsafe_allow_html=True,
                )

        else:

            st.info(
                "No ranking data available yet. Check the report response for reasoning documents."
            )

        st.divider()
