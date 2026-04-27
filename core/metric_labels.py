METRIC_MAP = {
    "MEDICAL_PAID": "Medical Cost",
    "RX_PAID": "Pharmacy Cost",
    "PAID": "Total Cost",
    "MR_ALLOWED": "MR Allowed",
    "AVOIDED": "Avoidable ED",
    "AVOIDIP": "Avoidable IP",
    "EDVISITS": "ED Visits",
    "IPVISITS": "IP Visits",
    "PROF": "Professional",
    "FOP": "Outpatient",
    "FIP": "Inpatient",
    "OTH": "Others"
}


def rename_columns(df):
    return df.rename(columns=METRIC_MAP)


def rename_dimension(df):
    if "Dimension" in df.columns:
        df["Dimension"] = df["Dimension"].replace(METRIC_MAP)
    return df


def rename_all(df):
    df = rename_columns(df)
    df = rename_dimension(df)
    return df