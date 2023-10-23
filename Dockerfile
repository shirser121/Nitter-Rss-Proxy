FROM python:3.11

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./rss_proxy /app/rss_proxy
COPY ./.env /app/.env

CMD ["uvicorn", "rss_proxy.main:app", "--host", "0.0.0.0", "--port", "3010", "--proxy-headers"]