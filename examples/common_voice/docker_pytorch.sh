#! /bin/bash

clear
echo "Building docker image"
sudo docker build -t dehoyos/common_voice .

echo "Initializing docker container"
sudo docker run -it \
  --net="host"\
  --privileged \
  --rm \
  --shm-size=8gb \
  --gpus all \
  -v /:/workspace \
  -p 8888:8889 -p 8000:8001 dehoyos/common_voice:latest /bin/bash

