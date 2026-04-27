import plotly.express as px
import pandas as pd


def build_chart(df, prompt):

    # ---------------------------------------
    # 🛑 SAFETY CHECK
    # ---------------------------------------
    if df is None or df.empty:
        return px.bar(title="No Data Available")

    cols = df.columns.tolist()

    # ---------------------------------------
    # 📊 CATEGORY UTILIZATION → BAR (SAFE MELT)
    # ---------------------------------------
    if prompt in [
        "Utilization by Age Category",
        "Utilization by Gender",
        "High Utilization Members"
    ]:

        # Detect correct X-axis column
        if "AGE_CATEGORY" in df.columns:
            x_col = "AGE_CATEGORY"
        elif "GENDER" in df.columns:
            x_col = "GENDER"
        elif "MEMBERID" in df.columns:
            x_col = "MEMBERID"
        else:
            # fallback: first non-numeric column
            non_numeric = df.select_dtypes(exclude="number").columns
            x_col = non_numeric[0] if len(non_numeric) > 0 else cols[0]

        # Convert to long format (prevents Plotly error)
        df_melt = df.melt(
            id_vars=x_col,
            value_vars=["ED Visits", "IP Visits"],
            var_name="Metric",
            value_name="Value"
        )

        return px.bar(
            df_melt,
            x=x_col,
            y="Value",
            color="Metric",
            barmode="group",
            title=prompt
        )

    # ---------------------------------------
    # 💰 COST CATEGORY → BAR
    # ---------------------------------------
    if prompt in [
        "Total Cost by Line of Business",
        "Total Cost by County",
        "Total Cost by Age Category",
        "Total Cost by Gender",
        "Top 10 High Cost Members",
        "Cost Distribution Across Members",
        "Cost by Product",
        "Cost by Product Type",
        "County-wise PMPM",
        "Pareto Cost Analysis (Top 20%)"
    ]:
        return px.bar(
            df,
            x="Dimension",
            y="Value",
            title=prompt
        )

    # ---------------------------------------
    # 💸 AVOIDABLE BY COUNTY → GROUPED BAR
    # ---------------------------------------
    if prompt == "Avoidable Cost by County":

        df_melt = df.melt(
            id_vars="COUNTY",
            value_vars=["Avoidable ED", "Avoidable IP"],
            var_name="Metric",
            value_name="Value"
        )

        return px.bar(
            df_melt,
            x="COUNTY",
            y="Value",
            color="Metric",
            barmode="group",
            title=prompt
        )

    # ---------------------------------------
    # 📈 MEDICAL vs PHARMACY → LINE
    # ---------------------------------------
    if prompt == "Medical vs Pharmacy Cost Split":
        return px.line(
            df,
            x="MONTH",
            y=["Medical Cost", "Pharmacy Cost"],
            markers=True,
            title=prompt
        )

    # ---------------------------------------
    # 📈 ED vs IP TREND → LINE
    # ---------------------------------------
    if prompt == "ED vs IP Utilization Trend":
        return px.line(
            df,
            x="MONTH",
            y=["ED Visits", "IP Visits"],
            markers=True,
            title=prompt
        )

    # ---------------------------------------
    # 📈 GENERIC TIME SERIES (SAFE)
    # ---------------------------------------
    if "MONTH" in cols:

        numeric_cols = df.select_dtypes(include="number").columns.tolist()

        if len(numeric_cols) == 0:
            return px.bar(title="No numeric data to plot")

        # Melt to avoid wide-form issues
        df_melt = df.melt(
            id_vars="MONTH",
            value_vars=numeric_cols,
            var_name="Metric",
            value_name="Value"
        )

        return px.line(
            df_melt,
            x="MONTH",
            y="Value",
            color="Metric",
            markers=True,
            title=prompt
        )

    # ---------------------------------------
    # 📊 DIMENSION + VALUE (DEFAULT)
    # ---------------------------------------
    if "Dimension" in cols and "Value" in cols:
        return px.bar(df, x="Dimension", y="Value", title=prompt)

    # ---------------------------------------
    # 📊 METRIC TABLE
    # ---------------------------------------
    if "Metric" in cols and "Value" in cols:
        return px.bar(df, x="Metric", y="Value", title=prompt)

    # ---------------------------------------
    # 🛑 FINAL FALLBACK
    # ---------------------------------------
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    if len(numeric_cols) > 0:
        x_col = df.select_dtypes(exclude="number").columns[0]
        return px.bar(df, x=x_col, y=numeric_cols)

    return px.bar(title="Unsupported chart format")