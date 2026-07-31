from flask import Flask, render_template, request
import os
import numpy as np

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

app = Flask(__name__)

# ==========================================
# Load Model
# ==========================================

MODEL_PATH = os.path.join("models", "mobilenetv2_rmsprop.keras")
model = load_model(MODEL_PATH)

# ==========================================
# Class Names
# ==========================================

CLASS_NAMES = [

    "Actinic Keratosis",

    "Basal Cell Carcinoma",

    "Benign Keratosis",

    "Dermatofibroma",

    "Melanocytic Nevus",

    "Melanoma",

    "Vascular Lesion"

]

# ==========================================
# Upload Folder
# ==========================================

UPLOAD_FOLDER = os.path.join("static", "uploads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ==========================================
# Prediction Function
# ==========================================

def predict_image(img_path):

    img = image.load_img(img_path, target_size=(224,224))

    img = image.img_to_array(img)

    img = img.astype("float32") / 255.0

    img = np.expand_dims(img, axis=0)

    predictions = model.predict(img, verbose=0)[0]

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

    return predicted_class, confidence, probability_data

# ==========================================
# Dashboard
# ==========================================

@app.route("/")

def dashboard():

    return render_template("dashboard.html")

# ==========================================
# Image Diagnosis
# ==========================================

@app.route("/image_diagnosis", methods=["GET","POST"])

def image_diagnosis():

    prediction = None
    confidence = None
    probability_data = []
    image_path = None

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

    return render_template(

        "image_diagnosis.html",

        prediction=prediction,

        confidence=confidence,

        probability_data=probability_data,

        image_path=image_path,

        model_name="MobileNetV2 + RMSprop"

    )

# ==========================================
# Explain Prediction
# ==========================================

@app.route("/explain-prediction")

def explain_prediction():

    return render_template("explain_prediction.html")

# ==========================================
# Model Analytics
# ==========================================

@app.route("/model-analytics")

def model_analytics():

    return render_template("model_analytics.html")

# ==========================================
# Reports
# ==========================================

@app.route("/reports")

def reports():

    return render_template("reports.html")

# ==========================================

if __name__ == "__main__":

    app.run(debug=True)