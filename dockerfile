FROM python:3.9-slim

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install streamlit==1.29.0 xgboost==2.0.1 requests pydantic

COPY src/app/streamlit_app.py /app/streamlit_app.py
COPY data/sample.json /app/data/sample.json
COPY src/data_models /app/src/data_models

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
