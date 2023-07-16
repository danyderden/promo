FROM python:3.11.3-alpine
WORKDIR /app


RUN python3 -m pip install --user --upgrade pip
RUN apk add gcc musl-dev libffi-dev
RUN pip install poetry

COPY . /app

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --without test

RUN alembic upgrade head

CMD ["poetry", "run", "gunicorn", "main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]