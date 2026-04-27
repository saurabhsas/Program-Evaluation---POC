import streamlit as st
import os
from dotenv import load_dotenv

from core.data_loader import load_data
from core.filters import apply_filters
from core.metrics import get_kpis
from core.query_router import run_prompt
from core.insights_engine import generate_insights
from core.formatters import format_df
from visualization.chart_router import build_chart
from reporting.pdf_export import export_pdf

load_dotenv()

st.set_page_config(page_title=os.getenv("APP_TITLE"), layout="wide")
st.title("🏥 " + os.getenv("APP_TITLE"))

df = load_data()

# ---------------- FILTERS ----------------
with st.sidebar:
    st.header("Filters")

    lob = st.selectbox("Line of Business", ["All"] + sorted(df["LINEOFBUSINESS"].dropna().unique()))
    fsproduct = st.selectbox("FS Product", ["All"] + sorted(df["FSPRODUCT"].dropna().unique()))
    accountid = st.selectbox("Account ID", ["All"] + sorted(df["ACCOUNTID"].dropna().unique()))
    accountname = st.selectbox("Account Name", ["All"] + sorted(df["ACCOUNTNAME"].dropna().unique()))
    county = st.selectbox("County", ["All"] + sorted(df["COUNTY"].dropna().unique()))
    zipcode = st.selectbox("Zip Code", ["All"] + sorted(df["ZIPCODE"].dropna().unique()))
    age_category = st.selectbox("Age Category", ["All"] + sorted(df["AGE_CATEGORY"].dropna().unique()))
    gender = st.selectbox("Gender", ["All"] + sorted(df["GENDER"].dropna().unique()))

filtered = apply_filters(df, gender, lob, fsproduct, accountid, accountname, county, zipcode, age_category)

# ---------------- PROMPTS ----------------
PROMPTS = [
    "Monthly Total Cost Trend", "Medical vs Pharmacy Cost Split",
    "Total Cost by Line of Business","Total Cost by County","Total Cost by Age Category",
    "Total Cost by Gender","Top 10 High Cost Members",
    "ED vs IP Utilization Trend",
    "High Utilization Members","Avoidable Cost Analysis","Avoidable Count by County",
    "Cost by Product","Cost by Product Type","Product-wise Utilization",
    "County-wise PMPM","Pareto Cost Analysis (Top 5%)"
]

selected_prompt = st.selectbox("Select Business Question", PROMPTS)

# ---------------- RUN ----------------
if st.button("Generate Insights"):

    result = run_prompt(selected_prompt, filtered)

    if result is None or result.empty:
        st.error("No data available")
        st.stop()

    # KPIs
    kpis = get_kpis(filtered)
# ---------------- KPI CARDS ----------------
    st.markdown("### 📊 Key Metrics")

    kpi_icons = {
        "Medical Cost": "💰",
        "Pharmacy Cost": "💊",
        "Total Cost": "💵",
        "MR Allowed": "📊",
        "Avoidable ED": "⚠️",
        "Avoidable IP": "🚨",
        "ED Visits": "🏥",
        "IP Visits": "🛏️",
        "Professional": "👨‍⚕️",
        "Outpatient": "🏥",
        "Inpatient": "🛌",
        "Others": "📦"
    }

    def render_kpi_card(title, value, icon):

        return f"""
        <div style="
            background-color:#ffffff;
            padding:15px;
            border-radius:12px;
            box-shadow:0px 2px 8px rgba(0,0,0,0.08);
            text-align:center;
            margin-bottom:10px;
        ">
            <div style="font-size:14px; color:#6c757d;">
                {icon} {title}
            </div>
            <div style="
                font-size:20px;
                font-weight:600;
                color:#2c3e50;
                margin-top:5px;
            ">
                {value}
            </div>
        </div>
        """

    # Display in grid
    cols = st.columns(4)

    for i, (k, v) in enumerate(kpis.items()):
        with cols[i % 4]:
            st.markdown(
                render_kpi_card(k, v, kpi_icons.get(k, "📌")),
                unsafe_allow_html=True
            )

    # Chart
    fig = build_chart(result, selected_prompt)
    st.plotly_chart(fig, use_container_width=True)

    # Table
    st.dataframe(format_df(result.copy()), use_container_width=True)

    # Insights
    insights = generate_insights(selected_prompt, result)
    st.subheader("🧠 Executive Insights")

    insight_html = """
    <div style="
        font-family: Arial, sans-serif;
        font-size: 14px;
        line-height: 1.6;
        color: #333333;
    ">
    <ul>
    """

    for ins in insights:
        insight_html += f"<li style='margin-bottom:8px;'>{ins}</li>"

    insight_html += "</ul></div>"

    st.markdown(insight_html, unsafe_allow_html=True)    

    # PDF
    pdf_path = export_pdf(kpis, result, selected_prompt, insights)
    with open(pdf_path, "rb") as f:
        st.download_button("Download PDF", f, "healthcare_report.pdf")
