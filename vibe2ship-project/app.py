import streamlit as st
import os
from google import genai
from google.genai import types

st.set_page_config(
    page_title="The Last-Minute Life Saver",
    layout="centered",
    page_icon="⏰"
)

st.title("⏰ The Last-Minute Life Saver")
st.caption("An AI-powered active productivity companion built for Vibe2Ship.")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    with st.sidebar:
        st.subheader("Configuration")
        api_key = st.text_input("Enter your Gemini API Key:", type="password")
        if api_key:
            os.environ["GEMINI_API_KEY"] = api_key

if not api_key:
    st.info("Please provide your Gemini API key in the sidebar or set it as an Environment Variable to begin.", icon="🔑")
else:
    client = genai.Client()

    st.markdown("### Tell me what you need to do, when it's due, and your energy level:")
    raw_user_tasks = st.text_area(
        label="Raw Schedule Data",
        placeholder="Example: I have an exam tomorrow at 9 AM, an electricity bill due tonight, and I need to buy groceries. I am feeling exhausted right now.",
        height=150,
        label_visibility="collapsed"
    )

    if st.button("Generate Proactive Execution Plan", type="primary"):
        if raw_user_tasks.strip() == "":
            st.warning("Please dump your messy task list first!")
        else:
            with st.spinner("Analyzing priorities and structuring timeline..."):
                try:
                    system_instruction = (
                        "You are an elite, proactive AI Productivity Companion. Your job is to take chaotic, "
                        "stressed task dumps from users and return an un-ignorable, action-oriented plan. "
                        "1. Prioritize tasks intelligently (Urgent vs Important).\n"
                        "2. Break major hurdles into micro-steps that require minimal activation energy.\n"
                        "3. Design an exact timeline breakdown for today based on context.\n"
                        "4. End with a motivational, high-clarity recommendation."
                    )

                    response = client.models.generate_content(
                        model='gemini-2.0-flash',
                        contents=raw_user_tasks,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            temperature=0.3,
                        )
                    )

                    st.success("Plan Formulated!")
                    st.markdown("---")
                    st.markdown(response.text)
                    st.markdown("---")
                    st.caption("💡 Stick to this timeline to prevent late-minute chaos.")

                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

st.sidebar.markdown("---")
st.sidebar.markdown("**Hackathon Track:** Problem Statement 1")
st.sidebar.markdown("**Core Tech:** Google AI Studio, Gemini API")