@echo off
echo Activating conda environment...
call conda activate Churn_env

echo Running ML pipeline...
python pipelines/1_ingest.py
python pipelines/2_preprocess.py
python pipelines/3_train.py
python pipelines/4_predict.py

echo Running KPIs & segmentation...
python analytics/churn_kpis.py
python segmentation/customer_intelligence.py

echo Starting FastAPI...
start cmd /k uvicorn api.main:app --reload

echo Starting Streamlit...
start cmd /k streamlit run App/streamlit_App.py

pause