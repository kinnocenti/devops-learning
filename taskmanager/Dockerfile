FROM python:3.12-slim-trixie

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app.py /app/

COPY templates/ /app/templates/

COPY static/ /app/static/

CMD ["flask", "--app", "app", "run", "--host", "0.0.0.0", "--port", "5000"]