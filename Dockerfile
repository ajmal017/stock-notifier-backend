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

# Copy the server python files into the server directory
COPY server.py /server
COPY server_login.py /server

COPY requirements.txt /server

RUN pip install -r requirements.txt

# Add C libraries
RUN mkdir /clibs

# GMP
ADD gmp-6.1.2.tar.xz /clibs/
RUN cd /clibs/gmp-6.1.2/ &&  ./configure --prefix=$HOME/.local && \
    make && make install
RUN rm -rf /clibs/gmp-6.1.2

# libSodium
ADD libsodium-1.0.16.tar.gz /clibs/
RUN cd /clibs/libsodium-1.0.16/ &&  ./configure --prefix=$HOME/.local && \
    make && make install
RUN rm -rf /clibs/libsodium-1.0.16

ENV LD_LIBRARY_PATH "/root/.local/lib:$LD_LIBRARY_PATH"

# Server Login
RUN mkdir /clibs/server_login
COPY server_login.cpp /clibs/server_login
COPY server_login.h /clibs/server_login
COPY Makefile /clibs/server_login
RUN cd /clibs/server_login && make && echo $(ls) && mv server_lib.so /server

# Make port 8099 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME World

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
RUN rm /tmp/chromedriver.zip

RUN pip install selenium

# set display port to avoid crash
ENV DISPLAY=:99

COPY database.py /server
COPY scraper.py /server


# Run server.py when the container launches
CMD ["python", "server.py"]