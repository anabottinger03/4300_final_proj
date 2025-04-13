import streamlit as st

st.set_page_config(page_title="Nutrition Analytics", layout="wide")

st.title("🍽️ Personalized Nutrition Dashboard")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Upload Log", "Analytics"])

if page == "Upload Log":
    from pages import upload
    upload.app()

elif page == "Analytics":
    from pages import analytics
    analytics.app()
