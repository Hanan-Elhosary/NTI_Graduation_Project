import streamlit as st
import pandas as pd
import os
import requests

st.set_page_config(page_title="LLM Dashboard", layout="wide")

st.sidebar.title("📂 Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

if 'df' not in st.session_state:
    st.session_state.df = None
if 'csv_path' not in st.session_state:
    st.session_state.csv_path = None

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.session_state.df = df

    os.makedirs("data", exist_ok=True)
    csv_path = os.path.join("data", uploaded_file.name)
    with open(csv_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.session_state.csv_path = csv_path
    st.sidebar.success("✅ File uploaded and saved!")

st.title("📊 AI-Powered Data Analysis Platform")

tab1, tab2, tab3 = st.tabs(["📈 Dashboard", "🧾 Data", "🤖 Chatbot"])

with tab1:
    st.subheader("Data Overview")
    if st.session_state.df is not None:
        st.metric("Rows", st.session_state.df.shape[0])
        st.metric("Columns", st.session_state.df.shape[1])
        with st.spinner("Generating Dashboard..."):
            response = requests.post(
                "http://127.0.0.1:8000/run-crew",
                json={
                    "argument": "Generate dashboard",
                    "csv_path": st.session_state.csv_path
                }
            )
            if response.status_code == 200:
                st.markdown(response.json()["result"], unsafe_allow_html=True)
            else:
                st.error("❌ Failed to generate dashboard.")
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
            with st.spinner("Thinking..."):
                response = requests.post(
                    "http://127.0.0.1:8000/run-crew",
                    json={
                        "argument": user_input,
                        "csv_path": st.session_state.csv_path
                    }
                )
                if response.status_code == 200:
                    st.success("✅ Chatbot response received!")
                    st.write(response.json()["result"])
                else:
                    st.error("❌ Failed to get a response.")
    else:
        st.warning("Please upload data first to enable chatbot.")

