from io import BytesIO
import os

from flask import send_file, session
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)
import pandas as pd
from reportlab.lib.enums import TA_CENTER


def generate_prediction_report():

    prediction = session.get("prediction")
    confidence = session.get("confidence")
    image_path = session.get("image_path")
    gradcam_path = session.get("gradcam_path")
    probability_data = session.get("probability_data", [])

    if prediction is None:
        return None

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    story = []

    # Title
    story.append(
        Paragraph(
            "<b>AI Skin Disease Diagnosis Report</b>",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    
    # Prediction Summary

    summary = [
        ["Predicted Disease", prediction],
        ["Confidence", f"{confidence:.2f}%"],
        ["Model", "MobileNetV2"],
        ["Input Size", "224 × 224"],
        ["Total Classes", "7"]
    ]

    table = Table(summary, colWidths=[170, 260])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.whitesmoke),
        ("GRID",(0,0),(-1,-1),1,colors.grey),
        ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#E3F2FD")),
        ("FONTNAME",(0,0),(-1,-1),"Helvetica"),
        ("BOTTOMPADDING",(0,0),(-1,-1),8)
    ]))

    story.append(table)
    story.append(Spacer(1,20))

    
    # Original Image

    if image_path:

        img = Image(
            os.path.join("static", image_path),
            width=3*inch,
            height=3*inch
        )

        story.append(
            Paragraph("<b>Original Image</b>", styles["Heading2"])
        )

        story.append(img)
        story.append(Spacer(1,20))

    # GradCAM
    if gradcam_path:

        img = Image(
            os.path.join("static", gradcam_path),
            width=3*inch,
            height=3*inch
        )

        story.append(
            Paragraph("<b>Grad-CAM Heatmap</b>", styles["Heading2"])
        )

        story.append(img)
        story.append(Spacer(1,20))

    # Probability Table

    story.append(
        Paragraph(
            "<b>Prediction Probabilities</b>",
            styles["Heading2"]
        )
    )

    data = [["Disease", "Probability"]]
    for item in probability_data:
        data.append([
            item["class_name"],
            f'{item["probability"]:.2f}%'
        ])

    prob_table = Table(data)
    prob_table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.darkblue),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),1,colors.black),
        ("BACKGROUND",(0,1),(-1,-1),colors.beige),
        ("ALIGN",(0,0),(-1,-1),"CENTER")

    ]))

    story.append(prob_table)
    story.append(Spacer(1,20))

    # AI Explain

    story.append(
        Paragraph(
            "<b>AI Explanation</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            "The Grad-CAM heatmap highlights the image regions that "
            "most influenced the AI model while making the prediction.",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1,20))

    # Skin Care Tips

    story.append(
        Paragraph(
            "<b>Skin Care Tips</b>",
            styles["Heading2"]
        )
    )

    tips = [
        "• Use sunscreen with SPF 30 or higher.",
        "• Avoid prolonged exposure to direct sunlight.",
        "• Keep the skin clean and moisturized.",
        "• Avoid scratching the affected area.",
        "• Consult a dermatologist for medical advice."
    ]

    for tip in tips:
        story.append(
            Paragraph(tip, styles["BodyText"])
        )
    story.append(Spacer(1,20))

    # Disclaimer

    story.append(
        Paragraph(
            "<b>Medical Disclaimer</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            "This report is generated using an Artificial Intelligence "
            "model for educational purposes only. It should not replace "
            "professional medical diagnosis.",
            styles["BodyText"]
        )
    )

    doc.build(story)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="Prediction_Report.pdf",
        mimetype="application/pdf"
    )




def generate_model_report():

    pdf_buffer = BytesIO()

    doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=(8.27 * inch, 11.69 * inch),
        leftMargin=25,
        rightMargin=25,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    title = styles["Title"]
    title.alignment = TA_CENTER

    heading = styles["Heading2"]
    heading.alignment = TA_CENTER

    body = styles["BodyText"]

    elements = []

    # Read CSV

    comparison_df = pd.read_csv("comparison/model_comparison.csv")
    evaluation_df = pd.read_csv("comparison/evaluation_comparison.csv")

    # Title

    elements.append(
        Paragraph(
            "<font size=24><b>AI Skin Disease Classification</b></font>",
            title
        )
    )

    elements.append(
        Paragraph(
            "<font size=18><b>Model Comparison Report</b></font>",
            title
        )
    )

    elements.append(Spacer(1, 20))
    elements.append(
        Paragraph(
            """
            This report compares all baseline and transfer learning models
            trained for multi-class skin disease classification.
            The best-performing model is selected based on overall
            testing performance.
            """,
            body
        )
    )

    elements.append(Spacer(1, 18))

    # BASELINE COMPARISON

    elements.append(
        Paragraph(
            "<b>Baseline & Transfer Learning Model Comparison</b>",
            heading
        )
    )

    elements.append(Spacer(1, 10))

    comparison_data = [comparison_df.columns.tolist()]

    for row in comparison_df.values.tolist():
        comparison_data.append(row)

    comparison_table = Table(
        comparison_data,
        colWidths=[
            1.55*inch,
            1.25*inch,
            1.40*inch,
            1.20*inch,
            0.95*inch,
            1.25*inch,
            0.95*inch
        ]
    )

    comparison_table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1E3A8A")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,0),10),
        ("BOTTOMPADDING",(0,0),(-1,0),10),
        ("BACKGROUND",(0,1),(-1,-1),colors.whitesmoke),
        ("GRID",(0,0),(-1,-1),0.5,colors.grey),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("FONTSIZE",(0,1),(-1,-1),9),
    ]))

    elements.append(comparison_table)
    elements.append(Spacer(1,25))

    # EVALUATION TABLE
    elements.append(
        Paragraph(
            "<b>Evaluation Metrics Comparison</b>",
            heading
        )
    )

    elements.append(Spacer(1,10))
    evaluation_data=[evaluation_df.columns.tolist()]

    for row in evaluation_df.values.tolist():
        evaluation_data.append(row)
    evaluation_table=Table(
        evaluation_data,
        colWidths=[
            2.0*inch,
            1.0*inch,
            1.0*inch,
            1.0*inch,
            1.0*inch
        ]

    )

    evaluation_table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#059669")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("BOTTOMPADDING",(0,0),(-1,0),10),
        ("BACKGROUND",(0,1),(-1,-1),colors.beige),
        ("GRID",(0,0),(-1,-1),0.5,colors.grey),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("FONTSIZE",(0,0),(-1,-1),9),
    ]))

    elements.append(evaluation_table)
    elements.append(Spacer(1,30))

    # =====================================================
    # BEST MODEL
    # =====================================================

    best = evaluation_df.loc[
    evaluation_df["Accuracy"].idxmax()
]

    elements.append(
        Paragraph(
            "<b>Selected Best Performing Model</b>",
            heading
        )
    )

    elements.append(Spacer(1,10))

    best_data = [

        ["Model", best["Model"]],
        ["Accuracy", f"{best['Accuracy']:.4f}"],
        ["Precision", f"{best['Precision']:.4f}"],
        ["Recall", f"{best['Recall']:.4f}"],
        ["F1-Score", f"{best['F1Score']:.4f}"],
        ["ROC-AUC", f"{best['ROC-AUC']:.4f}"]

    ]

    best_table=Table(
        best_data,
        colWidths=[2.7*inch,3.5*inch]

    )

    best_table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#2563EB")),
        ("TEXTCOLOR",(0,0),(0,-1),colors.white),
        ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),
        ("BACKGROUND",(1,0),(1,-1),colors.whitesmoke),
        ("GRID",(0,0),(-1,-1),0.5,colors.grey),
        ("BOTTOMPADDING",(0,0),(-1,-1),8),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),

    ]))

    elements.append(best_table)
    elements.append(Spacer(1,25))

    # Conclusion

    elements.append(
        Paragraph(
            "<b>Conclusion</b>",
            heading
        )
    )

    elements.append(Spacer(1,10))

    elements.append(
        Paragraph(
            f"""
            Among all evaluated deep learning models,
            <b>{best['Model']}</b> achieved the best overall performance
            with an <b>Accuracy</b> of <b>{best['Accuracy']:.4f}</b>,
            <b>Precision</b> of <b>{best['Precision']:.4f}</b>,
            <b>Recall</b> of <b>{best['Recall']:.4f}</b>,
            <b>F1-Score</b> of <b>{best['F1Score']:.4f}</b>,
            and <b>ROC-AUC</b> of <b>{best['ROC-AUC']:.4f}</b>.
            Therefore, <b>{best['Model']}</b> was selected as the final model
            for deployment in the AI-Assisted Skin Disease Classification System.
            """,
            body
        )
    )

    doc.build(elements)
    pdf_buffer.seek(0)
    return pdf_buffer