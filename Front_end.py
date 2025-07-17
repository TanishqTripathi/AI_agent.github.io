import streamlit as st

st.set_page_config(page_title="AI Agent",layout="centered", initial_sidebar_state="expanded")
st.title("AI Agent")
st.write("This is a simple AI agent that can answer questions and perform tasks.")

system_prompt = st.text_area("System Prompt",height=70,placeholder="Enter system prompt here...")

MODEL_NAME_GROQ = ["llama-3.3-70b-versatile"]
# MODEL_NAME_OPENAI = ["gpt-4o-mini"]

provider = st.radio("Model Provider", ["groq"], index=0)

if provider == "groq":
    model_name = st.selectbox("Model Name", MODEL_NAME_GROQ, index=0)
# elif provider == "openai":
#     model_name = st.selectbox("Model Name", MODEL_NAME_OPENAI, index=0)

allow_search = st.checkbox("Allow Search")

user_query = st.text_area("User Query", height=200, placeholder="Enter your query here...")

API_URL = "http://127.0.0.1:8000/chat"

if st.button("Get Response"):
    if user_query.strip():
        import requests
        
        payload={
            "model_name": model_name,
            "model_provider": provider,
            "messages": [user_query],
            "allow_search": allow_search,
            "system_prompt": system_prompt
        }
        
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            response_data = response.json()
            if "error" in response_data:
                st.error(response_data["error"])
            else:
                st.subheader("AI Response")
                st.markdown(f"**Final Response:** {response_data}")