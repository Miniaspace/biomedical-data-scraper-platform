FROM apache/airflow:2.8.1-python3.11

# Switch to root to install system dependencies
USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libffi-dev \
    libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Switch back to airflow user
USER airflow

# Copy requirements file
COPY requirements.txt /tmp/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Install Playwright browsers (if using dynamic rendering)
RUN playwright install chromium

# Set Python path to include project modules
ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow"

# Set default working directory
WORKDIR /opt/airflow
