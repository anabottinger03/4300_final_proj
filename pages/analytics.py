import streamlit as st
from utils import rds_utils
import pandas as pd

def app():
    st.header("Nutrition Analytics")

    user_id = st.text_input("Enter your user ID")

    if user_id:
        df = rds_utils.query_user_data(user_id)

        if df.empty:
            st.warning("No data found.")
        else:
            st.write("Raw Data")
            st.dataframe(df)

            st.subheader("Average Calories per Meal")
            st.bar_chart(df.groupby('meal_type')['calories'].mean())

            st.subheader("Macronutrient Breakdown")
            macros = df[['protein', 'fat', 'sugar']].sum()
            st.bar_chart(macros)
