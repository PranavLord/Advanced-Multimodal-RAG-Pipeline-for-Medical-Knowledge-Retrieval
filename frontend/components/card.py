import streamlit as st
from contextlib import contextmanager


@contextmanager
def medical_card(title: str):
    """
    Reusable medical card component.

    Usage
    -----
    with medical_card("👤 Patient Information"):
        st.text_input(...)
    """

    st.markdown(
        f"""
        <div class="med-card">

        <div class="section-title">
            {title}
        </div>
        """,
        unsafe_allow_html=True,
    )

    yield

    st.markdown(
        """
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
