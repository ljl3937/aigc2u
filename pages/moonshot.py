import streamlit as st
import os

st.set_page_config(page_title="API key设置", layout="wide")
if "MOONSHOT_API_KEY" not in st.session_state:
    st.session_state["MOONSHOT_API_KEY"] = os.environ.get("MOONSHOT_API_KEY")
st.title("API key 设置")
moonshot_api_key = st.text_input("API key", value=st.session_state["MOONSHOT_API_KEY"], max_chars=None, key=None, type='password')
saved = st.button("保存")
if saved:
    st.session_state["MOONSHOT_API_KEY"] = moonshot_api_key