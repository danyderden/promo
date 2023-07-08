FROM python:3.11.3
COPY . /app
WORKDIR /app


RUN python3 -m pip install --user --upgrade pip && \
    python3 -m pip install -r req.txt

RUN alembic upgrade head

CMD gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000