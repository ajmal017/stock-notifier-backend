# Stock Notifier Backend

This repository is for the backed of the stock notifier. It is a set of docker containers of the different modules of the program.

The login architecture depends on GMP and libsodium, with zip files included.

## Build

The server has 4 parts, 3 which run continuously and 1 on the intialization of the server

To bulid the database adder, run

```sudo docker build -t stock_adder -f batch_inserter/Dockerfile .```


To bulid the database updater, run

```sudo docker build -t stock_updater -f sr_updater/Dockerfile .```


To bulid the push notifier, run

```sudo docker build -t push_notifier -f push_notifier/Dockerfile .```


To build the http server, run

```sudo docker build -t http_server -f Dockerfile .```

## Run

All components are made to run on AWS