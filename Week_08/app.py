from flask import Flask, render_template, send_file
import pandas as pd
from charts import generate_charts
import joblib
from flask import request
import shap
from flask import send_file
from report_generator import generate_prediction_report
from report_generator import generate_optimization_report
from report_generator import generate_comparison_report


app = Flask(__name__)

file = pd.read_csv("dataset/final_featured_dataset.csv")
file = file.fillna("None")

model = joblib.load("models/catboost_model_2.pkl")
selected_features = joblib.load("models/selected_features2.pkl")

explainer = shap.TreeExplainer(model)


# Dashboard Route
@app.route("/")
def dashboard():

    total_records = file.shape[0]
    total_features = file.shape[1]
    missing_values = file.isnull().sum().sum()
    duplicates = file.duplicated().sum()
    target_mean = round(file["SalePrice"].mean(), 2) if "SalePrice" in file.columns else None

    generate_charts()

    stats = {
        "total_records": total_records,
        "total_features": total_features,
        "missing_values": missing_values,
        "duplicates": duplicates,
        "target_mean": target_mean
    }
    return render_template("dashboard.html", **stats)


# Analytics Route

@app.route("/analytics")
def analytics():

        corr = file.corr(numeric_only=True)["SalePrice"].sort_values(ascending=False)
        corr_table = pd.DataFrame({
            "Feature": corr.index,
            "Correlation": corr.values
        }).reset_index(drop=True)
        corr_table = corr_table[corr_table["Feature"] != "SalePrice"]
        corr_table = corr_table.head(20)

        skewness = file.skew(numeric_only=True).sort_values(ascending=False)
        skew_table = pd.DataFrame({
            "Feature": skewness.index,
            "Skewness": skewness.values
        }).reset_index(drop=True)

        skew_table = skew_table.head(20)
    
        return render_template("analytics.html",
                           corr_table=corr_table.to_dict(orient="records"),
                            skew_table=skew_table.to_dict(orient="records"))


# Reports Route

@app.route("/reports")
def reports():
    recommendations = "Focus on feature engineering for LotArea and OverallQual. Random Forest performed best after optimization."
    best_model = "CatBoost Regressor"
    performance_metrics = "MAE: 14311, RMSE: 19944, R²: 0.928"
    model_advantages = "High accuracy, handles categorical features well, robust to overfitting"
    model_limitations = "Longer training time, less interpretable compared to simpler models"
    missing_values = "Handled All missing values"
    outliers_removed = 2 
    features_engineered = 6  
    duplicates_removed = 10 
    return render_template(
        "reports.html",
        recommendations=recommendations,
        best_model=best_model,
        performance_metrics=performance_metrics,
        model_advantages=model_advantages,
        model_limitations=model_limitations,
        missing_values=missing_values,
        outliers_removed=outliers_removed,
        features_engineered=features_engineered,
        duplicates_removed=duplicates_removed
    )


# Report Download Route

from flask import send_file
from report_generator import generate_comparison_report

@app.route("/download_report")
def download_report():

    generate_comparison_report()

    return send_file(
        "reports/model_comparison_report.pdf",
        as_attachment=True
    )


@app.route("/comparison")
def comparison():

    comparison_df = pd.read_csv("dataset/model_comparison.csv")
    comparison_df = comparison_df.sort_values(
        by="R2 Score",
        ascending=False
    ).reset_index(drop=True)

    comparison_df["Rank"] = comparison_df.index + 1
    best_model = comparison_df.iloc[0]

    return render_template(
        "comparison.html",
        comparison=comparison_df.to_dict("records"),
        best_model=best_model
    )




@app.route("/prediction", methods=["GET", "POST"])
def prediction():

    if request.method == "POST":
        input_data = pd.DataFrame([{
            "OverallQual": int(request.form["OverallQual"]),
            "GrLivArea": float(request.form["GrLivArea"]),
            "TotalSF": float(request.form["TotalSF"]),
            "GarageCars": int(request.form["GarageCars"]),
            "GarageYrBlt": float(request.form["GarageYrBlt"]),
            "BsmtFinSF1": float(request.form["BsmtFinSF1"]),
            "LotArea": float(request.form["LotArea"])
        }])

        prediction = model.predict(input_data)[0]
        print("Prediction:", prediction)
        print("Input:")
        print(input_data)

        shap_values = explainer.shap_values(input_data)

        importance = pd.DataFrame({
            "Feature": input_data.columns,
            "SHAP": shap_values[0]
        })

        importance["Absolute"] = importance["SHAP"].abs()

        importance = importance.sort_values(
            by="Absolute",
            ascending=False
        ).head(6)

        top_features = []

        for _, row in importance.iterrows():
            top_features.append({
                "feature": row["Feature"],
                "value": round(row["SHAP"], 2)
            })

        generate_prediction_report(
            input_data,
            prediction,
            top_features
        )

        return render_template(
            "prediction.html",
            prediction=round(prediction,2),
            top_features=top_features
        )

    return render_template("prediction.html")

@app.route("/download_prediction_report")
def download_prediction_report():

    return send_file("reports/prediction_report.pdf",as_attachment=True)


@app.route("/download_optimization_report")
def download_optimization_report():

    pdf = generate_optimization_report()

    return send_file("reports/optimization_report.pdf", as_attachment=True)


@app.route("/download_eda_report")
def download_eda_report():

    return send_file("reports/Eda_Report.pdf", as_attachment=True )


@app.route("/download_preprocessing_report")
def download_preprocessing_report():
    return send_file("reports/Data_Preprocessing_report.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
