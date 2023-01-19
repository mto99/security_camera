FROM debian:latest
WORKDIR /app



RUN apt-get update
RUN apt-get -y install --no-install-recommends \
	gcc \
	g++ \
	gfortran \
	libopenblas-dev \
	libblas-dev \
	liblapack-dev \
	libatlas-base-dev \
	libhdf5-dev \
	libhdf5-100 \
	pkg-config \
	python3 \
	python3-dev \
	python3-pip \
	python3-setuptools \
	pybind11-dev \
	wget
  
RUN apt-get install -y git

RUN python3 -m pip install --upgrade pip

RUN apt install -y libopencv-dev python3-opencv

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get install python-opencv -y

RUN git clone https://github.com/mto99/security_camera.git
RUN chmod 777 source/*

CMD python3 /app/source/app.py
