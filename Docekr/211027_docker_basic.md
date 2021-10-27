# Docker
## Docker 사용 시 sudo 없이 사용하기

> sudo usermod -aG docker [현재 사용자]
- usermod : 사용자 속성을 변경하는 명령어
- G(== --groups) : 새로운 그룹을 말한다
- a(== --append) : 다른 그룹에서 삭제없이 G 옵션에 따른 그룹에 사용자를 추가한다.


## Docker 에 local folder 연결하기



# [참고](https://hub.docker.com/r/celinachild/floam-ssl) 를 통한 docker 명령어

```
(1) Install docker
(2) Install nvidia-docker
(3) Ready for GUI visualization

$ sudo apt-get install x11-xserver-utils
$ xhost +local:
How to run
$ docker pull celinachild/floam-ssl

$ docker run --gpus all -it --ipc=host --net=host --privileged -e DISPLAY=unix$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:rw -e NVIDIA_DRIVER_CAPABILITIES=all celinachild/floam-ssl /bin/bash

$ cd /home/catkin_ws/

$ source ./devel/setup.bash

$ roslaunch floam_ssl floam_ssl_mapping.launch
```
