import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.s3_downloader import get_processed_data, get_latest_processed_key, get_all_processed_keys

# ---- CONFIG ----
BUCKET_NAME = "nutrition-processed-ab"
USER_ID = "demo-user"  # replace later with authenticated user


st.set_page_config(page_title="Nutrition Analytics Dashboard", layout="wide")

st.title("🍽️ Nutrition Analytics Dashboard")

try:
    st.sidebar.header("Upload Selection")
    view_mode = st.sidebar.radio("Choose data scope:", ["Latest Upload Only", "All Uploads"])

    if view_mode == "All Uploads":
        keys = get_all_processed_keys(BUCKET_NAME, USER_ID)
        dfs = [get_processed_data(BUCKET_NAME, key) for key in keys]
        df = pd.concat(dfs, ignore_index=True)
    else:
        latest_key = get_latest_processed_key(BUCKET_NAME, USER_ID)
        df = get_processed_data(BUCKET_NAME, latest_key)

    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
    df = df.dropna(subset=["Date"]).sort_values("Date")

    # Sidebar Filters
    st.sidebar.header("Filters")

    if 'apply_filters' not in st.session_state:
        st.session_state.apply_filters = False

    with st.sidebar.form("filters"):
        selected_date = st.selectbox("Select Date", sorted(df["Date"].dt.date.unique()))
        selected_meal = st.multiselect("Meal Type", df["Meal_Type"].dropna().unique())
        selected_category = st.multiselect("Category", df["Category"].dropna().unique())

        apply_button = st.form_submit_button("Apply Filters")
        reset_button = st.form_submit_button("Reset Filters")

    if apply_button:
        st.session_state.apply_filters = True
    if reset_button:
        st.session_state.apply_filters = False

    if st.session_state.apply_filters:
        filtered_df = df[
            (df["Date"].dt.date == selected_date) &
            (df["Meal_Type"].isin(selected_meal)) &
            (df["Category"].isin(selected_category))
        ]
    else:
        filtered_df = df.copy()

    if filtered_df.empty:
        st.warning("No data matches your filters. Try adjusting filters.")
    else:
        st.subheader("Summary Statistics")

        # Select only numeric columns (excluding metadata)
        numeric_cols = filtered_df.select_dtypes(include='number').columns
        st.dataframe(filtered_df[numeric_cols].describe())


        # --- Avg Calories per Meal Type ---
        st.subheader("Average Calories per Meal Type")
        avg_calories = filtered_df.groupby("Meal_Type")["Calories (kcal)"].mean().sort_values(ascending=False)
        fig1, ax1 = plt.subplots()
        avg_calories.plot(kind="bar", ax=ax1)
        ax1.set_ylabel("Avg Calories")
        st.pyplot(fig1)

        # --- Top Sugar Categories ---
        st.subheader("Top 10 Categories by Total Sugar")
        top_sugar = filtered_df.groupby("Category")["Sugars (g)"].sum().sort_values(ascending=False).head(10)
        fig2, ax2 = plt.subplots()
        top_sugar.plot(kind="barh", ax=ax2)
        ax2.set_xlabel("Total Sugar")
        st.pyplot(fig2)

        # --- Nutrition Trends Over Time ---
        st.subheader("Nutrition Trends Over Time")
        trend_metrics = ["Calories (kcal)", "Sugars (g)", "Fat (g)", "Protein (g)"]
        daily_trends = filtered_df.groupby("Date")[trend_metrics].sum()

        fig3, ax3 = plt.subplots(figsize=(10, 4))
        daily_trends.plot(ax=ax3, marker='o')
        ax3.set_ylabel("Total per Day")
        ax3.set_xlabel("Date")
        ax3.set_title("Daily Nutrition Trends")
        plt.xticks(rotation=45)
        st.pyplot(fig3)

        # Raw Filtered Data
        st.subheader("Filtered Entries")
        st.dataframe(filtered_df)

except Exception as e:
    st.error(f"Failed to load processed data: {str(e)}")
