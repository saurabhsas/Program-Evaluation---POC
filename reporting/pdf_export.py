from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet


def export_pdf(kpis, df, prompt, insights):

    file_path = "healthcare_report.pdf"

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    story = []

    # Title
    story.append(Paragraph("Healthcare Executive Dashboard Report", styles["Title"]))
    story.append(Spacer(1, 20))

    # KPIs
    story.append(Paragraph("Key Metrics", styles["Heading2"]))
    story.append(Spacer(1, 10))

    for k, v in kpis.items():
        story.append(Paragraph(f"{k}: {v}", styles["Normal"]))

    story.append(Spacer(1, 20))

    # Selected Prompt
    story.append(Paragraph(f"Analysis: {prompt}", styles["Heading2"]))
    story.append(Spacer(1, 10))

    # Table (Top 20 rows max for readability)
    if df is not None and not df.empty:

        data = [df.columns.tolist()]

        for _, row in df.head(20).iterrows():
            data.append([str(x) for x in row.values])

        table = Table(data)
        story.append(table)
        story.append(Spacer(1, 20))

    # Insights
    story.append(Paragraph("Executive Insights", styles["Heading2"]))
    story.append(Spacer(1, 10))

    for ins in insights:
        story.append(Paragraph(f"- {ins}", styles["Normal"]))

    # Build PDF
    doc.build(story)

    return file_path