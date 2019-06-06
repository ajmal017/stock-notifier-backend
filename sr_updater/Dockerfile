# Use an official Python runtime as a parent image
FROM python:3.7-slim

RUN apt-get update && \
    apt-get -y install build-essential && \
    apt-get -y install m4 && \
    apt-get -y install wget && \
    apt-get -y install curl && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory to /server
WORKDIR /server

# Make port 5000 available to the world outside this container
EXPOSE 4444

# Define environment variable
ENV NAME World

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ && rm /tmp/chromedriver.zip

RUN pip install selenium

# set display port to avoid crash
ENV DISPLAY=:99

COPY sr_updater/requirements.txt /server

RUN pip install -r requirements.txt

COPY database.py /server
COPY scraper.py /server
COPY price_query.py /server
COPY sr_updater/sr_updater.py /server

# Run server.py when the container launches
CMD ["python", "sr_updater.py", "['AMD', 'LOVE', 'SLAB', 'AAPL', 'GOOG', 'SYMC', 'FB', 'TSLA', 'QCOM']"]