def fmt_currency(x):
    return f"${x:,.0f}"


def fmt_number(x):
    return f"{int(x):,}"


def get_kpis(df):

    return {
        "Members": fmt_number(df["MEMBERID"].nunique()),
        "Medical Cost": fmt_currency(df["MEDICAL_PAID"].sum()),
        "Pharmacy Cost": fmt_currency(df["RX_PAID"].sum()),
        "Total Cost": fmt_currency(df["PAID"].sum()),
        "MR Allowed": fmt_currency(df["MR_ALLOWED"].sum()),

        # Counts (NO $)
        "Avoidable ED": fmt_number(df["AVOIDED"].sum()),
        "Avoidable IP": fmt_number(df["AVOIDIP"].sum()),

        "ED Visits": fmt_number(df["EDVISITS"].sum()),
        "IP Visits": fmt_number(df["IPVISITS"].sum()),

        # Cost buckets
        "Professional": fmt_currency(df["PROF"].sum()),
        "Outpatient": fmt_currency(df["FOP"].sum()),
        "Inpatient": fmt_currency(df["FIP"].sum()),
        "Others": fmt_currency(df["OTH"].sum())
    }
