FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*
COPY . /app/
RUN pip3 install -r min-req.txt
EXPOSE 8501
ENTRYPOINT ["python", "-m", "streamlit", "run", "rag/rag_app.py"]