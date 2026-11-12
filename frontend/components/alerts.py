import streamlit as st


def success(message: str):
    """Display a success alert."""

    st.markdown(
        f"""
        <div style="
            background: #14532D;
            border-left: 6px solid #22C55E;
            color: white;
            padding: 16px;
            border-radius: 12px;
            margin-bottom: 15px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.20);
        ">
            <strong>✅ Success</strong><br>
            {message}
        </div>
        """,
        unsafe_allow_html=True,
    )


def error(message: str):
    """Display an error alert."""

    st.markdown(
        f"""
        <div style="
            background: #7F1D1D;
            border-left: 6px solid #EF4444;
            color: white;
            padding: 16px;
            border-radius: 12px;
            margin-bottom: 15px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.20);
        ">
            <strong>❌ Error</strong><br>
            {message}
        </div>
        """,
        unsafe_allow_html=True,
    )


def warning(message: str):
    """Display a warning alert."""

    st.markdown(
        f"""
        <div style="
            background: #78350F;
            border-left: 6px solid #F59E0B;
            color: white;
            padding: 16px;
            border-radius: 12px;
            margin-bottom: 15px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.20);
        ">
            <strong>⚠ Warning</strong><br>
            {message}
        </div>
        """,
        unsafe_allow_html=True,
    )


def info(message: str):
    """Display an information alert."""

    st.markdown(
        f"""
        <div style="
            background: #1E3A8A;
            border-left: 6px solid #3B82F6;
            color: white;
            padding: 16px;
            border-radius: 12px;
            margin-bottom: 15px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.20);
        ">
            <strong>ℹ Information</strong><br>
            {message}
        </div>
        """,
        unsafe_allow_html=True,
    )
