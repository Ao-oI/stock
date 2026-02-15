FROM python:3.11-slim

# Set environment keys
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ=Asia/Shanghai

# Install system dependencies and tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    make \
    wget \
    tar \
    libpq-dev \
    cron \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

# Install TA-Lib C library
WORKDIR /tmp
RUN wget --no-check-certificate http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    cd .. && \
    rm -rf ta-lib ta-lib-0.4.0-src.tar.gz

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
# Install numpy first for TA-Lib
RUN pip install --no-cache-dir numpy==2.4.1 || pip install --no-cache-dir numpy
RUN pip install --no-cache-dir -r requirements.txt

# Copy cron configuration
COPY deployment/stock-cron /etc/cron.d/stock-cron
RUN chmod 0644 /etc/cron.d/stock-cron && \
    crontab /etc/cron.d/stock-cron

# Copy start script
COPY deployment/start.sh .
RUN chmod +x start.sh && dos2unix start.sh

# Copy project files
COPY . .

# Expose port
EXPOSE 9988

CMD ["./start.sh"]
