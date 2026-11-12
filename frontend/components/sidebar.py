import streamlit as st


def render_sidebar():
    with st.sidebar:
        st.markdown("# 🩺 MedIntel AI")
        st.caption("AI-powered Clinical Decision Support System")
        st.divider()

        st.markdown("## 🚀 Features")

        features = [
            "📄 Upload Medical Reports",
            "🧠 AI Medical Analysis",
            "💊 Medication Intelligence",
            "📚 Evidence-based Explanations",
            "📥 Consultation Report Download",
        ]

        for feature in features:
            st.markdown(f"✅ {feature}")

        st.divider()

        st.markdown("## 🔒 Privacy")
        st.success("All uploaded medical reports remain private during your session.")
        st.divider()

        st.caption("MedIntel AI • Version 2.0")
