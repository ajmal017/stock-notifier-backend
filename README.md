# Stock Notifier Backend

This repository is for the backed of the stock notifier. It is a set of docker containers of the different modules of the program.

The login architecture depends on GMP and libsodium, with zip files included.

## Build

The server has 4 parts, 3 which run continuously and 1 on the intialization of the server

## Run
  
Run with "docker run -p: 8000:8000 stock_server"

