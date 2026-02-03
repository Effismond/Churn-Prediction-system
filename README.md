# Customer Churn Prediction System

An end-to-end **Machine Learning churn prediction project** featuring:
- 🚀 **FastAPI backend** for real-time predictions
- 📊 **Streamlit dashboard** for interactive analysis
- 🧠 Trained ML model for customer churn
- 📁 Clean, production-ready project structure

This project demonstrates **data science, ML engineering, and deployment readiness**

## 📌 Project Overview

Customer churn is a major business problem.  
This system predicts whether a customer is likely to churn and exposes predictions through:
- a **REST API**
- a **web-based dashboard**

## 🏗️ Project Structure

Churn_env-system/
│
├── api/
│ └── main.py # FastAPI application
│
├── models/
│ └── churn_model.pkl # Trained ML model
│
├── segmentation/
│ └── at_risk_customers.csv
│
├── streamlit_App.py # Streamlit dashboard
├── requirements.txt
├── README.md
└── .gitignore

## ⚙️ Tech Stack

- **Python**
- **FastAPI** – REST API
- **Streamlit** – Dashboard
- **Pandas / NumPy**
- **Scikit-learn**
- **Joblib**
- **Uvicorn**

uvicorn api.main:app --reload
API base URL:
👉 http://127.0.0.1:8000

Swagger Docs:
👉 http://127.0.0.1:8000/docs

Available Endpoints
GET / → Health check

GET /at-risk?limit=50 → At-risk customers

POST /predict → Churn prediction

🧪 Sample Prediction Request
POST /predict
{
  "tenure": 12,
  "monthly_charges": 70.5,
  "total_charges": 845.0
}

Sample Response
{
  "prediction": 1,
  "churn_probability": 0.78
}

📈 Key Features

✅ End-to-end ML pipeline
✅ API + UI separation (production-ready)
✅ Cached data & model loading
✅ Error handling with HTTP status codes
✅ Clean project structure
✅ Ready for cloud deployment

🚀 Future Improvements

Deploy FastAPI (Render / Railway)

Deploy Streamlit (Streamlit Cloud)

Add authentication

Model monitoring & logging

CI/CD with GitHub Actions

👤 Author

Effismond Augustine
Data Scientist / Machine Learning Engineer

📧 Email: effismond50@gmail.com
🔗 LinkedIn:www.linkedin.com/in/nnamnso-effiong-7a759132b
🐙 GitHub: Effismond