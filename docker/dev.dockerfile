FROM python:3.11-slim

ARG ENVIRONMENT

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements/${ENVIRONMENT}.requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install -y libpq-dev gcc
RUN pip install --no-cache-dir -r /app/requirements.txt

ADD src /app/

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "api.wsgi"]