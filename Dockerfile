FROM python:3.12-slim
WORKDIR /app
COPY . /app/
RUN pip install -r min-req.txt
EXPOSE 8501
ENTRYPOINT ["python", "-m", "streamlit", "run", "rag/rag_app.py"]