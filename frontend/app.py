import streamlit as st

# ==========================================================
# Page Configuration
# ==========================================================
st.set_page_config(
    page_title="MedIntel AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==========================================================
# Load CSS
# ==========================================================
with open("assets/styles.css") as css:
    st.markdown(
        f"<style>{css.read()}</style>",
        unsafe_allow_html=True,
    )

# ==========================================================
# Hero Section
# ==========================================================
st.markdown(
    """
    <div class="hero">
        <h1>🩺 MedIntel AI</h1>
        <p class="subtitle">
            AI-powered Medical Report Analysis & Clinical Insights
        </p>
        <p>Analyze • Understand • Explain • Assist</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# ==========================================================
# What MedIntel AI Can Analyze
# ==========================================================
st.markdown(
    """
    <div class="section-title">
        Trusted AI for Medical Document Analysis
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:
    st.success("📄 Blood Reports")
    st.success("🧪 Laboratory Reports")
    st.success("💊 Prescriptions")
    st.success("📑 Discharge Summary")

with col2:
    st.success("🩻 MRI")
    st.success("🖥 CT Scan")
    st.success("🩺 X-Ray")
    st.success("📋 Clinical Reports")

st.write("")
st.write("")

# ==========================================================
# Features
# ==========================================================
st.markdown(
    """
    <div class="section-title">
        Why Choose MedIntel AI?
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="card">
            <h3>📄 Report Analysis</h3>
            <p>Extracts and explains findings from medical reports in patient-friendly language.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="card">
            <h3>💊 Medication Intelligence</h3>
            <p>Explains medicines, their purpose, side effects, precautions and educational alternatives.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="card">
            <h3>🧠 Clinical Insights</h3>
            <p>Provides evidence-based explanations using both uploaded reports and medical knowledge.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")
st.write("")
st.write("")

# ==========================================================
# Call To Action
# ==========================================================
left, center, right = st.columns([1, 2, 1])

with center:
    if st.button("🚀 Begin Analysis"):
        st.switch_page("pages/1_Upload.py")
