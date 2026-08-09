from flask import Flask, render_template, request, session, send_file

import os
import numpy as np

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

import tensorflow as tf
import cv2
import matplotlib
import matplotlib.cm as cm

from report_generator import generate_prediction_report
from report_generator import generate_model_report

app = Flask(__name__)
app.secret_key = "harinithilo123"


# Load Model

MODEL_PATH = os.path.join("models", "resnet_SGD.keras")
print("Loading model:", MODEL_PATH)
model = load_model(MODEL_PATH)


print("\n MODEL LAYERS ")
for layer in model.layers:
    print(layer.name)

# Class Names
CLASS_NAMES = [
    "Actinic Keratosis",
    "Basal Cell Carcinoma",
    "Benign Keratosis",
    "Dermatofibroma",
    "Melanoma",
    "Melanocytic Nevus",
    "Vascular Lesion"
]

#
# Upload Folder

UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Prediction Function
def predict_image(img_path):

    from tensorflow.keras.applications.resnet50 import preprocess_input
    img = image.load_img(img_path, target_size=(224,224))
    img = image.img_to_array(img)
    img = preprocess_input(img)
    img = np.expand_dims(img, axis=0)

    predictions = model.predict(img, verbose=0)[0]
    print(predictions)
    print(np.argmax(predictions))

    print("\nPrediction Vector:")
    for cls, prob in zip(CLASS_NAMES, predictions):
        print(f"{cls}: {prob:.6f}")

    print("Predicted Index:", np.argmax(predictions))
    print("Predicted Class:", CLASS_NAMES[np.argmax(predictions)])

    predicted_index = np.argmax(predictions)
    predicted_class = CLASS_NAMES[predicted_index]
    confidence = float(predictions[predicted_index] * 100)

    probability_data = []
    for cls, prob in zip(CLASS_NAMES, predictions):
        probability_data.append({
            "class_name": cls,
            "probability": round(float(prob * 100),2)

        })

    probability_data.sort(

        key=lambda x: x["probability"],
        reverse=True

    )
    print("Predictions:", predictions)
    print("Length:", len(predictions))
    print(probability_data)

    return predicted_class, confidence, probability_data

# Dashboard
@app.route("/")

def dashboard():
    session.clear()

    return render_template("dashboard.html")


# Image Diagnosis
@app.route("/image_diagnosis", methods=["GET","POST"])
def image_diagnosis():

    prediction = None
    confidence = None
    probability_data = []
    image_path = None
    gradcam_path = None

    if request.method == "POST":
        if "image" not in request.files:
            return render_template(
                "image_diagnosis.html"
            )
        file = request.files["image"]
        if file.filename == "":

            return render_template(
                "image_diagnosis.html"
            )

        filename = file.filename

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        file.save(filepath)

        prediction, confidence, probability_data = predict_image(filepath)
        image_path = "uploads/" + filename

        # Create Grad-CAM image
        gradcam_path = save_gradcam(filepath)
        print("GradCAM Path:", gradcam_path)

        # Store values in session
        session["prediction"] = prediction
        session["confidence"] = confidence
        session["probability_data"] = probability_data
        session["image_path"] = "uploads/" + filename
        session["gradcam_path"] = gradcam_path
        
    return render_template(
        "image_diagnosis.html",
        prediction=prediction,
        confidence=confidence,
        probability_data=probability_data,
        image_path=image_path,
        model_name="ResNet20"

    )


# Explain Prediction

@app.route("/explain-prediction")
def explain_prediction():

    if "prediction" not in session:
        return render_template("explain_prediction.html")

    
    print("GradCAM Path:", session.get("gradcam_path"))
    return render_template("explain_prediction.html",
                          
        prediction=session.get("prediction"),
        confidence=session.get("confidence"),
        probability_data=session.get("probability_data", []),
        image_path=session.get("image_path"),
        gradcam_path=session.get("gradcam_path"),
        model_name="ResNet"
    )


def make_gradcam_heatmap(img_array, model, last_conv_layer_name):

    grad_model = tf.keras.models.Model(
        inputs=model.inputs,
        outputs=[
            model.get_layer(last_conv_layer_name).output,
            model.output
        ]
    )

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array)
        pred_index = tf.argmax(predictions[0])
        class_channel = predictions[:, pred_index]

    grads = tape.gradient(class_channel, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0,1,2))
    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = tf.maximum(heatmap, 0)
    max_val = tf.reduce_max(heatmap)

    if max_val != 0:
        heatmap /= max_val

    return heatmap.numpy()


# save the cam
def save_gradcam(img_path):

    print("save_gradcam() called")

    img = image.load_img(img_path, target_size=(224,224))
    from tensorflow.keras.applications.resnet50 import preprocess_input

    img_array = image.img_to_array(img)
    img_array = preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)

    heatmap = make_gradcam_heatmap(
        img_array,
        model,
        "conv5_block3_out"
    )

    print("Heatmap Shape:", heatmap.shape)
    img = cv2.imread(img_path)
    print("Original Image:", img.shape)

    img = cv2.resize(img,(224,224))
    heatmap = np.uint8(255 * heatmap)
    print("Heatmap Converted:", heatmap.shape)

    jet = matplotlib.colormaps["jet"]
    jet_colors = jet(np.arange(256))[:, :3]
    jet_heatmap = jet_colors[heatmap]
    jet_heatmap = cv2.resize(jet_heatmap,(224,224))
    jet_heatmap = np.uint8(jet_heatmap * 255)

    overlay = cv2.addWeighted(img,0.6,jet_heatmap,0.4,0)
    output_path = os.path.join(
        "static",
        "uploads",
        "gradcam_overlay.jpg"
    )

    print("Saving:", output_path)
    cv2.imwrite(output_path, overlay)
    print("Saved:", os.path.exists(output_path))

    return "uploads/gradcam_overlay.jpg"


@app.route("/download-prediction-report")
def download_prediction_report():
    return generate_prediction_report()


# Model Analytics

import pandas as pd
@app.route("/model-analytics")

def model_analytics():

    baseline = pd.read_csv("comparison/model_comparison.csv")
    models = baseline["Model"].tolist()

    train_accuracy = baseline["Train Accuracy"].tolist()
    val_accuracy = baseline["Validation Accuracy"].tolist()
    test_accuracy = baseline["Test Accuracy"].tolist()
    train_loss = baseline["Train Loss"].tolist()
    val_loss = baseline["Validation Loss"].tolist()
    test_loss = baseline["Test Loss"].tolist()

    best_index = baseline["Test Accuracy"].idxmax()
    best_model = baseline.loc[
        best_index,
        "Model"
    ]
    best_accuracy = baseline.loc[
        best_index,
        "Test Accuracy"
    ]

    baseline_table = baseline.to_dict(
        orient="records"
    )

    optimization_df = pd.read_csv(
    "comparison/optimization_summary.csv"
)   
    optimization_df["Test Accuracy"] = optimization_df["Test Accuracy"].apply(
        lambda x: f"{x:.2f}"
    )


    optimization_table = optimization_df.to_dict(
        orient="records"
    )
    optimization_models = optimization_df["Model"].tolist()
    optimization_accuracy = optimization_df["Test Accuracy"].tolist()

    evaluation = pd.read_csv(
        "comparison/evaluation_comparison.csv"
    )
    evaluation = evaluation.sort_values(
        by="Accuracy",
        ascending=False
    )
    final_table = evaluation.to_dict(
        orient="records"
    )

    return render_template("model_analytics.html",
                           train_accuracy=train_accuracy,
                            val_accuracy=val_accuracy,
                            test_accuracy=test_accuracy,

                            train_loss=train_loss,
                            val_loss=val_loss,
                            test_loss=test_loss,


                            best_model=best_model,
                            best_accuracy=best_accuracy,

                            total_models=len(baseline),
                            baseline_table=baseline_table,
                            optimization_table=optimization_table,

                            optimization_models=optimization_models,

                            optimization_accuracy=optimization_accuracy,
                            final_table=final_table)


@app.route("/download-model-report")
def download_model_report():

    pdf = generate_model_report()

    return send_file(
        pdf,
        as_attachment=True,
        download_name="Model_Comparison_Report.pdf",
        mimetype="application/pdf"
    )
        

# Reports

@app.route("/reports")
def reports():
    return render_template("reports.html")



if __name__ == "__main__":
    app.run(debug=True)