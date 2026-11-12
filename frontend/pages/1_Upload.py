import streamlit as st
import requests

from components.header import page_header
from components.card import medical_card
from components.sidebar import render_sidebar
from services.api import BackendAPI


def show_centered_loader(message: str = "Processing medical reports..."):
    loader = st.empty()
    loader.markdown(
        f"""
        <style>
            .loading-overlay {{
                position: fixed;
                inset: 0;
                width: 100vw;
                height: 100vh;
                background: rgba(15, 23, 42, 0.92);
                backdrop-filter: blur(4px);
                z-index: 2147483647;
                display: flex;
                align-items: center;
                justify-content: center;
                pointer-events: all;
            }}
            .loading-overlay * {{
                pointer-events: none;
            }}
            .loading-card {{
                width: min(92%, 520px);
                background: rgba(15, 23, 42, 0.98);
                border: 1px solid rgba(148, 163, 184, 0.16);
                border-radius: 28px;
                padding: 34px 32px;
                box-shadow: 0 30px 80px rgba(0, 0, 0, 0.28);
                text-align: center;
            }}
            .loading-spinner {{
                margin: 0 auto 24px;
                width: 72px;
                height: 72px;
                border: 8px solid rgba(255, 255, 255, 0.12);
                border-top-color: #3b82f6;
                border-radius: 50%;
                animation: loading-spin 1s linear infinite;
            }}
            .loading-text {{
                font-size: 18px;
                color: #f8fafc;
                margin-bottom: 8px;
                font-weight: 700;
            }}
            .loading-subtext {{
                font-size: 14px;
                color: #94a3b8;
                margin: 0;
            }}
            @keyframes loading-spin {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
        </style>
        <div class="loading-overlay">
            <div class="loading-card">
                <div class="loading-spinner"></div>
                <div class="loading-text">{message}</div>
                <p class="loading-subtext">This may take a few seconds depending on report size.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return loader

# ==========================================================
# Page Configuration
# ==========================================================
st.set_page_config(
    page_title="MedIntel AI",
    page_icon="🩺",
    layout="wide",
)

with open("assets/styles.css") as css:
    st.markdown(
        f"<style>{css.read()}</style>",
        unsafe_allow_html=True,
    )

# ==========================================================
# Session State
# ==========================================================
if "patient_name" not in st.session_state:
    st.session_state.patient_name = ""

if "patient_age" not in st.session_state:
    st.session_state.patient_age = None

if "patient_gender" not in st.session_state:
    st.session_state.patient_gender = "Prefer not to say"

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

# ---------------- NEW ----------------
if "session_id" not in st.session_state:
    st.session_state.session_id = None

# ==========================================================
# Sidebar
# ==========================================================
render_sidebar()

# ==========================================================
# Header
# ==========================================================
page_header(
    "Upload Medical Reports",
    "Upload one or more clinical reports for automatic AI analysis and insights.",
)

# ==========================================================
# Patient Information
# ==========================================================
with medical_card("👤 Patient Information"):
    patient_name = st.text_input(
        "Full Name *",
        value=st.session_state.patient_name,
        placeholder="Enter patient's full name",
    )

    col1, col2 = st.columns(2)

    with col1:
        patient_age = st.number_input(
            "Age",
            min_value=0,
            max_value=120,
            value=None,
            placeholder="Optional",
        )

    with col2:
        patient_gender = st.selectbox(
            "Gender",
            [
                "Male",
                "Female",
                "Other",
                "Prefer not to say",
            ],
            index=3,
        )

# ==========================================================
# Upload Reports
# ==========================================================
with medical_card("📂 Upload Medical Reports"):
    st.info("Upload one or more medical reports in PDF format.")

    uploaded_files = st.file_uploader(
        "Choose PDF Reports",
        type=["pdf"],
        accept_multiple_files=True,
        help="",
    )

    st.caption("PDF format • One or more medical reports")

    if uploaded_files:
        st.markdown("---")
        st.success(f"✅ {len(uploaded_files)} medical report(s) selected.")

        for file in uploaded_files:
            st.markdown(f"📄 **{file.name}**")

# ==========================================================
# Continue Button
# ==========================================================
st.markdown("<br>", unsafe_allow_html=True)

continue_clicked = st.button(
    "🚀 Continue to AI Analysis",
    use_container_width=True,
)

if continue_clicked:
    # ------------------------------------------------------
    # Validate Patient Name
    # ------------------------------------------------------
    if patient_name.strip() == "":
        st.toast(
            "Please enter the patient's name.",
            icon="⚠️",
        )
        st.stop()

    # ------------------------------------------------------
    # Validate Uploaded Files
    # ------------------------------------------------------
    if not uploaded_files:
        st.toast(
            "Please upload at least one PDF report.",
            icon="⚠️",
        )
        st.stop()

    # ------------------------------------------------------
    # Upload Reports
    # ------------------------------------------------------
    try:
        loader = show_centered_loader("🩺 Processing medical reports...")
        response = BackendAPI.upload_reports(uploaded_files)
        loader.empty()

        # --------------------------------------------------
        # Save Session
        # --------------------------------------------------
        st.session_state.patient_name = patient_name
        st.session_state.patient_age = patient_age
        st.session_state.patient_gender = patient_gender
        st.session_state.uploaded_files = uploaded_files
        st.session_state.upload_response = response
        st.session_state.session_id = response["session_id"]

        st.toast(
            "Reports uploaded successfully!",
            icon="🎉",
        )

        st.switch_page("pages/2_Chat.py")

    # ------------------------------------------------------
    # Backend Validation Errors
    # ------------------------------------------------------
    except requests.exceptions.HTTPError:
        st.toast(
            "Unable to process the uploaded report. Please upload a valid medical PDF.",
            icon="⚠️",
        )
        st.stop()

    # ------------------------------------------------------
    # Unexpected Errors
    # ------------------------------------------------------
    except Exception as e:
        print(e)
        st.toast(
            "Something went wrong while processing the uploaded report. Please try again.",
            icon="❌",
        )
        st.stop()
