import os
import pandas as pd
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
import pandas as pd
from datetime import datetime

df = pd.read_csv("dataset/final_encoded_dataset.csv")
rows, cols = df.shape


def generate_comparison_report():
    # Read comparison CSV
    df = pd.read_csv("dataset/model_comparison.csv")
    os.makedirs("reports", exist_ok=True)

    pdf_path = "reports/model_comparison_report.pdf"
    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()
    elements = []

    # Title
    title = Paragraph(
        "<b>Advanced Regression Model Comparison Report</b>",
        styles["Title"]
    )

    elements.append(title)
    elements.append(Spacer(1, 0.25 * inch))

    # Details
    elements.append(
        Paragraph("<b>Project :</b> House Price Prediction", styles["Normal"])
    )

    elements.append(
        Paragraph("<b>Dataset :</b> House Prices", styles["Normal"])
    )

    elements.append(
        Paragraph("<b>Target :</b> SalePrice", styles["Normal"])
    )

    elements.append(Spacer(1, 0.25 * inch))

    # Summary
    summary = """
    Seven regression algorithms were trained and evaluated
    using R² Score, MAE, MSE, RMSE and Cross Validation.
    The best performing model is highlighted below.
    """

    elements.append(
        Paragraph("<b>Executive Summary</b>", styles["Heading2"])
    )

    elements.append(
        Paragraph(summary, styles["BodyText"])
    )

    elements.append(Spacer(1, 0.25 * inch))

    # Performance Table
    elements.append(
    Paragraph("<b>Model Performance</b>", styles["Heading2"])
    )

    table_data = [[ "Model", "R² Score", "MAE", "MSE", "RMSE", "CV Score" ]]

    for _, row in df.iterrows():
        table_data.append([
            row["Model"],
            f"{row['R2 Score']:.4f}",
            f"{row['MAE']:,.2f}",
            f"{row['MSE']:,.2f}",
            f"{row['RMSE']:,.2f}",
            f"{row['CV Score']:.4f}"
        ])

    table = Table(
        table_data,
        colWidths=[120, 60, 75, 90, 75, 65]
    )

    table.setStyle(TableStyle([

        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#0B5ED7")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("GRID", (0,0), (-1,-1), 0.5, colors.black),
        ("BACKGROUND", (0,1), (-1,-1), colors.whitesmoke),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("BOTTOMPADDING", (0,0), (-1,0), 8),
        ("TOPPADDING", (0,1), (-1,-1), 6),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    # Best Model

    best = df.sort_values(
        "R2 Score",
        ascending=False
    ).iloc[0]

    elements.append(
        Paragraph("<b>Best Model</b>", styles["Heading2"])
    )

    elements.append(
        Paragraph(
            f"""
            <b>Model :</b> {best['Model']}<br/>
            <b>R² Score :</b> {best['R2 Score']:.4f}<br/>
            <b>MAE :</b> {best['MAE']:.2f}<br/>
            <b>RMSE :</b> {best['RMSE']:.2f}<br/>
            <b>CV Score :</b> {best['CV Score']:.4f}
            """,
            styles["BodyText"]
        )
    )

    elements.append(Spacer(1, 0.25 * inch))

    # Conclusion
    elements.append(
        Paragraph("<b>Conclusion</b>", styles["Heading2"])
    )

    elements.append(
        Paragraph(
            f"""
            Based on the evaluation metrics,
            <b>{best['Model']}</b> achieved the best
            prediction performance and is recommended
            for deployment.
            """,
            styles["BodyText"]
        )
    )

    doc.build(elements)
    print("Report Generated Successfully")
    print(pdf_path)


def generate_prediction_report(input_data, prediction, top_features):

    os.makedirs("reports", exist_ok=True)
    pdf = SimpleDocTemplate("reports/prediction_report.pdf")

    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(
        Paragraph("<b>HOUSE PRICE PREDICTION REPORT</b>", styles["Title"])
    )
    elements.append(Spacer(1,20))

    # Prediction

    elements.append(
        Paragraph(
            f"<b>Predicted House Price :</b> ₹ {prediction:,.2f}",
            styles["Heading2"]
        )
    )

    elements.append(Spacer(1,20))

    # Input Table

    data = [["Feature","Value"]]
    for col in input_data.columns:
        data.append([col, str(input_data.iloc[0][col])])

    table = Table(data,colWidths=[220,150])
    table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.darkblue),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),1,colors.grey),
        ("BACKGROUND",(0,1),(-1,-1),colors.beige),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),

    ]))

    elements.append(table)
    elements.append(Spacer(1,20))

    # Top Features
    elements.append(
        Paragraph("<b>Top Feature Contributions</b>", styles["Heading2"])
    )
    for item in top_features:

        elements.append(
            Paragraph(
                f"{item['feature']} : {item['value']}",
                styles["BodyText"]
            )
        )

    elements.append(Spacer(1,20))

    # Model

    elements.append(
        Paragraph("<b>Model Used :</b> CatBoost Regressor",styles["BodyText"])
    )

    elements.append(
        Paragraph("<b>R² Score :</b> 0.9307",styles["BodyText"])
    )

    elements.append(
        Paragraph("<b>Cross Validation :</b> 0.9280",styles["BodyText"])
    )

    pdf.build(elements)

def generate_optimization_report():

    os.makedirs("reports", exist_ok=True)
    # Load dataset
    df = pd.read_csv("dataset/final_encoded_dataset.csv")

    rows, cols = df.shape
    pdf_path = "reports/optimization_report.pdf"

    doc = SimpleDocTemplate(pdf_path)
    styles = getSampleStyleSheet()

    elements = []
    # Title

    elements.append(
        Paragraph(
            "<b>MODEL OPTIMIZATION REPORT</b>",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "<b>Advanced Regression Model Comparison & Optimization Platform</b>",
            styles["Heading2"]
        )
    )

    elements.append(Spacer(1, 10))

    elements.append(
        Paragraph(
            f"<b>Generated On:</b> {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 20))

    # Dataset Information

    elements.append(
        Paragraph("<b>1. Dataset Information</b>", styles["Heading2"])
    )

    dataset = Table([
        ["Property", "Value"],
        ["Dataset", "House Prices"],
        ["Total Samples", rows],
        ["Total Features", cols - 1],
        ["Target Variable", "SalePrice"],
        ["Train/Test Split", "80% / 20%"]
    ], colWidths=[200, 200])

    dataset.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.darkblue),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 1, colors.grey),
        ("BACKGROUND", (0,1), (-1,-1), colors.beige),
        ("ALIGN", (0,0), (-1,-1), "CENTER")
    ]))

    elements.append(dataset)

    elements.append(Spacer(1, 20))

    # Optimization Technique

    elements.append(
        Paragraph("<b>2. Optimization Technique</b>", styles["Heading2"])
    )

    elements.append(
        Paragraph(
            """
            RandomizedSearchCV was used to optimize the regression models.
            Multiple combinations of hyperparameters were evaluated using
            5-fold cross-validation. The best parameter set was selected
            based on the highest R² Score.
            """,
            styles["BodyText"]
        )
    )

    elements.append(Spacer(1, 20))

    # Models Optimized
    elements.append(
        Paragraph("<b>3. Optimized Models</b>", styles["Heading2"])
    )

    model_table = Table([
        ["Algorithm", "Optimization Method"],
        ["Decision Tree", "RandomizedSearchCV"],
        ["Random Forest", "RandomizedSearchCV"],
        ["Gradient Boosting", "RandomizedSearchCV"],
        ["XGBoost", "RandomizedSearchCV"],
        ["LightGBM", "RandomizedSearchCV"],
        ["CatBoost", "RandomizedSearchCV"],
    ], colWidths=[220, 180])

    model_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.green),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 1, colors.grey),
        ("BACKGROUND", (0,1), (-1,-1), colors.whitesmoke),
        ("ALIGN", (0,0), (-1,-1), "CENTER")
    ]))

    elements.append(model_table)

    elements.append(Spacer(1, 20))

    # Best Model

    elements.append(
        Paragraph("<b>4. Final Selected Model</b>", styles["Heading2"])
    )

    elements.append(
        Paragraph(
            """
            <b>Algorithm:</b> CatBoost Regressor<br/>
            <b>R² Score:</b> 0.9307<br/>
            <b>MAE:</b> 14033.41<br/>
            <b>RMSE:</b> 19560.91<br/>
            <b>Cross Validation:</b> 0.9280
            """,
            styles["BodyText"]
        )
    )

    elements.append(Spacer(1, 20))

    # Conclusion
    elements.append(
        Paragraph("<b>5. Conclusion</b>", styles["Heading2"])
    )

    elements.append(
        Paragraph(
            """
            Hyperparameter optimization using RandomizedSearchCV significantly
            improved the predictive performance of the regression models.
            Among all optimized models, CatBoost Regressor achieved the best
            balance between prediction accuracy and generalization capability.
            Therefore, CatBoost was selected as the final deployment model.
            """,
            styles["BodyText"]
        )
    )

    doc.build(elements)
    return pdf_path


if __name__ == "__main__":
    generate_comparison_report()