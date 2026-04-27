import plotly.express as px


def build_chart(df, prompt):

    # ---------------------------------------
    # 🛑 SAFETY CHECK
    # ---------------------------------------
    if df is None or df.empty:
        return px.bar(title="No Data Available")

    cols = df.columns.tolist()

    # --------------------------------------------------
    # 🧑‍🤝‍🧑 MEMBER-LEVEL CHARTS (FIX LABEL ISSUE)
    # --------------------------------------------------
    if prompt in ["Top 10 High Cost Members", "High Utilization Members"]:

        x_col = cols[0]  # MEMBERID / Dimension

        # 🔥 Ensure string (prevents 11B formatting)
        df[x_col] = df[x_col].astype(str)

        # ---- Multi-metric (Utilization) ----
        if "ED Visits" in cols and "IP Visits" in cols:

            df_melt = df.melt(
                id_vars=x_col,
                value_vars=["ED Visits", "IP Visits"],
                var_name="Metric",
                value_name="Value"
            )

            fig = px.bar(
                df_melt,
                x=x_col,
                y="Value",
                color="Metric",
                barmode="group",
                title=prompt
            )

        # ---- Single metric (Cost) ----
        else:
            fig = px.bar(
                df,
                x=x_col,
                y="Value",
                title=prompt
            )

        # 🔥 CRITICAL FIX → force categorical axis
        fig.update_xaxes(type="category")

        return fig

    # ---------------------------------------
    # 💰 COST CATEGORY → BAR
    # ---------------------------------------
    if prompt in [
        "Total Cost by Line of Business",
        "Total Cost by County",
        "Total Cost by Age Category",
        "Total Cost by Gender",
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
    # 📦 PRODUCT UTILIZATION (FSPRODUCT)
    # ---------------------------------------
    if prompt == "Product-wise Utilization":

        x_col = df.columns[0]  # FSPRODUCT

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
    # 📈 GENERIC TIME SERIES
    # ---------------------------------------
    if "MONTH" in cols:

        y_cols = [c for c in cols if c != "MONTH"]

        return px.line(
            df,
            x="MONTH",
            y=y_cols,
            markers=True,
            title=prompt
        )

    # ---------------------------------------
    # 📊 DEFAULT CATEGORY
    # ---------------------------------------
    if "Dimension" in cols and "Value" in cols:
        return px.bar(df, x="Dimension", y="Value", title=prompt)

    # ---------------------------------------
    # 🛑 FINAL FALLBACK
    # ---------------------------------------
    return px.bar(title="Unsupported chart format")
