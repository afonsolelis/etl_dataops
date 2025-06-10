FROM python:3.9-slim
WORKDIR /app
COPY src/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ .
COPY sample_data/ /data/
CMD ["python", "etl.py"]
