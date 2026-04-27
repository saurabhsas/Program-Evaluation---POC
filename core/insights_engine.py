import numpy as np

def fmt_currency(x): return f"${x:,.0f}"
def fmt_number(x): return f"{int(x):,}"

def generate_insights(prompt, df):

    insights = []

    if df is None or df.empty:
        return ["No insights available."]

    cols = df.columns.tolist()

    # ---------------------------------------------------
    # 📈 TREND INSIGHTS (MONTH BASED)
    # ---------------------------------------------------
    if "MONTH" in cols:

        metric_cols = [c for c in cols if c != "MONTH"]

        for metric in metric_cols:

            values = df[metric].values

            total = np.sum(values)
            avg = np.mean(values)
            max_val = np.max(values)
            min_val = np.min(values)

            max_month = df.iloc[np.argmax(values)]["MONTH"]
            min_month = df.iloc[np.argmin(values)]["MONTH"]

            # Formatting
            if "Cost" in metric or metric == "Value":
                fmt = fmt_currency
            else:
                fmt = fmt_number

            insights.append(
                f"{metric}: total {fmt(total)}, average {fmt(avg)}, "
                f"highest in {max_month} ({fmt(max_val)}), lowest in {min_month} ({fmt(min_val)})."
            )

            # MoM change
            if len(values) >= 2:
                change = (values[-1] - values[-2]) / max(values[-2], 1) * 100
                direction = "increased" if change > 0 else "decreased"
                insights.append(f"{metric} has {direction} by {abs(change):.1f}% vs last month.")

    # ---------------------------------------------------
    # 📊 CATEGORY DISTRIBUTION
    # ---------------------------------------------------
    if "Dimension" in cols and "Value" in cols:

        df_sorted = df.sort_values("Value", ascending=False)

        total = df["Value"].sum()
        avg = df["Value"].mean()
        max_val = df_sorted.iloc[0]["Value"]
        min_val = df_sorted.iloc[-1]["Value"]

        top = df_sorted.iloc[0]
        bottom = df_sorted.iloc[-1]

        insights.append(
            f"Total cost is {fmt_currency(total)} with an average of {fmt_currency(avg)} per category."
        )

        insights.append(
            f"{top['Dimension']} is highest at {fmt_currency(max_val)}, "
            f"while {bottom['Dimension']} is lowest at {fmt_currency(min_val)}."
        )

        pct = max_val / max(total, 1) * 100
        insights.append(f"Top segment contributes {pct:.1f}% of total cost.")

    # ---------------------------------------------------
    # 🏥 UTILIZATION SUMMARY
    # ---------------------------------------------------
    if "ED Visits" in cols and "IP Visits" in cols:

        ed_total = df["ED Visits"].sum()
        ip_total = df["IP Visits"].sum()

        ratio = ed_total / max(ip_total, 1)

        insights.append(
            f"Total ED Visits: {fmt_number(ed_total)}, IP Visits: {fmt_number(ip_total)}."
        )

        insights.append(f"ED to IP ratio is {ratio:.2f}.")

        if ratio > 2:
            insights.append("High ED dependency suggests potential care inefficiencies.")

    # ---------------------------------------------------
    # 💸 AVOIDABLE SUMMARY
    # ---------------------------------------------------
    if prompt in ["Avoidable Cost Analysis", "Avoidable Cost by County"]:

        if "Dimension" in cols:
            m = dict(zip(df["Dimension"], df["Value"]))

            avoided = m.get("Avoidable ED", 0)
            avoid_ip = m.get("Avoidable IP", 0)

            insights.append(f"Avoidable ED events: {fmt_number(avoided)}.")
            insights.append(f"Avoidable IP events: {fmt_number(avoid_ip)}.")

            total_avoidable = avoided + avoid_ip
            insights.append(f"Total avoidable events: {fmt_number(total_avoidable)}.")

    # ---------------------------------------------------
    # 👤 MEMBER DISTRIBUTION
    # ---------------------------------------------------
    if prompt in ["Top 10 High Cost Members", "Cost Distribution Across Members"]:

        if "Value" in df.columns:

            total = df["Value"].sum()
            avg = df["Value"].mean()
            max_val = df["Value"].max()

            insights.append(
                f"Total member cost is {fmt_currency(total)} with an average of {fmt_currency(avg)}."
            )

            insights.append(
                f"Highest member cost is {fmt_currency(max_val)}, indicating skewed distribution."
            )

    # ---------------------------------------------------
    # 📊 RATIOS / SINGLE METRIC
    # ---------------------------------------------------
    if "Metric" in cols and "Value" in cols:

        val = df["Value"].values[0]

        if "Ratio" in prompt:
            insights.append(f"{prompt}: {val:.2f}")
        else:
            insights.append(f"{prompt}: {fmt_currency(val)}")

    # ---------------------------------------------------
    # 🎯 FINAL ACTIONABLE INSIGHTS
    # ---------------------------------------------------
    insights.append("Focus on high-cost segments for targeted interventions.")
    insights.append("Optimize care pathways to reduce avoidable utilization.")

    return insights