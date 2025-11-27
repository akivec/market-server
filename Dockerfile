FROM python:3.11-slim

WORKDIR /app

COPY server.py /app/server.py
COPY apks /apks

EXPOSE 80

CMD ["python", "server.py"]

