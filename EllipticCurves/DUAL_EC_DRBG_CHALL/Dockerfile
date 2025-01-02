FROM python:3.12-slim

WORKDIR /app

COPY chall.py .
COPY util.py .
COPY requirements.txt .
COPY flag.txt .

# Install necessary packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    socat \
    build-essential \
    libgmp-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 1337

CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:python3 chall.py"]
