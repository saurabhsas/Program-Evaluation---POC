import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

def load_data():

    df = pd.read_csv(os.getenv("DATA_PATH"))

    # Normalize column names
    df.columns = df.columns.str.strip().str.upper()

    # Create Month column (Jan2025 format)
    df["MONTH"] = pd.to_datetime(
        df["ELIGIBILITYYEARANDMONTH"].astype(str),
        format="%Y%m"
    ).dt.strftime("%b%Y")

    return df