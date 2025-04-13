import pandas as pd


# Load original data
df = pd.read_csv("data/daily_food_nutrition_dataset.csv")

# Drop rows with any null values
df_clean = df.dropna()

# Optional: Reset index after dropping
df_clean = df_clean.reset_index(drop=True)

# Save cleaned version
df_clean.to_csv("data/cleaned_food_nutrition_dataset.csv", index=False)

print("Cleaning Complete. Saved as cleaned_food_nutrition_dataset.csv")
