import streamlit as st
import os
import google.generativeai as genai

st.set_page_config(
    page_title="The Last-Minute Life Saver",
    layout="centered",
    page_icon="⏰"
)

st.title("⏰ The Last-Minute Life Saver")
st.caption("An AI-powered active productivity companion built for Vibe2Ship.")

# Look for API Key in Streamlit Secrets first, then environment variables
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    with st.sidebar:
        st.subheader("Configuration")
        api_key = st.text_input("Enter your Gemini API Key:", type="password")

if not api_key:
    st.info("Please provide your Gemini API key in the sidebar or add it to Advanced Settings -> Secrets to begin.", icon="🔑")
else:
    # Configure the stable generative AI client
    genai.configure(api_key=api_key)

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

                    # Initialize the highly stable Gemini 1.5 Flash model
                    model = genai.GenerativeModel(
                        model_name='gemini-1.5-flash',
                        system_instruction=system_instruction
                    )

                    response = model.generate_content(
                        raw_user_tasks,
                        generation_config={"temperature": 0.3}
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
