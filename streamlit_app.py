
import streamlit as st
from google import genai
from google.genai import types

# Page settings
st.set_page_config(
    page_title="MedBot",
    page_icon="🩺",
    layout="centered"
)

# Medical assistant instructions
SYSTEM_PROMPT = """
You are MedBot, an educational medical assistant specialized ONLY
in Type 2 Diabetes Mellitus.

Your tasks:
- Explain Type 2 Diabetes in simple Arabic or English.
- Answer questions about definition, causes, risk factors,
  symptoms, diagnosis, complications, prevention and treatment.
- Explain medical terms in a student-friendly way.
- Use reliable medical organizations such as WHO, CDC, NIDDK
  and the American Diabetes Association as reference sources.
- Mention sources when possible. Never invent references.
- If you are uncertain, say so clearly.
- Do not diagnose users or prescribe medicines or doses.
- Do not replace a doctor or medical professional.
- If asked about an unrelated topic, politely explain
  that MedBot specializes in Type 2 Diabetes.
- Answer in the same language used by the user.
"""

# Title
st.title("🩺 MedBot")
st.subheader("AI Medical Educational Assistant")
st.markdown("### Type 2 Diabetes Specialist")

st.info(
    "MedBot is an educational project designed to explain "
    "Type 2 Diabetes. It does not provide diagnosis or replace doctors."
)

# API key
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error(
        "The Gemini API key has not been added yet. "
        "We will add it in Streamlit Secrets in a later step."
    )
    st.stop()

# Connect to Gemini
client = genai.Client(api_key=api_key)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Suggested questions
with st.sidebar:
    st.header("About MedBot")
    st.write("An AI assistant specialized in Type 2 Diabetes.")

    st.subheader("Suggested Questions")
    st.write("1. What is Type 2 Diabetes?")
    st.write("2. What are its symptoms?")
    st.write("3. What causes Type 2 Diabetes?")
    st.write("4. How is it diagnosed?")
    st.write("5. What are its complications?")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_question = st.chat_input(
    "Ask MedBot about Type 2 Diabetes..."
)

if user_question:
    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        with st.spinner("MedBot is preparing an answer..."):
            try:
                history = []

                for message in st.session_state.messages[:-1]:
                    role = (
                        "user" if message["role"] == "user"
                        else "model"
                    )
                    history.append(
                        types.Content(
                            role=role,
                            parts=[types.Part(text=message["content"])]
                        )
                    )

                chat = client.chats.create(
                    model="gemini-3.8-flash",
                    history=history,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.3,
                        max_output_tokens=1000
                    )
                )

                response = chat.send_message(
                    message=user_question
                )

                answer = response.text or (
                    "Sorry, I could not prepare an answer."
                )

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as error:
                st.error(
                    "Something went wrong. Please check the "
                    "API settings and try again."
                )
