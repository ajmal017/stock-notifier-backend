# Use an official Python runtime as a parent image
FROM python:3.7-slim

# Set the working directory to /server
WORKDIR /server

RUN pip install selenium

# set display port to avoid crash
ENV DISPLAY=:99

COPY push_notifier/requirements.txt /server

RUN pip install -r requirements.txt

COPY database.py /server
COPY scraper.py /server
COPY price_query.py /server
COPY push_notifier/push_notifier.py /server
COPY keys.py /server

# Run server.py when the container launches
CMD ["python", "push_notifier.py", "['AMD', 'GOOG', 'NFLX', 'AAPL']"]