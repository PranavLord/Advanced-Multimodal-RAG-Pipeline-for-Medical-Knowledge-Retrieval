import streamlit as st


def page_footer():
    """Displays a consistent footer across all pages."""

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
        <hr>
        <div class="footer">
            🩺 MedIntel AI • Medical Knowledge Retrieval System
        </div>
        """,
        unsafe_allow_html=True,
    )
