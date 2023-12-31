FROM python:3.8
COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt
COPY ./db.sql /docker-entrypoint-initdb.d/
COPY ./app /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload", "--reload-dir", "/app"]