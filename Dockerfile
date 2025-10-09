FROM python:3.11

WORKDIR /app

COPY requirements.txt .

# Upgrade pip and install Python packages
RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel && \
    pip3 install --no-cache-dir -r requirements.txt

# Install Node.js and npm if needed
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . .

ENV FILE=config/docker-config.yaml

EXPOSE 8080

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8080", "main:app"]

