# Use a more compatible base image
FROM python:3.10-slim

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y \
    curl \
    unzip \
    jq \
    libx11-dev \
    libxcomposite1 \
    libxrandr2 \
    libxcursor1 \
    libnss3 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    xvfb \
    bash \
    build-essential \
    libffi-dev \
    python3-dev && \
    apt-get clean

# Install selenium
RUN pip install --no-cache-dir selenium

# Set download URLs and paths
ENV LATEST_STABLE_JSON="https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"
ENV DOWNLOAD_PATH_CHROME_LINUX="/opt/chrome-headless-shell-linux.zip"
ENV DOWNLOAD_PATH_CHROME_DRIVER_LINUX="/opt/chrome-driver-linux.zip"
ENV CHROME_DIR="/opt/chrome"
ENV DRIVER_DIR="/opt/chrome-driver"

# Retrieve the Chrome and ChromeDriver URLs, download, and install them
RUN json_data=$(curl -s "$LATEST_STABLE_JSON") && \
    latest_chrome_linux_download_url=$(echo "$json_data" | jq -r ".channels.Stable.downloads.chrome[0].url") && \
    latest_chrome_driver_linux_download_url=$(echo "$json_data" | jq -r ".channels.Stable.downloads.chromedriver[0].url") && \
    mkdir -p "$CHROME_DIR" "$DRIVER_DIR" && \
    curl -Lo "$DOWNLOAD_PATH_CHROME_LINUX" "$latest_chrome_linux_download_url" && \
    unzip -q "$DOWNLOAD_PATH_CHROME_LINUX" -d "$CHROME_DIR" && \
    rm -rf "$DOWNLOAD_PATH_CHROME_LINUX" && \
    curl -Lo "$DOWNLOAD_PATH_CHROME_DRIVER_LINUX" "$latest_chrome_driver_linux_download_url" && \
    unzip -q "$DOWNLOAD_PATH_CHROME_DRIVER_LINUX" -d "$DRIVER_DIR" && \
    rm -rf "$DOWNLOAD_PATH_CHROME_DRIVER_LINUX"

# Clean up unnecessary dependencies and files
RUN rm -rf /var/lib/apt/lists/*

# Set environment variables for Chrome and Chromedriver
ENV CHROME_BIN="/opt/chrome/chrome"
ENV CHROME_DRIVER="/opt/chrome-driver/chromedriver"

# Add the Python script to the Docker container
COPY scraper.py /opt/scraper.py

# Set the default command to run your Python script
CMD ["python", "/opt/scraper.py"]
