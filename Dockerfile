FROM python:3.9
WORKDIR /app

RUN mkdir /app/security_camera

ADD container /app/security_camera
ADD source /app/security_camera

RUN container/./run.sh
CMD container/./cmd.sh