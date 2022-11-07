#!/bin/bash

img_name = "sec_cam:latest"

#check if img exists
if ! [[ $(docker images | grep $img_name) ]]
then
    exit -1
fi

#start container
docker run -d -p 5000:5000 -v ../:/app --name security_camera $img_name
