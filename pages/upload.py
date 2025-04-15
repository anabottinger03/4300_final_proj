import streamlit as st
import pandas as pd
import uuid
from utils.s3_uploader import get_s3_client, upload_to_s3

s3_client = get_s3_client()

st.title("Upload Nutrition Log")

uploaded_file = st.file_uploader("Select your nutrition log (.csv)", type="csv")

if uploaded_file is not None:
    st.write(f"Selected file: `{uploaded_file.name}`")

    try:
        # Try reading just to check it's a readable CSV
        _ = pd.read_csv(uploaded_file)

        # Reset file pointer for upload
        uploaded_file.seek(0)

        if st.button("Upload File"):
            user_id = "demo-user"  # Replace with real user later
            file_id = str(uuid.uuid4())

            success = upload_to_s3(s3_client, uploaded_file, user_id, file_id)

            if success:
                st.success("File uploaded successfully! Processing will complete shortly.")
            else:
                st.error("Upload failed!")

    except Exception as e:
        st.error(f"Error reading CSV file: {str(e)}")
