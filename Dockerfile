FROM python:3.9
WORKDIR /app
ADD ../security_camera /app
RUN container/./run.sh
CMD container/./cmd.sh