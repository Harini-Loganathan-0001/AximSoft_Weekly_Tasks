from flask import Flask, render_template, request, send_file
import os
import pandas as pd
import numpy as np
import tensorflow as tf
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences


app = Flask(__name__)

model = "notebooks/models2/gru_final_90.keras"

gru_model = tf.keras.models.load_model(model)
print("loaded")
print("Model input shape :", gru_model.input_shape)
print("Model output shape:", gru_model.output_shape)

with open("models/tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

MAX_SEQUENCE_LENGTH = 500



@app.route("/")
def home():
    return render_template("index.html")

def preprocess_review(review):
    sequence = tokenizer.texts_to_sequences([review])

    padded = pad_sequences(
        sequence,
        maxlen=MAX_SEQUENCE_LENGTH,
        padding="post",
        truncating="post"
    )

    return padded






def predict_sentiment(review):

    padded_review = preprocess_review(review)

    probability = float(
        gru_model.predict(padded_review, verbose=0)[0][0]
    )

    if probability >= 0.5:
        sentiment = "Positive"
        confidence = probability
    else:
        sentiment = "Negative"
        confidence = 1 - probability

    return {
        "sentiment": sentiment,
        "confidence": confidence,
        "positive_probability": probability,
        "negative_probability": 1 - probability
    }


@app.route("/prediction", methods=["GET", "POST"])
def prediction():

    result = None
    review = ""

    if request.method == "POST":

        review = request.form.get("review", "").strip()

        if review:
            result = predict_sentiment(review)

    return render_template(
        "predict.html",
        result=result,
        review=review
    )


@app.route("/comparison")
def comparison():

    baseline_path = "models/phase4_baseline_comparison.csv"

    baseline_df = pd.read_csv(baseline_path)

    baseline_columns = baseline_df.columns.tolist()

    baseline_data = baseline_df.to_dict(orient="records")

    # Final model comparison
    final_path = "models/phase7_final_model_comparison.csv"

    final_df = pd.read_csv(final_path)

    final_columns = final_df.columns.tolist()
    final_data = final_df.to_dict(orient="records")


    return render_template(
        "comparison.html",

        baseline_columns=baseline_columns,
        baseline_data=baseline_data,

        final_columns=final_columns,
        final_data=final_data
    )


@app.route("/analytics")
def analytics():
    return render_template("analytics.html")


@app.route("/batch-prediction", methods=["GET", "POST"])
def batch_prediction():

    results = None
    summary = None
    error = None

    if request.method == "POST":

        file = request.files.get("file")

        if not file or file.filename == "":
            error = "Please upload a CSV file."

        else:

            try:
                df = pd.read_csv(file)

                if "review" not in df.columns:
                    error = "CSV must contain a column named 'review'."

                else:

                    predictions = []

                    for review in df["review"].fillna("").astype(str):

                        if review.strip():

                            result = predict_sentiment(review)

                            predictions.append(
                                result["sentiment"]
                            )

                        else:
                            predictions.append("Unknown")

                    df["Predicted Sentiment"] = predictions

                    # Store results for download
                    batch_result_df = df.copy()

                    results = df.to_dict(
                        orient="records"
                    )

                    summary = {
                        "total": len(df),
                        "positive": predictions.count("Positive"),
                        "negative": predictions.count("Negative"),
                        "unknown": predictions.count("Unknown")
                    }

                    # Save temporarily
                    df.to_csv(
                        "batch_prediction_results.csv",
                        index=False
                    )

            except Exception as e:
                error = str(e)

    return render_template(
        "batch_prediction.html",
        results=results,
        summary=summary,
        error=error
    )
@app.route("/download-results")
def download_results():

    return send_file(
        "batch_prediction_results.csv",
        as_attachment=True,
        download_name="sentiment_predictions.csv",
        mimetype="text/csv"
    )

if __name__ == "__main__":
    app.run(debug=True)