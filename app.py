import streamlit as st
from customer_agent import handle_ticket


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="TechFlow Customer Support",
    page_icon="💬",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("💬 TechFlow Customer Support")

st.caption(
    "Customer Support Agent with persistent customer memory"
)


# ============================================================
# SIDEBAR - CUSTOMER
# ============================================================

st.sidebar.header("👤 Customer")

customer_id = st.sidebar.text_input(
    "Customer ID",
    value="AcmeCorp"
)


st.sidebar.markdown("---")


# ============================================================
# CLEAR CHAT SESSION
# ============================================================

st.sidebar.subheader("🔄 Support Session")

st.sidebar.caption(
    "Start a new support session while keeping "
    "the customer's persistent Hindsight memory."
)


if st.sidebar.button(
    "🧹 Clear Chat Session",
    use_container_width=True
):

    # Clear ONLY the current conversation.
    # Hindsight customer memory is NOT deleted.

    st.session_state.messages = []

    st.session_state.pop(
        "last_result",
        None
    )

    st.rerun()


st.sidebar.success(
    "💾 Persistent customer memory is preserved.\n\n"
    "Clearing this chat does NOT delete Hindsight memory."
)


# ============================================================
# CURRENT CHAT
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# Display existing conversation

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# CUSTOMER MESSAGE
# ============================================================

prompt = st.chat_input(
    "Describe your product issue..."
)


if prompt:

    # --------------------------------------------------------
    # Show customer message
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)


    # --------------------------------------------------------
    # Generate support response
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "Checking customer history..."
        ):

            result = handle_ticket(
                customer_id,
                prompt
            )


        st.markdown(
            result["reply"]
        )


    # --------------------------------------------------------
    # Save assistant response to current chat
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": result["reply"]
        }
    )


    # --------------------------------------------------------
    # Save latest Hindsight recall result
    # --------------------------------------------------------

    st.session_state.last_result = result


# ============================================================
# HINDSIGHT MEMORY INSPECTOR
# ============================================================

st.markdown("---")

st.subheader(
    "🧠 Hindsight Customer Memory"
)

st.caption(
    "Previously stored customer support information "
    "recalled from persistent memory."
)


if "last_result" in st.session_state:

    memory = st.session_state.last_result[
        "recalled_memory"
    ]


    if memory == "NO PREVIOUS SUPPORT HISTORY EXISTS.":

        st.info(
            "No previous support history found."
        )

    else:

        st.success(
            "Previous customer support history recalled."
        )

        st.write(
            memory
        )

else:

    st.info(
        "Send a support message to retrieve "
        "customer history."
    )


# ============================================================
# HOW THE MEMORY DEMO WORKS
# ============================================================

with st.expander(
    "ℹ️ How persistent customer memory works"
):

    st.markdown(
        """
### Persistent Customer Memory Demo

**1. Customer reports a problem**

The Customer Support Agent handles the issue.

**2. Hindsight stores useful information**

Relevant factual information from the interaction is
retained as persistent customer memory.

**3. Clear Chat Session**

The current conversation disappears from the interface.

**4. Customer returns**

The same Customer ID can be used for the next support session.

**5. Hindsight recalls previous support history**

The agent can use relevant information from the previous
interaction without requiring the customer to repeat the
same details.

---

### Important

**Clear Chat Session does NOT delete Hindsight memory.**

It only clears the current conversation displayed in
this application.
"""
    )