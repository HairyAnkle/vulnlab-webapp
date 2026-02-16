FROM python:3.12-slim

WORKDIR /srv/app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN flask --app run.py init-db || true

EXPOSE 5000
CMD ["python", "run.py"]
