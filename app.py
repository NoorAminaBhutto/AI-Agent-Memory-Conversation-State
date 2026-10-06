import json
from pathlib import Path
import streamlit as st

APP_TITLE = "AI Agent Memory & Conversation State"
MEMORY_FILE = Path("memory.json")

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🧠",
    layout="wide"
)


def load_long_term_memory():
    if MEMORY_FILE.exists():
        try:
            return json.loads(
                MEMORY_FILE.read_text(encoding="utf-8")
            )
        except Exception:
            return []
    return []


def save_long_term_memory(items):
    MEMORY_FILE.write_text(
        json.dumps(items, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def assistant_reply(message, history, memories):
    text = message.lower().strip()

    if any(
        phrase in text
        for phrase in [
            "what do you remember",
            "remember about me",
            "my memory"
        ]
    ):
        if not memories:
            return "I don't have any saved long-term memories yet."

        return (
            "Here is what I remember: "
            + "; ".join(
                f"{m['key']} = {m['value']}"
                for m in memories
            )
            + "."
        )

    if "hello" in text or text == "hi":
        return (
            "Hello! I can remember this conversation "
            "and selected information saved for later."
        )

    if (
        "what did i say" in text
        or "earlier" in text
        or "previous" in text
    ):
        recent = [
            m["content"]
            for m in history[-6:]
            if m["role"] == "user"
        ]

        if not recent:
            return (
                "There is no earlier conversation "
                "in this session yet."
            )

        return (
            "In this session, you recently said: "
            + " | ".join(recent[-3:])
        )

    if memories:
        details = ", ".join(
            f"{m['key']}: {m['value']}"
            for m in memories
        )

        return (
            "I can help with that. "
            "I also have these approved long-term "
            f"details available: {details}."
        )

    return (
        "I can help with your request. "
        "Short-term conversation memory is active. "
        "You can save selected information to "
        "long-term memory using the panel."
    )


if "messages" not in st.session_state:
    st.session_state.messages = []

if "long_term" not in st.session_state:
    st.session_state.long_term = load_long_term_memory()


st.title("🧠 AI Agent Memory & Conversation State")

st.caption(
    "Day 20 — Short-term conversation memory "
    "+ selected long-term user memory"
)


with st.sidebar:

    st.header("🧠 Memory Controls")

    st.write(
        "**Short-term memory:** "
        "Current conversation stored in the active session."
    )

    st.write(
        "**Long-term memory:** "
        "Selected information saved in memory.json."
    )

    st.divider()

    st.subheader("💾 Save User Information")

    key = st.text_input(
        "Memory Category",
        placeholder="preference / goal / project"
    )

    value = st.text_input(
        "Memory Value",
        placeholder="Prefers concise answers"
    )

    if st.button(
        "💾 Save to Long-term Memory",
        use_container_width=True
    ):

        if key.strip() and value.strip():

            st.session_state.long_term.append(
                {
                    "key": key.strip(),
                    "value": value.strip()
                }
            )

            save_long_term_memory(
                st.session_state.long_term
            )

            st.success("Memory saved successfully.")

        else:
            st.warning(
                "Please enter both category and value."
            )


    st.subheader("📚 Saved Memory")

    if st.session_state.long_term:

        for i, item in enumerate(
            st.session_state.long_term
        ):

            c1, c2 = st.columns([5, 1])

            c1.write(
                f"**{item['key']}**: {item['value']}"
            )

            if c2.button(
                "×",
                key=f"delete_{i}"
            ):

                st.session_state.long_term.pop(i)

                save_long_term_memory(
                    st.session_state.long_term
                )

                st.rerun()

    else:
        st.info(
            "No long-term memories saved yet."
        )


    if st.button(
        "🗑️ Clear Short-term Conversation",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


    if st.button(
        "⚠️ Clear Long-term Memory",
        use_container_width=True
    ):

        st.session_state.long_term = []

        save_long_term_memory([])

        st.rerun()


st.subheader("💬 Conversation")


for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


prompt = st.chat_input(
    "Type a message..."
)


if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    reply = assistant_reply(
        prompt,
        st.session_state.messages[:-1],
        st.session_state.long_term
    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": reply
        }
    )

    st.rerun()


st.divider()


col1, col2, col3 = st.columns(3)

col1.metric(
    "Current-session messages",
    len(st.session_state.messages)
)

col2.metric(
    "Saved long-term memories",
    len(st.session_state.long_term)
)

col3.metric(
    "Memory layers",
    "2"
)


with st.expander(
    "📋 Assignment Demonstration Flow"
):

    st.markdown(
        """
        **1. Short-term memory**

        Send multiple messages and ask what you said earlier.

        **2. Long-term memory**

        Save an approved fact such as:

        `goal = Build practical AI applications`

        **3. Memory recall**

        Ask:

        `What do you remember about me?`

        **4. User control**

        Review, delete, or clear saved memories.

        **5. Key difference**

        Short-term memory supports the current conversation,
        while long-term memory stores selected useful information
        for later use.
        """
    )
