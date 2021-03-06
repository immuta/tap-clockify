FROM python:3.8-slim

RUN apt-get update && apt-get install -y gcc libssl-dev
RUN mkdir -p /opt/code
WORKDIR /opt/code

ADD . tap-clockify
RUN pip install -r tap-clockify/requirements.txt
RUN pip install ./tap-clockify

CMD [ "python", "tap-clockify/docker-entrypoint.py" ]
