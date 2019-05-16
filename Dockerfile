# Use an official Python runtime as a parent image
FROM python:3.7-slim

RUN apt-get update && \
    apt-get -y install build-essential && \
    apt-get -y install m4 && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory to /server
WORKDIR /server

# Copy the server python files into the server directory
COPY server.py /server
COPY server_login.py /server

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

# Run server.py when the container launches
CMD ["python", "server.py"]