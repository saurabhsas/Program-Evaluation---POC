import pandas as pd
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

@st.cache_data(show_spinner=False)
def load_data(member_ids=None):

    df = pd.read_csv(os.getenv("DATA_PATH"))
    df.columns = df.columns.str.strip().str.upper()

    # Create Month column
    df["MONTH"] = pd.to_datetime(
        df["ELIGIBILITYYEARANDMONTH"].astype(str),
        format="%Y%m"
    ).dt.strftime("%b%Y")

    # 🔥 APPLY MEMBER FILTER EARLY
    if member_ids is not None:
        df = df[df["MEMBERID"].isin(member_ids)]

    return df
