ARG PYTHON_VERSION=3.12-slim

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/
COPY . /code

RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

RUN python manage.py collectstatic --noinput
RUN chmod +x startup.sh

EXPOSE 8000
ENTRYPOINT ["./startup.sh"]

#CMD ["gunicorn","--bind",":8000","--workers","2","AutoWood_Backend.wsgi"]
#CMD ["python manage.py migrate"]


