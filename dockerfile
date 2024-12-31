FROM python:3.12.3-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app/ /app/
COPY ./app/volume_backend /app/volume_backend

EXPOSE 6001

CMD ["uvicorn","main:app", "--host", "0.0.0.0", "--port","6001"]

