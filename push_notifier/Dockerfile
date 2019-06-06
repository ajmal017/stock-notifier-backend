# Use an official Python runtime as a parent image
FROM python:3.7-slim

# Set the working directory to /server
WORKDIR /server

RUN pip install selenium

# set display port to avoid crash
ENV DISPLAY=:99

COPY push_notifier/requirements.txt /server

RUN pip install -r requirements.txt
RUN pip install awscli

COPY database.py /server
COPY scraper.py /server
COPY price_query.py /server
COPY notifications.py /server
COPY push_notifier/push_notifier.py /server
COPY push_notifier/start.sh /server

# Run server.py when the container launches
CMD ["/server/start.sh"]