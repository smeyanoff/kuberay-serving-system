# app/Dockerfile

FROM python:3.9-slim

WORKDIR /app

RUN pip3 install streamlit==1.29.0 requests==2.3.0 pydantic==1.10

COPY src/app/streamlit_app.py /app/streamlit_app.py
COPY data/sample.json /app/data/sample.json
COPY src/data_models /app/data_models

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
