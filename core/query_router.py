import pandas as pd


def sort_month(df):
    df["_SORT"] = pd.to_datetime(df["MONTH"], format="%b%Y")
    return df.sort_values("_SORT").drop(columns="_SORT")


def run_prompt(prompt, df):

    if df is None or df.empty:
        return pd.DataFrame()

    # =========================================================
    # 📈 TRENDS
    # =========================================================

    if prompt == "Monthly Total Cost Trend":
        res = df.groupby("MONTH")["PAID"].sum().reset_index()
        return sort_month(res.rename(columns={"PAID": "Total Cost"}))

    if prompt == "Medical vs Pharmacy Cost Split":
        res = df.groupby("MONTH")[["MEDICAL_PAID", "RX_PAID"]].sum().reset_index()
        res = res.rename(columns={
            "MEDICAL_PAID": "Medical Cost",
            "RX_PAID": "Pharmacy Cost"
        })
        return sort_month(res)

    if prompt == "ED vs IP Utilization Trend":
        res = df.groupby("MONTH")[["EDVISITS", "IPVISITS"]].sum().reset_index()
        res = res.rename(columns={
            "EDVISITS": "ED Visits",
            "IPVISITS": "IP Visits"
        })
        return sort_month(res)

    # =========================================================
    # 💰 COST DISTRIBUTION
    # =========================================================

    if prompt == "Total Cost by Line of Business":
        return df.groupby("LINEOFBUSINESS")["PAID"].sum().reset_index() \
            .rename(columns={"LINEOFBUSINESS": "Dimension", "PAID": "Value"})

    if prompt == "Total Cost by County":
        return df.groupby("COUNTY")["PAID"].sum().reset_index() \
            .rename(columns={"COUNTY": "Dimension", "PAID": "Value"})

    if prompt == "Total Cost by Age Category":
        return df.groupby("AGE_CATEGORY")["PAID"].sum().reset_index() \
            .rename(columns={"AGE_CATEGORY": "Dimension", "PAID": "Value"})

    if prompt == "Total Cost by Gender":
        return df.groupby("GENDER")["PAID"].sum().reset_index() \
            .rename(columns={"GENDER": "Dimension", "PAID": "Value"})

    if prompt == "Top 10 High Cost Members":
        res = df.groupby("MEMBERID")["PAID"].sum().nlargest(10).reset_index()
        res["MEMBERID"] = res["MEMBERID"].astype(str)
        return res.rename(columns={"MEMBERID": "Dimension", "PAID": "Value"})

    # =========================================================
    # 🏥 UTILIZATION
    # =========================================================

    if prompt == "High Utilization Members":
        res = df.groupby("MEMBERID")[["EDVISITS", "IPVISITS"]].sum().reset_index()
        res = res.sort_values("EDVISITS", ascending=False).head(10)

        res["MEMBERID"] = res["MEMBERID"].astype(str)

        return res.rename(columns={
            "EDVISITS": "ED Visits",
            "IPVISITS": "IP Visits"
        })

    # =========================================================
    # 💸 AVOIDABLE
    # =========================================================

    if prompt == "Avoidable Cost Analysis":
        res = df[["AVOIDED", "AVOIDIP"]].sum().reset_index()
        res.columns = ["Dimension", "Value"]

        res["Dimension"] = res["Dimension"].replace({
            "AVOIDED": "Avoidable ED",
            "AVOIDIP": "Avoidable IP"
        })

        return res

    if prompt == "Avoidable Cost by County":
        return df.groupby("COUNTY")[["AVOIDED", "AVOIDIP"]].sum().reset_index() \
            .rename(columns={
                "AVOIDED": "Avoidable ED",
                "AVOIDIP": "Avoidable IP"
            })

    # =========================================================
    # 📦 PRODUCT (FIXED → FSPRODUCT)
    # =========================================================

    if prompt == "Cost by Product":
        return df.groupby("FSPRODUCT")["PAID"].sum().reset_index() \
            .rename(columns={"FSPRODUCT": "Dimension", "PAID": "Value"}) \
            .sort_values("Value", ascending=False)

    if prompt == "Cost by Product Type":
        return df.groupby("PRODUCTTYPEDESCR")["PAID"].sum().reset_index() \
            .rename(columns={"PRODUCTTYPEDESCR": "Dimension", "PAID": "Value"}) \
            .sort_values("Value", ascending=False)

    if prompt == "Product-wise Utilization":

        res = df.groupby("FSPRODUCT")[["EDVISITS", "IPVISITS"]].sum().reset_index()

        res = res.rename(columns={
            "EDVISITS": "ED Visits",
            "IPVISITS": "IP Visits"
        })

        res = res.sort_values("ED Visits", ascending=False)

        return res

    # =========================================================
    # 📊 PMPM
    # =========================================================

    if prompt == "County-wise PMPM":
        g = df.groupby("COUNTY").agg({
            "PAID": "sum",
            "MEMBERID": "nunique"
        }).reset_index()

        g["Value"] = g["PAID"] / g["MEMBERID"]

        return g.rename(columns={"COUNTY": "Dimension"}) \
            .sort_values("Value", ascending=False)

    # =========================================================
    # 📊 PARETO (TOP 5%)
    # =========================================================

    if prompt == "Pareto Cost Analysis (Top 20%)":

        g = df.groupby("MEMBERID")["PAID"].sum().sort_values(ascending=False)

        top_n = max(int(0.05 * len(g)), 1)

        top_5 = g.head(top_n).reset_index()

        top_5["MEMBERID"] = top_5["MEMBERID"].astype(str)

        return top_5.rename(columns={
            "MEMBERID": "Dimension",
            "PAID": "Value"
        })

    # =========================================================
    # 🛑 SAFE FALLBACK
    # =========================================================

    return pd.DataFrame()
