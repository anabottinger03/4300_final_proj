import pandas as pd
# optional pre cleaning of upload locally 
def clean_nutrition_data(df):
    df['calories'] = df['calories'].fillna(0)
    df['sugar'] = df['sugar'].fillna(0)
    df['protein'] = df['protein'].fillna(0)
    df['fat'] = df['fat'].fillna(0)
    return df
