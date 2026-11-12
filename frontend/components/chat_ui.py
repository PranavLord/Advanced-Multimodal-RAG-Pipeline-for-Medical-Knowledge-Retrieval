import streamlit as st

from services.api import BackendAPI


def get_provider_badge(provider: str):

    provider = (provider or "unknown").lower()

    if provider == "gemini":

        return """
<div style="text-align:right;">
<span style="
background:#e8f5e9;
color:#2e7d32;
padding:3px 10px;
border-radius:12px;
font-size:11px;
font-weight:600;">
🟢 Powered by Gemini
</span>
</div>
"""

    elif provider == "groq":

        return """
<div style="text-align:right;">
<span style="
background:#fff3e0;
color:#ef6c00;
padding:3px 10px;
border-radius:12px;
font-size:11px;
font-weight:600;">
🟠 Powered by Groq
</span>
</div>
"""

    elif provider == "cohere":

        return """
<div style="text-align:right;">
<span style="
background:#ede7f6;
color:#5e35b1;
padding:3px 10px;
border-radius:12px;
font-size:11px;
font-weight:600;">
🟣 Powered by Cohere
</span>
</div>
"""

    elif provider == "openrouter":

        return """
<div style="text-align:right;">
<span style="
background:#e3f2fd;
color:#1565c0;
padding:3px 10px;
border-radius:12px;
font-size:11px;
font-weight:600;">
🔵 Powered by OpenRouter
</span>
</div>
"""

    return """
<div style="text-align:right;">
<span style="
background:#eeeeee;
color:#616161;
padding:3px 10px;
border-radius:12px;
font-size:11px;
font-weight:600;">
⚪ Provider Unknown
</span>
</div>
"""


def render_chat_ui():

    # ==========================================================
    # Initialize Chat History
    # ==========================================================

    if "messages" not in st.session_state:

        st.session_state.messages = []

    # ==========================================================
    # Welcome Message
    # ==========================================================

    if len(st.session_state.messages) == 0:

        user_name = st.session_state.get(
            "patient_name",
            "Patient"
        )

        display_name = user_name.strip().title() or "Patient"

        st.info(
            f"""
### 👋 Welcome to MedIntel AI, **{display_name}**

Your uploaded medical reports are ready for analysis.

You can ask questions about diagnoses, medications,
laboratory results, clinical findings, treatment plans,
or anything contained within the uploaded reports.

**AI Features**

- ✅ Multi-document Analysis
- ✅ Conversation Memory
- ✅ Evidence Mapping
- ✅ Query Rewriting
- ✅ Cross-document Reasoning

Start by typing your first question below.
"""
        )

    # ==========================================================
    # Display Conversation
    # ==========================================================

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            if message["role"] == "assistant":

                st.markdown(

                    get_provider_badge(

                        message.get("provider")

                    ),

                    unsafe_allow_html=True

                )

    # ==========================================================
    # Chat Input
    # ==========================================================

    prompt = st.chat_input(

        "Ask a question about the uploaded medical reports..."

    )

    if prompt:

        # ======================================================
        # User Message
        # ======================================================

        st.session_state.messages.append(

            {

                "role": "user",

                "content": prompt

            }

        )

        with st.chat_message("user"):

            st.markdown(prompt)

        # ======================================================
        # Assistant
        # ======================================================

        with st.chat_message("assistant"):

            placeholder = st.empty()

            placeholder.markdown(

                "💬 **Medi is typing...**"

            )

            try:

                response = BackendAPI.chat(

                    question=prompt,

                    session_id=st.session_state.session_id,

                    provider=st.session_state.get(

                        "provider",

                        "auto"

                    )

                )

                answer = response["answer"]

                provider = response.get(

                    "provider",

                    "unknown"

                )

            except Exception as e:

                answer = (

                    f"❌ Error communicating with backend.\n\n{e}"

                )

                provider = "unknown"

            placeholder.markdown(answer)

            st.markdown(

                get_provider_badge(provider),

                unsafe_allow_html=True

            )

        # ======================================================
        # Save Assistant Message
        # ======================================================

        st.session_state.messages.append(

            {

                "role": "assistant",

                "content": answer,

                "provider": provider

            }

        )

        st.rerun()