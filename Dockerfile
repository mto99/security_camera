FROM python:3.9
WORKDIR /app

RUN mkdir /app/security_camera

ADD container/ /app/security_camera/container/
ADD source/ /app/security_camera/source/
ADD requirements.txt /app/security_camera/

RUN /app/security_camera/container/./run.sh
CMD /app/security_camera/container/./cmd.sh