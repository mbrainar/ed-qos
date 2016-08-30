##
## Dockerfile for Event Driven QoS
##
FROM python:2-alpine
MAINTAINER Steven Luzynski <sluzynsk@cisco.com>

RUN pip install --no-cache-dir setuptools wheel

ADD . /app
WORKDIR /app
RUN pip install --requirement /app/requirements.txt
ENV FLASK_APP=app.py
CMD ["flask", "initdb"]
CMD ["flask", "run"]
