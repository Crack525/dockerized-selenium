# Use the official Python image with a specific version for compatibility
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies
RUN apt-get update -y && apt-get install -y wget xvfb unzip jq curl \
x11vnc libxi6 libgconf-2-4 ffmpeg


# Install Google Chrome dependencies
RUN apt-get install -y libxss1 libappindicator1 libgconf-2-4 \
    fonts-liberation libasound2 libnspr4 libnss3 libx11-xcb1 libxtst6 lsb-release xdg-utils \
    libgbm1 libnss3 libatk-bridge2.0-0 libgtk-3-0 libx11-xcb1 libxcb-dri3-0


# Fetch the latest version numbers and URLs for Chrome and ChromeDriver
RUN curl -s https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json > /tmp/versions.json

RUN CHROME_URL=$(jq -r '.channels.Stable.downloads.chrome[] | select(.platform=="linux64") | .url' /tmp/versions.json) && \
    wget -q --continue -O /tmp/chrome-linux64.zip $CHROME_URL && \
    unzip /tmp/chrome-linux64.zip -d /opt/chrome

RUN chmod +x /opt/chrome/chrome-linux64/chrome


RUN CHROMEDRIVER_URL=$(jq -r '.channels.Stable.downloads.chromedriver[] | select(.platform=="linux64") | .url' /tmp/versions.json) && \
    wget -q --continue -O /tmp/chromedriver-linux64.zip $CHROMEDRIVER_URL && \
    unzip /tmp/chromedriver-linux64.zip -d /opt/chromedriver && \
    chmod +x /opt/chromedriver/chromedriver-linux64/chromedriver

# Set up Chromedriver Environment variables
ENV CHROMEDRIVER_DIR /opt/chromedriver
ENV PATH $CHROMEDRIVER_DIR:$PATH

# Set Chrome Environment variables
#ENV CHROME_BIN /opt/chrome/chrome-linux64/chrome

# Expose the X11 forwarding port
EXPOSE 6000

# Set up Chrome to run in non-headless mode
ENV DISPLAY=:99

# Ensure that the "reports" directory exists for output
RUN mkdir -p reports

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
COPY . .

# Command to run the tests
#CMD ["pytest", "tests/test_twitch.py"]

# Command to run the tests with pytest and generate an HTML report
#CMD ["pytest", "--html=reports/report.html", "--self-contained-html", "features"]

# Then, in your entrypoint or command, start Xvfb
CMD ["sh", "-c", "Xvfb :99 -ac & DISPLAY=:99 pytest --html=reports/report.html --self-contained-html features"]

# Command to run Xvfb and capture screen with ffmpeg
#CMD ["sh", "-c", "Xvfb :99 -ac & DISPLAY=:99 pytest --html=reports/report.html --self-contained-html features && ffmpeg -y -f x11grab -video_size 412x914 -i :99 -r 25 /app/reports/screen_recording.gif"]