import streamlit as st
from contextlib import contextmanager


@contextmanager
def medical_loader(
    message: str = "Processing...",
    description: str = "Analyzing your uploaded medical reports. Please wait."
):
    """
    Professional loading card and progress indicator.

    Example
    -------
    with medical_loader("Uploading medical reports..."):
        upload_reports()
    """

    placeholder = st.empty()

    with placeholder.container():
        st.markdown(
            f"""
            <style>
                .report-loading-overlay {{
                    position: fixed;
                    inset: 0;
                    width: 100vw;
                    height: 100vh;
                    background: rgba(8, 15, 34, 0.88);
                    backdrop-filter: blur(4px);
                    z-index: 2147483647;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    pointer-events: all;
                }}
                .report-loading-overlay * {{
                    pointer-events: none;
                }}
                .report-loading-card {{
                    width: min(92%, 520px);
                    background: rgba(15, 23, 42, 0.98);
                    border: 1px solid rgba(148, 163, 184, 0.16);
                    border-radius: 28px;
                    padding: 34px 32px;
                    box-shadow: 0 30px 80px rgba(0, 0, 0, 0.28);
                    text-align: center;
                }}
                .report-loading-spinner {{
                    margin: 0 auto 24px;
                    width: 72px;
                    height: 72px;
                    border: 8px solid rgba(255, 255, 255, 0.12);
                    border-top-color: #3b82f6;
                    border-radius: 50%;
                    animation: loading-spin 1s linear infinite;
                }}
                .report-loading-text {{
                    font-size: 18px;
                    color: #f8fafc;
                    margin-bottom: 8px;
                    font-weight: 700;
                }}
                .report-loading-subtext {{
                    font-size: 14px;
                    color: #94a3b8;
                    margin: 0;
                }}
                @keyframes loading-spin {{
                    0% {{ transform: rotate(0deg); }}
                    100% {{ transform: rotate(360deg); }}
                }}
            </style>
            <div class="report-loading-overlay">
                <div class="report-loading-card">
                    <div class="report-loading-spinner"></div>
                    <div class="report-loading-text">{message}</div>
                    <p class="report-loading-subtext">{description}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        progress = st.progress(0)

    try:
        progress.progress(15)
        yield
        progress.progress(100)
    finally:
        placeholder.empty()
