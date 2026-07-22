import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
matplotlib.use("Agg")

def generate_charts(file_path="dataset/final_featured_dataset.csv"):
    # Load dataset
    file = pd.read_csv(file_path)

    # SalePrice Histogram
    if "SalePrice" in file.columns:
        plt.figure(figsize=(8,5))
        sns.histplot(file["SalePrice"].dropna(), bins=40, kde=True, color="skyblue")
        plt.title("SalePrice Distribution")
        plt.xlabel("SalePrice")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.savefig("static/images/saleprice_histogram.png")
        plt.close()

    # Correlation Heatmap
    plt.figure(figsize=(10,8))
    corr = file.corr(numeric_only=True)
    sns.heatmap(corr, cmap="coolwarm", center=0)
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig("static/images/correlation_heatmap.png")
    plt.close()

    # Living Area vs SalePrice
    plt.figure(figsize=(8,5))
    sns.scatterplot(x=file["GrLivArea"], y=file["SalePrice"], alpha=0.6)
    plt.title("GrLivArea vs SalePrice")
    plt.xlabel("GrLivArea")
    plt.ylabel("SalePrice")
    plt.tight_layout()
    plt.savefig("static/images/another_chart.png")
    plt.close()



    # --- Missing Value Heatmap ---
    # Focus only on columns with missing values, limit to top 20 for clarity
    missing_cols = file.isnull().sum()
    missing_cols = missing_cols[missing_cols > 0].sort_values(ascending=False).head(20)

    plt.figure(figsize=(8,5))  # same size as box plot
    sns.heatmap(file[missing_cols.index].isnull(), cbar=False, cmap="viridis")
    plt.title("Missing Value Heatmap")
    plt.xticks(rotation=45, ha="right")  # rotate labels for readability
    plt.tight_layout()
    plt.savefig("static/images/missing_value_heatmap.png")
    plt.close()

    # --- SalePrice Box Plot ---
    plt.figure(figsize=(8,5))  # same size as heatmap
    sns.boxplot(x=file["SalePrice"])
    plt.title("SalePrice Box Plot")
    plt.xlabel("SalePrice")
    plt.tight_layout()
    plt.savefig("static/images/saleprice_boxplot.png")
    plt.close()


    metrics_dict = {
        "Linear Regression": {"MAE":22534.356179,"MSE":2.988824e+09,"RMSE":54670.135324,"R2":0.458912},
        "Decision Tree": {"MAE":27232.280822,"MSE":1.533306e+09,"RMSE":39157.448713,"R2":0.722415},
        "Random Forest": {"MAE":16740.269658,"MSE":6.227481e+08,"RMSE":24954.922212,"R2":0.887259},
        "Gradient Boosting": {"MAE":15264.313968,"MSE":4.625788e+08,"RMSE":21507.644612,"R2":0.916256},
        "XGBoost": {"MAE":17409.261719,"MSE":6.329558e+08,"RMSE":25158.612362,"R2":0.885412},
        "LightGBM": {"MAE":16006.293802,"MSE":6.001027e+08,"RMSE":24496.994374,"R2":0.891359}
    }

    # Bar chart for R² scores
    models = list(metrics_dict.keys())
    r2_scores = [metrics_dict[m]["R2"] for m in models]

    plt.figure(figsize=(8,5))
    sns.barplot(x=models, y=r2_scores, palette="viridis")
    plt.title("Model Comparison (R² Scores)")
    plt.ylabel("R² Score")
    plt.ylim(0,1)  # keep scale consistent
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig("static/images/model_comparison.png")
    plt.close()

    return metrics_dict


