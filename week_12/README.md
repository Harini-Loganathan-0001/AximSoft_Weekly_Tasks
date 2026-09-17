# AI Customer Intelligence Platform

An end-to-end, lightweight AI Customer Intelligence Platform that combines customer analytics, churn prediction, explainable AI, customer-support text analysis, semantic search, Retrieval-Augmented Generation (RAG), and a locally running small language model.

The platform is designed for **CPU-first execution on low-end laptops**, without paid APIs, cloud-based LLM inference, or cloud vector databases.

## Project Overview

The AI Customer Intelligence Platform helps analyze customer behavior and provide intelligent customer-support insights through a unified local application.

The system integrates:

* Customer data analysis and EDA
* SQL-based customer analytics
* Data preprocessing and feature engineering
* Machine learning-based churn prediction
* Customer risk assessment
* SHAP-based explainability
* Customer-support ticket classification
* Sentence Transformer embeddings
* FAISS semantic search
* Knowledge-base retrieval
* Retrieval-Augmented Generation
* Local LLM inference
* Tool-based AI workflows
* Simple agent routing
* Flask web application
* System resource benchmarking

## Architecture

```text
Customer Data
      ↓
EDA
      ↓
SQL Analytics
      ↓
Data Preprocessing
      ↓
Feature Engineering
      ↓
Machine Learning
      ↓
Churn Prediction
      ↓
SHAP Explainability
      ↓
Customer Support Text
      ↓
NLP / TF-IDF
      ↓
Sentence Transformers
      ↓
FAISS Semantic Search
      ↓
Knowledge Base
      ↓
RAG
      ↓
Local Small LLM
      ↓
Tool Calling
      ↓
Simple Agent
      ↓
Flask Application
```

## Datasets

### Telco Customer Churn Dataset

The IBM Telco Customer Churn dataset is used for customer analytics and churn prediction.

Main information includes:

* Customer demographics
* Tenure
* Contract type
* Internet service
* Payment method
* Monthly charges
* Total charges
* Churn status

### Customer Support Ticket Dataset

The customer support dataset is used for:

* Support ticket text analysis
* Text classification
* Semantic search
* Knowledge retrieval
* RAG-based responses

## Project Structure

```text
week_12/
│
├── customer_env/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── knowledge_base/
│
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_sql_analysis.ipynb
│   ├── 03_preprocessing.ipynb
│   ├── 04_feature_engineering.ipynb
│   ├── 05_ml_models.ipynb
│   ├── 06_ann.ipynb
│   ├── 07_nlp.ipynb
│   ├── 08_embeddings_faiss.ipynb
│   └── 09_rag_llm.ipynb
│
├── src/
│   └── tools.py
│
├── models/
│
│
├── templates/
│
├── static/
│
├── app.py
├── requirements.txt
└── README.md
```

## Technologies Used

### Programming and Web

* Python
* Flask
* HTML
* CSS
* Bootstrap
* JavaScript

### Data Processing

* Pandas
* NumPy
* SQLite

### Machine Learning

* Scikit-learn
* XGBoost

### Explainable AI

* SHAP

### NLP

* TF-IDF
* Scikit-learn

### Semantic Search

* Sentence Transformers
* FAISS

### Generative AI

* Ollama
* Llama 3.2 3B

## Machine Learning

Several classification algorithms were evaluated for customer churn prediction, including:

* Logistic Regression
* Decision Tree
* K-Nearest Neighbors
* Random Forest
* Gradient Boosting
* XGBoost

The final churn model uses **XGBoost with feature selection and a classification threshold of 0.60**.

### Final Model Performance

| Metric    |  Score |
| --------- | -----: |
| Accuracy  | 0.7814 |
| Precision | 0.5714 |
| Recall    | 0.7059 |
| F1 Score  | 0.6316 |
| ROC-AUC   | 0.8403 |
| PR-AUC    | 0.6635 |

## Feature Engineering

Additional customer features were created to improve customer intelligence and churn analysis.

Important engineered features include:

* TenureGroup
* NumberOfServices
* IsDSL
* IsFiberOptic
* NoInternet
* MonthlyChargesGroup
* TotalChargesGroup
* ChargeToTenureRatio
* HighValueCustomer
* HighRiskCustomer
* InternetTechSupport

The processed dataset is stored as:

```text
data/processed/feature_engineered_customers.csv
```

## Explainable AI

SHAP is used to explain individual customer churn predictions.

For each customer, the platform provides:

* Churn probability
* Risk level
* Prediction
* Top contributing features
* SHAP values
* Churn-increasing factors
* Churn-decreasing factors

The application displays the **Top 10 SHAP factors** for individual customers.

## NLP and Semantic Search

Customer-support text is processed using NLP techniques.

The NLP pipeline includes:

```text
Support Tickets
      ↓
Text Preprocessing
      ↓
TF-IDF
      ↓
Text Classification
```

For semantic search:

```text
Knowledge Base
      ↓
Text Chunks
      ↓
Sentence Transformer
      ↓
Embeddings
      ↓
FAISS
```

The embedding model used is:

```text
all-MiniLM-L6-v2
```

## Knowledge Base

The business knowledge base contains support information related to areas such as:

* Technical support
* Installation
* Warranty
* Product support
* Customer service

The processed knowledge base contains:

```text
137 chunks
384-dimensional embeddings
```

FAISS is used for efficient similarity search.

## Retrieval-Augmented Generation

The RAG pipeline retrieves relevant business information before generating an answer.

```text
User Query
    ↓
Embedding Generation
    ↓
FAISS Search
    ↓
Top Relevant Documents
    ↓
Grounded Prompt
    ↓
Local LLM
    ↓
Final Response
```

The RAG system is designed to answer using only the available business-support information and avoid unsupported information.

When sufficient information is unavailable, the system returns:

```text
The available support information is insufficient to provide a specific solution. Human support may be required.
```

## Local LLM

The project uses a locally running:

```text
Llama 3.2 3B
```

through Ollama.

The LLM is used for generating grounded support responses and does **not** perform the customer churn prediction itself.

## Tool-Based AI Workflow

The platform provides the following tools:

### Customer Profile Tool

Retrieves customer information using a customer ID.

### Churn Prediction Tool

Returns:

* Churn prediction
* Churn probability
* Classification threshold

### SHAP Explanation Tool

Returns the most important factors influencing an individual customer's churn prediction.

### Business Knowledge Search Tool

Searches the business knowledge base using semantic similarity.

### RAG Answer Tool

Generates a grounded response using retrieved business information.

## Simple Agent

A lightweight rule-based agent routes user queries to the appropriate tool.

```text
User Query
    ↓
Query Classification
    ↓
Tool Selection
    ↓
Tool Execution
    ↓
Response
```

The agent supports:

* Customer profile requests
* Churn prediction requests
* Churn explanation requests
* Business knowledge searches
* RAG support questions

The agent was evaluated using 10 test queries and achieved:

```text
Routing Accuracy: 100%
```

## Flask Application

The system is integrated into a Flask web application.

Main application modules include:

* Dashboard
* Customer Profile
* Churn Prediction
* Explainable AI
* Knowledge Search
* RAG
* AI Assistant

The dashboard provides an overview of customer statistics and machine-learning performance.

## Resource Benchmarking

The complete system was benchmarked to understand its suitability for CPU-based execution.

| Component            |      Time |
| -------------------- | --------: |
| Model Loading        |  0.0111 s |
| ML Inference         |  0.0130 s |
| Embedding Generation |  0.0432 s |
| FAISS Search         |  0.0030 s |
| RAG Retrieval        |  0.0497 s |
| LLM Inference        |  9.1795 s |
| End-to-End Response  | 11.2063 s |

Observed RAM usage remained approximately:

```text
370–381 MB
```

The benchmark showed that ML inference, embeddings, and FAISS retrieval require relatively little time, while local LLM inference is the main contributor to the overall response time.

## Installation

Clone the project:

```bash
git clone <repository-url>
cd week_12
```

Create the Python environment:

```bash
python -m venv customer_env
```

Activate the environment on Windows:

```powershell
customer_env\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the Flask application:

```bash
python app.py
```

Open the application in the browser:

```text
http://127.0.0.1:5000
```

## Running Jupyter Notebooks

The notebooks can be launched using:

```powershell
customer_env\Scripts\python.exe -m notebook
```

The notebooks should be executed in the following order:

```text
01_eda.ipynb
02_sql_analysis.ipynb
03_preprocessing.ipynb
04_feature_engineering.ipynb
05_ml_models.ipynb
06_ann.ipynb
07_nlp.ipynb
08_embeddings_faiss.ipynb
09_rag_llm.ipynb
```

## System Requirements

The platform is designed for lightweight local execution.

Recommended:

* Python 3.11+
* 8 GB RAM or more
* CPU-based execution
* Windows, macOS, or Linux
* Ollama for local LLM execution

A dedicated GPU is not required for the final application.

## Design Goals

The project focuses on:

* Local execution
* Low resource usage
* Explainable predictions
* Grounded AI responses
* Modular architecture
* No paid APIs
* No cloud LLM inference
* No cloud vector database
* Practical deployment on low-end systems

## Limitations

* Local LLM inference can increase response time on CPU-only systems.
* Churn predictions depend on the available customer dataset and trained model.
* RAG responses are limited to information available in the business knowledge base.
* The system is intended as a customer intelligence and support assistant, not as an autonomous decision-making system.

## Conclusion

The AI Customer Intelligence Platform integrates traditional machine learning, explainable AI, NLP, semantic search, RAG, and local generative AI into a single lightweight application.

The system provides customer analytics, churn prediction, individual prediction explanations, support knowledge retrieval, and grounded AI assistance while maintaining a CPU-first and locally executable architecture.

The completed platform demonstrates how multiple AI components can be combined into a practical customer intelligence solution suitable for resource-constrained environments.
