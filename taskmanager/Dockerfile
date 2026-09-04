FROM python:3.12-slim-trixie

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app.py templates/ static/ /app/

CMD ["flask", "--app", "app", "run"]