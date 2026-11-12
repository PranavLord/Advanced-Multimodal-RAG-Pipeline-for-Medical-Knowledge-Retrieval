import streamlit as st


def page_header(title: str, subtitle: str):
    html = """
    <div class="hero">
        <h1>{title}</h1>
        <p class="subtitle">{subtitle}</p>
    </div>
    """

    html = html.format(title=title, subtitle=subtitle)
    st.markdown(html, unsafe_allow_html=True)
    st.divider()
