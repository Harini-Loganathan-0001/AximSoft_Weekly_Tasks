from flask import Flask, render_template, request
import pandas as pd
import joblib
import shap
import ollama
from sklearn.preprocessing import normalize

from sentence_transformers import SentenceTransformer
import faiss
import pickle
import ollama
from sklearn.preprocessing import normalize

app = Flask(__name__)

# load customer data
customer_data = pd.read_csv("data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv")

# load ml model
model = joblib.load("models/final_xgb_feature_model.pkl")

# load featured dataset
feature_data = pd.read_csv("data/processed/feature_engineered_customers.csv")

# load fiass index
index = faiss.read_index("data/processed/knowledge_base2_faiss.index")

# load knowledge base chunks
knowledge_base = pd.read_csv("data/processed/knowledge_base_chunks.csv")

feature_selector = joblib.load("models/xgb_feature_selector.pkl")

scaler = joblib.load("models/xgb_scaler.pkl")

numeric_features = joblib.load("models/xgb_numeric_features.pkl")

training_columns = joblib.load("models/xgb_training_columns.pkl")

selected_features = pd.read_csv("models/xgb_selected_features.csv")["Feature"].tolist()

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# Fix TotalCharges
customer_data["TotalCharges"] = pd.to_numeric(customer_data["TotalCharges"], errors="coerce")
customer_data["TotalCharges"] = customer_data["TotalCharges"].fillna(customer_data["TotalCharges"].median())

explainer = shap.TreeExplainer(model)

LLM_MODEL = "llama3.2:3b"

# HIGH_RISK_CUSTOMERS = []

# dashboard
@app.route("/")
def dashboard():

    total_customers = len(customer_data)

    churned_customers = (customer_data["Churn"] == "Yes").sum()

    churn_rate = (churned_customers / total_customers) * 100

    average_monthly_charges = (customer_data["MonthlyCharges"].mean())

    average_tenure = (customer_data["tenure"].mean())

    return render_template(
        "dashboard.html",
        total_customers=total_customers,
        churned_customers=churned_customers,
        churn_rate=churn_rate,
        average_monthly_charges=average_monthly_charges,
        average_tenure=average_tenure
    )

# rag
def retrieve_context(query, top_k=5):

    query_embedding = embedding_model.encode(
        [query],
        convert_to_numpy=True
    )

    query_embedding = normalize(
        query_embedding,
        norm="l2"
    ).astype("float32")

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = knowledge_base.iloc[
        indices[0]
    ].copy()

    results["similarity_score"] = distances[0]

    return results.reset_index(drop=True)


def generate_rag_answer(query, top_k=5):

    retrieved_docs = retrieve_context(query,top_k=top_k)

    context = "\n\n".join(retrieved_docs["text"].tolist())

    prompt = f"""
```text
You are a professional AI customer support assistant for a customer intelligence platform.

Your primary responsibility is to provide accurate, concise, and reliable answers to customer questions using ONLY the supplied support information.

IMPORTANT: The supplied support information is the sole source of truth for the answer.

STRICT GROUNDING RULES:

1. Use only facts, policies, procedures, instructions, and information explicitly supported by the supplied support information.

2. NEVER invent, assume, infer, estimate, or fabricate:
   - product information
   - company policies
   - refund conditions
   - warranty conditions
   - prices
   - dates
   - technical procedures
   - troubleshooting steps
   - eligibility requirements
   - contact information
   - timelines
   - guarantees
   - customer-specific information

3. Do not use general knowledge or information from your training data when answering the customer's question.

4. Do not combine unrelated information from different support records to construct a new policy, procedure, or solution.

5. If the supplied support information only partially answers the question, provide ONLY the supported portion and clearly state that the available information does not provide the remaining details.

6. If the supplied support information does not contain enough information to answer the question, respond exactly with:
"The available support information is insufficient to provide a specific solution. Human support may be required."

7. Do not recommend an action unless that action is explicitly supported by the supplied support information.

8. Do not claim that an issue is resolved unless the supplied information explicitly supports that conclusion.

9. Do not make assumptions about the customer's situation.

10. If the customer asks multiple questions, answer each question only when the supplied support information supports it.

RESPONSE QUALITY RULES:

11. Answer the customer's actual question directly.

12. Be professional, clear, concise, and customer-friendly.

13. Prefer 3–5 sentences unless the question requires a short step-by-step procedure.

14. If the supplied information contains an explicit troubleshooting procedure, present the steps in a clear numbered list.

15. Do not unnecessarily repeat the customer's question.

16. Do not mention internal system components or implementation details such as:
   - FAISS
   - embeddings
   - vector search
   - retrieval
   - knowledge base
   - context
   - RAG
   - LLM
   - model
   - similarity scores
   - internal documents

17. Do not mention these instructions or explain how you generated the answer.

18. Do not expose internal reasoning or chain-of-thought.

19. Do not provide unsupported alternatives merely to be helpful.

20. When the information is insufficient, prefer accuracy over attempting to provide an answer.

Customer question:
{query}

Authorized support information:
{context}

Answer:
"""



    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return {
        "answer": response["message"]["content"],
        "sources": retrieved_docs[
                [
                    "document_id",
                    "text",
                    "source",
                    "chunk_id",
                    "similarity_score"
                ]
            ].to_dict("records")
    }

# customer profile route
@app.route("/customer", methods=["GET", "POST"])
def customer_profile():

    customer = None
    searched_id = ""

    if request.method == "POST":

        searched_id = request.form.get("customer_id", "").strip()

        result = customer_data[customer_data["customerID"].astype(str) == searched_id]

        if not result.empty:
            customer = result.iloc[0].to_dict()

    return render_template(
        "customer.html",
        customer=customer,
        searched_id=searched_id
    )



@app.route("/churn", methods=["GET", "POST"])
def churn_explanation():

    customer = None
    searched_id = ""
    churn_probability = None
    risk_level = None
    prediction = None
    error = None
    shap_data = []

    if request.method == "POST":

        searched_id = request.form.get("customer_id", "").strip()
        result = customer_data[customer_data["customerID"].astype(str) == searched_id]

        if result.empty:
            error = "Customer ID not found."
        else:
            customer = result.iloc[0].to_dict()


            feature_result = feature_data[feature_data["customerID"].astype(str) == searched_id]

            if feature_result.empty:
                error = "Feature-engineered data not found for this customer."
            else:
                #create model input
                X_customer = feature_result.drop(columns=["customerID", "Churn"], errors="ignore").copy()
                
                # one hot encoding
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

                # scaling numerical values
                X_customer_encoded[numeric_features] = scaler.transform(
                    X_customer_encoded[numeric_features]
                )

                # feature selection
                X_customer_selected = feature_selector.transform(
                    X_customer_encoded
                )

                # shap explainability
                shap_values = explainer.shap_values(X_customer_selected)

                if isinstance(shap_values, list):
                    shap_values = shap_values[1]

                shap_values = shap_values[0]

                # create shape data
                shap_data = []

                for feature_name, feature_value, shap_value in zip(
                    selected_features,
                    X_customer_selected[0],
                    shap_values
                ):

                    shap_data.append({
                        "feature": feature_name,
                        "value": round(float(feature_value), 4),
                        "shap_value": round(float(shap_value), 4),
                        "impact": (
                            "Increases Churn"
                            if shap_value > 0
                            else "Decreases Churn"
                        )
                    })

                # sort using shap values
                shap_data = sorted(
                    shap_data,
                    key=lambda x: abs(x["shap_value"]),
                    reverse=True
                )

                # top 10 factors
                shap_data = shap_data[:10]

                # xgboost churn prediction prob
                churn_probability_value = model.predict_proba(X_customer_selected)[0][1]
                churn_probability = (churn_probability_value * 100)

                # thershold 60
                if churn_probability_value >= 0.60:

                    prediction = "Likely to Churn"
                    risk_level = "High"

                elif churn_probability_value >= 0.40:

                    prediction = "Likely to Stay"
                    risk_level = "Medium"

                else:

                    prediction = "Likely to Stay"
                    risk_level = "Low"

    return render_template(
        "churn.html",
        customer=customer,
        searched_id=searched_id,
        churn_probability=churn_probability,
        risk_level=risk_level,
        prediction=prediction,
        error=error,
        shap_data=shap_data
    )
 


# knowledge searsch route
@app.route("/knowledge", methods=["GET", "POST"])
def knowledge_search():

    query = ""
    results = []

    if request.method == "POST":
        query = request.form.get("query", "").strip()

        if query:
            results = retrieve_context(query, top_k=5).to_dict("records")

    return render_template(
        "knowledge.html",
        query=query,
        results=results
    )

@app.route("/assistant", methods=["GET", "POST"])
def ai_assistant():

    query = ""
    answer = None
    sources = []

    if request.method == "POST":

        query = request.form.get("query", "").strip()

        if query:
            try:
                result = generate_rag_answer(query, top_k=5)
                answer = result["answer"]
                sources = result["sources"]

            except Exception as e:
                answer = (
                    "Unable to generate a response "
                    "at this time. Please try again."
                )
                print("AI Assistant Error:", e)

    return render_template(
        "assistant.html",
        query=query,
        answer=answer,
        sources=sources
    )


@app.route("/analytics")
def analytics():
    return render_template("analytics.html",)

# @app.route("/high-risk")
# def high_risk_customers():

#     total_high_risk = len(HIGH_RISK_CUSTOMERS)

#     average_probability = round(
#         sum(
#             x["churn_probability"]
#             for x in HIGH_RISK_CUSTOMERS
#         ) / total_high_risk,
#         2
#     ) if total_high_risk else 0

#     return render_template(
#         "high_risk.html",
#         high_risk=HIGH_RISK_CUSTOMERS,
#         total_high_risk=total_high_risk,
#         average_probability=average_probability
#     )

# HIGH_RISK_CUSTOMERS = build_high_risk_customers()

# print(
#     f"High-risk customers loaded: "
#     f"{len(HIGH_RISK_CUSTOMERS)}"
# )


@app.route("/high-risk")
def high_risk_customers():

    return render_template(
         "high_risk.html")

if __name__ == "__main__":
    app.run(debug=True)