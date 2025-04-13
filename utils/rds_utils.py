import pandas as pd
import sqlalchemy
from config import DB_CONNECTION_STRING

engine = sqlalchemy.create_engine(DB_CONNECTION_STRING)

def query_user_data(user_id):
    query = f"""
        SELECT * FROM nutrition_data
        WHERE user_id = '{user_id}'
    """
    df = pd.read_sql(query, engine)
    return df
