FROM python:3.11.3
COPY . /app
WORKDIR /app


RUN python3 -m pip install --user --upgrade pip && \
    python3 -m pip install -r req.txt

RUN alembic upgrade head

CMD ["python", "main.py"]