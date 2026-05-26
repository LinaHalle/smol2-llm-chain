import pandas as pd

df = None

def load_csv(file_path: str):
    global df
    df = pd.read_csv(file_path)
    return df

def get_starts():
    if df is None:
        return None
    return df.describe(include="all")