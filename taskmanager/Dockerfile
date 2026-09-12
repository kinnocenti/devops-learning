FROM python:3.12-slim-trixie

WORKDIR /app

RUN groupadd --gid 1000 appuser \
    && useradd --uid 1000 --gid 1000 appuser

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app.py /app/

COPY templates/ /app/templates/

COPY static/ /app/static/

USER appuser

CMD ["flask", "--app", "app", "run", "--host", "0.0.0.0", "--port", "5000"]