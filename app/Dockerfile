FROM python:3.12-slim

# Installer quelques dépendances système

RUN apt-get update && apt-get install -y \
    build-essential libpq-dev gcc \
    libnss3 libxss1 libasound2 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
    libdrm2 libxrandr2 libgbm1 libxcomposite1 libxdamage1 libxfixes3 \
    libxext6 libglib2.0-0 libgtk-3-0 curl wget gnupg \
    && rm -rf /var/lib/apt/lists/*


RUN pip install playwright && playwright install

WORKDIR /app
# Copier le code
# COPY . /app

# Installer dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt



EXPOSE 9090

CMD ["python", "/app/app.py"]
