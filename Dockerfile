FROM python:3.9-slim

RUN pip install fastapi uvicorn

EXPOSE 80

COPY ./app /app

RUN pip install -r app/requirements.txt

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]