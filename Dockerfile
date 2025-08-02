FROM python:3.13

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

# Düzgün netcat versiyasını əlavə et
RUN apt-get update && apt-get install -y netcat-openbsd

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
