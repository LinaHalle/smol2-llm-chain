# denna filen lagrar och hämtar dataset
import pandas as pd

_df = None


def save_dataframe(df: pd.DataFrame):
    global _df
    _df = df

def get_dataframe():
    return _df