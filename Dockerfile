FROM python:3.12.2-alpine
WORKDIR /app
COPY main.py requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT /app/main.py
