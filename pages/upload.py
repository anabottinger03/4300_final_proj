import streamlit as st
from utils import s3_utils
import uuid

def app():
    st.header("Upload Your Food Log")

    user_id = st.text_input("Enter your user ID")

    uploaded_file = st.file_uploader("Upload CSV file")

    if uploaded_file and user_id:
        file_id = str(uuid.uuid4())
        s3_utils.upload_to_s3(uploaded_file, user_id, file_id)
        st.success("File uploaded successfully!")
