import os
import numpy as np
import pandas as pd
import joblib
import tensorflow as tf


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "models", "phase7", "final_rnn_48h_to_24h_rmsprop.keras")
DATA_PATH = os.path.join(BASE_DIR, "processed_data", "PJME_phase2_preprocessed.csv")
FEATURE_SCALER_PATH = os.path.join( BASE_DIR, "scalers", "feature_scaler.pkl")
TARGET_SCALER_PATH = os.path.join( BASE_DIR, "scalers", "target_scaler.pkl")
OUTPUT_PATH = os.path.join( BASE_DIR, "scalers", "forecast_intervals.pkl")


INPUT_HOURS = 48
FORECAST_HOURS = 24

#load model
model = tf.keras.models.load_model(MODEL_PATH)


#load scales
feature_scaler = joblib.load(FEATURE_SCALER_PATH)
target_scaler = joblib.load(TARGET_SCALER_PATH)

print("Scalers loaded")

# load data
data = pd.read_csv(DATA_PATH, parse_dates=["Datetime"])
data = (data.sort_values("Datetime").reset_index(drop=True))


feature_columns = [

    "Hour",
    "Day",
    "Week",
    "Month",
    "DayOfWeek",
    "IsWeekend",

    "Lag_1",
    "Lag_24",
    "Lag_48",
    "Lag_168",

    "Rolling_Mean_24",
    "Rolling_Mean_168",

    "Rolling_Std_24",
    "Rolling_Std_168"
]


validation_hours = 60 * 24

validation_start = (len(data) - validation_hours)
validation_data = data.iloc[validation_start:].copy()



# create sequences 48 to 24
X_validation = []
y_validation = []


for i in range(validation_start, len(data) - FORECAST_HOURS, FORECAST_HOURS):

    sequence = data.iloc[i - INPUT_HOURS:i][feature_columns]

    target = data.iloc[i:i + FORECAST_HOURS]["PJME_MW"].values

    if len(sequence) != INPUT_HOURS:
        continue

    if len(target) != FORECAST_HOURS:
        continue

    X_validation.append(sequence.values)
    y_validation.append(target)


X_validation = np.array(X_validation)
y_validation = np.array(y_validation)


print("X validation shape:",X_validation.shape)
print("Y validation shape:", y_validation.shape)

# scale the features
X_scaled = feature_scaler.transform(X_validation.reshape(-1, len(feature_columns)))
X_scaled = X_scaled.reshape(X_validation.shape)

print("Scaled X shape:", X_scaled.shape)

#prediction
predicted_scaled = model.predict(X_scaled, verbose=0)


print("Predicted scaled shape:", predicted_scaled.shape)

# inverse transform
predicted = (target_scaler.inverse_transform( predicted_scaled.reshape(-1, 1)).reshape(predicted_scaled.shape))

# calculate the errors
errors = (y_validation - predicted)

print("Error shape:",errors.shape)


# forecast interval
lower_errors = np.percentile(errors, 2.5, axis=0)
upper_errors = np.percentile(errors, 97.5, axis=0)

#save
intervals = {
    "lower_errors":lower_errors,
    "upper_errors":upper_errors,
    "confidence_level":0.95
}

