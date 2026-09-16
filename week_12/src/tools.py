import pandas as pd
import joblib
import shap

customer_data = pd.read_csv("data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv")
feature_data = pd.read_csv("data/processed/feature_engineered_customers.csv")
model = joblib.load("models/final_xgb_feature_model.pkl")
feature_selector = joblib.load("models/xgb_feature_selector.pkl")
scaler = joblib.load("models/xgb_scaler.pkl")
numeric_features = joblib.load("models/xgb_numeric_features.pkl")
training_columns = joblib.load("models/xgb_training_columns.pkl")
selected_features = pd.read_csv("models/xgb_selected_features.csv")["Feature"].tolist()

explainer = shap.TreeExplainer(model)

def get_customer_profile(customer_id):

    result = customer_data[customer_data["customerID"].astype(str) == str(customer_id)]

    if result.empty:
        return None

    return result.iloc[0].to_dict()

def prepare_customer_features(customer_id):

    feature_result = feature_data[feature_data["customerID"].astype(str) == str(customer_id)]

    if feature_result.empty:
        return None

    X_customer = feature_result.drop(columns=["customerID", "Churn"], errors="ignore").copy()

    categorical_features = X_customer.select_dtypes(include=["object", "category"]).columns.tolist()

    X_customer_encoded = pd.get_dummies(
        X_customer,
        columns=categorical_features,
        drop_first=False,
        dtype=int
    )

    X_customer_encoded = X_customer_encoded.reindex(
        columns=training_columns,
        fill_value=0
    )

    X_customer_encoded[numeric_features] = scaler.transform(X_customer_encoded[numeric_features])
    X_customer_selected = feature_selector.transform(X_customer_encoded)

    return X_customer_selected

def predict_customer_churn(customer_id):

    X_customer_selected = prepare_customer_features(customer_id)

    if X_customer_selected is None:
        return None

    probability = model.predict_proba(X_customer_selected)[0][1]

    if probability >= 0.60:
        risk_level = "High"
        prediction = "Likely to Churn"

    elif probability >= 0.40:
        risk_level = "Medium"
        prediction = "Likely to Stay"

    else:
        risk_level = "Low"
        prediction = "Likely to Stay"

    return {
        "customer_id": str(customer_id),
        "churn_probability": float(round(float(probability) * 100, 2)),
        "risk_level": risk_level,
        "prediction": prediction
    }

def get_customer_shap(customer_id):

    X_customer_selected = prepare_customer_features(customer_id)

    if X_customer_selected is None:
        return None

    shap_values = explainer.shap_values(X_customer_selected)

    if isinstance(shap_values, list):
        shap_values = shap_values[1]

    shap_values = shap_values[0]

    results = []

    for feature_name, shap_value in zip(selected_features, shap_values):
        results.append({
            "feature": feature_name,
            "shap_value": round(float(shap_value), 4),
            "impact": (
                "Increases Churn"
                if shap_value > 0
                else "Decreases Churn"
            )
        })

    results = sorted(
        results,
        key=lambda x: abs(x["shap_value"]),
        reverse=True
    )

    return results[:10]

def search_knowledge_base(query, top_k=5):

    from sentence_transformers import SentenceTransformer
    import faiss
    from sklearn.preprocessing import normalize

    knowledge_base = pd.read_csv("data/processed/knowledge_base_chunks.csv")
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    index = faiss.read_index("data/processed/knowledge_base2_faiss.index")

    query_embedding = embedding_model.encode([query], convert_to_numpy=True)

    query_embedding = normalize(
        query_embedding,
        norm="l2"
    ).astype("float32")

    distances, indices = index.search( query_embedding, top_k)

    results = knowledge_base.iloc[indices[0]].copy()
    results["similarity_score"] = distances[0]

    return results.reset_index(drop=True).to_dict(orient="records")
