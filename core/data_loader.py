import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()


def load_data():

    # Load main dataset
    df = pd.read_csv(os.getenv("DATA_PATH"))
    df.columns = df.columns.str.strip().str.upper()

    # Create Month column
    df["MONTH"] = pd.to_datetime(
        df["ELIGIBILITYYEARANDMONTH"].astype(str),
        format="%Y%m"
    ).dt.strftime("%b%Y")

    # --------------------------------------------------
    # 🔥 NEW: MEMBER FILTER LOGIC
    # --------------------------------------------------

    member_path = os.getenv("MEMBER_FILTER_PATH")

    if member_path and os.path.exists(member_path):

        member_df = pd.read_csv(member_path)

        # Normalize column names
        member_df.columns = member_df.columns.str.upper()

        if "MEMBERID" not in member_df.columns:
            raise ValueError("Member filter file must contain MEMBERID column")

        member_ids = set(member_df["MEMBERID"].dropna().unique())

        # Filter main dataset
        df = df[df["MEMBERID"].isin(member_ids)]

    # --------------------------------------------------

    return df
