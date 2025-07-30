# streamlit_app.py
import streamlit as st
import pandas as pd
import os
import requests

st.set_page_config(page_title="LLM Dashboard", layout="wide")

st.sidebar.title("📂 Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.session_state.df = df
    # Save file locally
    with open(os.path.join("data", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.sidebar.success("✅ File uploaded and saved!")

st.title("📊 AI-Powered Data Analysis Platform")

# Tabs
tab1, tab2, tab3 = st.tabs(["📈 Dashboard", "🧾 Data", "🤖 Chatbot"])

with tab1:
    st.subheader("Data Overview")
    if st.session_state.df is not None:
        st.metric("Rows", st.session_state.df.shape[0])
        st.metric("Columns", st.session_state.df.shape[1])
        st.write("📊 Charts will appear here soon.")
    else:
        st.info("Upload a file to see dashboard insights.")

with tab2:
    st.subheader("Preview Uploaded Data")
    if st.session_state.df is not None:
        st.dataframe(st.session_state.df, use_container_width=True)
    else:
        st.info("No data uploaded yet.")

with tab3:
    st.subheader("Ask the Assistant")
    if st.session_state.df is not None:
        user_input = st.text_input("Ask something about the data:")
        if user_input:
            # You could use requests.post to send to FastAPI or run local Crew
            st.write(f"🧠 Chatbot is thinking about: `{user_input}`")

    else:
        st.warning("Please upload data first to enable chatbot.")
