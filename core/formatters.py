import pandas as pd

def fmt_currency(x): return f"${x:,.0f}"
def fmt_number(x): return f"{int(x):,}"

def format_df(df):
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            if "Cost" in col or col == "Value":
                df[col] = df[col].apply(fmt_currency)
            elif "Visits" in col or "Avoidable" in col:
                df[col] = df[col].apply(fmt_number)
    return df