from flask import Flask, render_template, request
import os
import numpy as np
import pandas as pd
import joblib
import tensorflow as tf


app = Flask(__name__)

# path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


MODEL_PATH = os.path.join(BASE_DIR, "models", "phase7", "final_rnn_48h_to_24h_rmsprop.keras")
FEATURE_SCALER_PATH = os.path.join(BASE_DIR, "scalers","feature_scaler.pkl")
TARGET_SCALER_PATH = os.path.join(BASE_DIR,"scalers", "target_scaler.pkl")
DATA_PATH = os.path.join( BASE_DIR, "processed_data", "PJME_phase2_preprocessed.csv")
INTERVAL_PATH = os.path.join(BASE_DIR,"scalers","forecast_intervals.pkl")

# load model
model = tf.keras.models.load_model(MODEL_PATH)

forecast_intervals = joblib.load(INTERVAL_PATH)

lower_errors = forecast_intervals["lower_errors"]
upper_errors = forecast_intervals["upper_errors"]

print("model loaded")
print("Input shape :", model.input_shape)
print("Output shape:", model.output_shape)
print("Forecast intervals loaded")
print("Lower errors shape:", np.asarray(lower_errors).shape)
print("Upper errors shape:", np.asarray(upper_errors).shape)

# load scalers
feature_scaler = joblib.load(FEATURE_SCALER_PATH)
target_scaler = joblib.load(TARGET_SCALER_PATH)

print("Feature scaler loaded")
print("Target scaler loaded")

# load data
PJME_data = pd.read_csv(DATA_PATH)
PJME_data["Datetime"] = pd.to_datetime(PJME_data["Datetime"])
PJME_data = PJME_data.sort_values("Datetime").reset_index(drop=True)


print("Dataset loaded:",PJME_data.shape)


# features
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

# Create future features
def create_future_features(dt, demand_history):

    values = np.asarray(demand_history, dtype=float)

    features = {
        "Hour": dt.hour,
        "Day": dt.day,
        "Week": int(dt.isocalendar().week),
        "Month": dt.month,
        "DayOfWeek": dt.dayofweek,
        "IsWeekend": int(dt.dayofweek >= 5),
        "Lag_1": values[-1],
        "Lag_24": values[-24],
        "Lag_48": values[-48],
        "Lag_168": values[-168],
        "Rolling_Mean_24": np.mean(values[-24:]),
        "Rolling_Mean_168": np.mean(values[-168:]),
        "Rolling_Std_24": np.std(values[-24:]),
        "Rolling_Std_168": np.std(values[-168:])
    }

    return features


# genrate 24 hourss forecast
def generate_24_hour_forecast():

    demand_history = (PJME_data["PJME_MW"].astype(float).tolist() )
    last_datetime = ( PJME_data["Datetime"].iloc[-1])

    future_dates = pd.date_range(
        start=(last_datetime + pd.Timedelta(hours=1)),
        periods=24,
        freq="h"
    )

    # buile the last 24 input features
    sequence_features = []
    all_demand = demand_history

    start_index = (len(PJME_data) - 48)

    for i in range(start_index, len(PJME_data)):

        dt = PJME_data.iloc[i]["Datetime"]
        previous_values = all_demand[:i]

        # Safe
        if len(previous_values) < 168:
            previous_values = all_demand[:168]

        row = create_future_features(dt, previous_values)
        sequence_features.append(row)


    sequence_features = pd.DataFrame(sequence_features)
    sequence_features = sequence_features[feature_columns]

    #scalee
    sequence_scaled = (feature_scaler.transform(sequence_features))

    # rnn input
    sequence_scaled = sequence_scaled.reshape(1, 48, 14)

    print("Forecast inputtt:", sequence_scaled.shape)

    #prediction
    prediction_scaled = model.predict(sequence_scaled, verbose=0)

    # inverse scale
    predictions = (target_scaler.inverse_transform(
            prediction_scaled.reshape(-1, 1)).flatten()
    )

    lower_bounds = predictions + lower_errors
    upper_bounds = predictions + upper_errors


    # results
    forecast_df = pd.DataFrame({
        "Datetime": future_dates,
        "Forecast_MW": predictions,
        "Lower_MW": lower_bounds,

    "Upper_MW": upper_bounds
    })


    return forecast_df

#dashboard
@app.route("/")
def dashboard():

    latest_demand = float(PJME_data["PJME_MW"].iloc[-1])
    latest_datetime = (PJME_data["Datetime"].iloc[-1])

    average_demand = float(PJME_data["PJME_MW"].tail(24).mean())
    maximum_demand = float(PJME_data["PJME_MW"].max())

    minimum_demand = float(PJME_data["PJME_MW"].min())

    return render_template("dashboard.html",
        latest_demand=latest_demand,
        latest_datetime=latest_datetime,
        average_demand=average_demand,
        maximum_demand=maximum_demand,
        minimum_demand=minimum_demand
    )


# forecast page
@app.route("/forecast", methods=["GET", "POST"])
def forecast():

    forecast_df = None
    forecast_available = False
    average_forecast = None
    peak_forecast = None
    minimum_forecast = None
    peak_time = None
    error = None

    if request.method == "POST":
        try:
            forecast_df = (generate_24_hour_forecast())
            forecast_available = True
            average_forecast = round(forecast_df["Forecast_MW"].mean(), 2)

            peak_index = (forecast_df["Forecast_MW"].idxmax())

            peak_forecast = round(forecast_df.loc[peak_index,"Forecast_MW"], 2)

            minimum_forecast = round(forecast_df["Forecast_MW"].min(),2)
            peak_time = (forecast_df.loc[peak_index, "Datetime"].strftime("%Y-%m-%d %H:%M"))

        except Exception as e:
            error = str(e)
            print("Forecast error:",e)


    return render_template("forecast.html",
        forecast=forecast_df,
        forecast_available=forecast_available,
        average_forecast=average_forecast,
        peak_forecast=peak_forecast,
        minimum_forecast=minimum_forecast,
        peak_time=peak_time,
        error=error
    )

# analytics page
@app.route("/analytics")
def analytics():

    recent_data = (PJME_data.tail(168).copy())
    recent_data["Datetime"] = (recent_data["Datetime"].dt.strftime("%Y-%m-%d %H:%M"))
    dates = recent_data["Datetime"].tolist()

    demand = recent_data["PJME_MW"].tolist()

    daily_data = (PJME_data.set_index("Datetime")["PJME_MW"].resample("D").mean().tail(30))

    daily_dates = [x.strftime("%Y-%m-%d")for x in daily_data.index]

    daily_values = (daily_data.round(2).tolist())

    return render_template("analytics.html",
        dates=dates,
        demand=demand,
        daily_dates=daily_dates,
        daily_values=daily_values
    )

# validation page
@app.route("/validation")
def validation():

    df = pd.read_csv("comparison/phase7_final_results.csv")
    validation_data = {
        "30": {
            "mae": 1760.4446451822917,
            "rmse": 2485.4733423173907,
            "mape": 5.014282326881961,
            "r2": 0.8998047358504945,
            "bias": 304.7603515625
        },

        "60": {
            "mae": 1945.6095269097223,
            "rmse": 2739.1471559224597,
            "mape": 5.34199935184507,
            "r2": 0.873378420077503,
            "bias": 282.6929633246528
        }
    }

    peak_demand_data = {
        "30": {
            "mae": 2680.5411241319443,
            "rmse": 3255.570996511496,
            "mape": 5.509521015338086
        },

        "60": {
            "mae": 3159.5068088107637,
            "rmse": 3777.598196631339,
            "mape": 6.465600064149024
        }
    }

    return render_template("validation.html",
        validation_data=validation_data,
        peak_demand_data=peak_demand_data
    )

if __name__ == "__main__":
    app.run(debug=True)