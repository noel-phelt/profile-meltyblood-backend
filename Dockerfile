FROM python:3.9-slim

WORKDIR /var/www

COPY ./src/requirements.txt .
RUN pip install --no-cache-dir --upgrade -r /var/www/requirements.txt

COPY ./src/ ./

# CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]