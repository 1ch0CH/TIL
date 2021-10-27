# Docker
- 211027 Docker를 사용하게 된 이유 : a-loam을 사용하기 위해서 : a loam의 ros-kinetic-perception version에는 rviz가 없는듯? -> 확인 해보자
## Docker 사용 시 sudo 없이 사용하기

> sudo usermod -aG docker [현재 사용자]
- usermod : 사용자 속성을 변경하는 명령어
- G(== --groups) : 새로운 그룹을 말한다
- a(== --append) : 다른 그룹에서 삭제없이 G 옵션에 따른 그룹에 사용자를 추가한다.


## Docker 에 local folder 연결하기


# A-Loam
## [참고](https://hub.docker.com/r/celinachild/loam) 를 통한 docker 명령어 알기

```
(1) Install docker
(2) Install nvidia-docker
(3) Ready for GUI visualization

$ sudo apt-get install x11-xserver-utils
$ xhost +
How to run
$ docker pull celinachild/loam:latest

$ docker run --gpus all -it --ipc=host --net=host --privileged -e DISPLAY=unix$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:rw -e NVIDIA_DRIVER_CAPABILITIES=all celinachild/loam:latest /bin/bash

$ cd /home/catkin_ws/

$ source ./devel/setup.bash

$ roslaunch aloam_velodyne aloam_velodyne_VLP_16.launch
```

## Dockerfile
```
FROM ros:kinetic-perception

ENV CERES_VERSION="1.12.0"
ENV PCL_VERSION="1.8.0"
ENV CATKIN_WS=/root/catkin_ws

    # setup processors number used to compile library
RUN if [ "x$(nproc)" = "x1" ] ; then export USE_PROC=1 ; else export USE_PROC=$(($(nproc)/2)) ; fi && \
    # Install dependencies
      apt-get update && apt-get install -y \
      cmake \
      libatlas-base-dev \
      libeigen3-dev \
      libgoogle-glog-dev \
      libsuitesparse-dev \
      python-catkin-tools \
      ros-${ROS_DISTRO}-cv-bridge \
      ros-${ROS_DISTRO}-image-transport \
      ros-${ROS_DISTRO}-message-filters \
      ros-${ROS_DISTRO}-tf && \
    rm -rf /var/lib/apt/lists/* && \
    # Build and install Ceres
    git clone https://ceres-solver.googlesource.com/ceres-solver && \
    cd ceres-solver && \
    git checkout tags/${CERES_VERSION} && \
    mkdir build && cd build && \
    cmake .. && \
    make -j${USE_PROC} install && \
    cd ../.. && \
    rm -rf ./ceres-solver && \
    # Build and install pcl
    git clone https://github.com/PointCloudLibrary/pcl.git && \
    cd pcl && \
    git checkout tags/pcl-${PCL_VERSION} && \
    mkdir build && cd build && \
    cmake .. && \
    make -j${USE_PROC} install && \
    cd ../.. && \
    rm -rf ./pcl && \
    # Setup catkin workspace
    mkdir -p $CATKIN_WS/src/A-LOAM/
    
# WORKDIR $CATKIN_WS/src

# Copy A-LOAM
COPY ./ $CATKIN_WS/src/A-LOAM/
# use the following line if you only have this dockerfile
# RUN git clone https://github.com/HKUST-Aerial-Robotics/A-LOAM.git

# Build A-LOAM
WORKDIR $CATKIN_WS
ENV TERM xterm
ENV PYTHONIOENCODING UTF-8
RUN catkin config \
      --extend /opt/ros/$ROS_DISTRO \
      --cmake-args \
        -DCMAKE_BUILD_TYPE=Release && \
    catkin build && \
    sed -i '/exec "$@"/i \
            source "/root/catkin_ws/devel/setup.bash"' /ros_entrypoint.sh
```
## run.sh
```
#!/bin/bash
trap : SIGTERM SIGINT

function abspath() {
    # generate absolute path from relative path
    # $1     : relative filename
    # return : absolute path
    if [ -d "$1" ]; then
        # dir
        (cd "$1"; pwd)
    elif [ -f "$1" ]; then
        # file
        if [[ $1 = /* ]]; then
            echo "$1"
        elif [[ $1 == */* ]]; then
            echo "$(cd "${1%/*}"; pwd)/${1##*/}"
        else
            echo "$(pwd)/$1"
        fi
    fi
}

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 LIDAR_SCAN_NUMBER" >&2
  exit 1
fi

roscore &
ROSCORE_PID=$!
sleep 1

rviz -d ../rviz_cfg/aloam_velodyne.rviz &
RVIZ_PID=$!

A_LOAM_DIR=$(abspath "..")

if [ "$1" -eq 16 ]; then
    docker run \
    -it \
    --rm \
    --net=host \
    -v ${A_LOAM_DIR}:/root/catkin_ws/src/A-LOAM/ \
    ros:aloam \
    /bin/bash -c \
    "cd /root/catkin_ws/; \
    catkin config \
        --cmake-args \
            -DCMAKE_BUILD_TYPE=Release; \
        catkin build; \
        source devel/setup.bash; \
        roslaunch aloam_velodyne aloam_velodyne_VLP_16.launch rviz:=false"
elif [ "$1" -eq "32" ]; then
    docker run \
    -it \
    --rm \
    --net=host \
    -v ${A_LOAM_DIR}:/root/catkin_ws/src/A-LOAM/ \
    ros:aloam \
    /bin/bash -c \
    "cd /root/catkin_ws/; \
    catkin config \
        --cmake-args \
            -DCMAKE_BUILD_TYPE=Release; \
        catkin build; \
        source devel/setup.bash; \
        roslaunch aloam_velodyne aloam_velodyne_HDL_32.launch rviz:=false"
elif [ "$1" -eq "64" ]; then
    docker run \
    -it \
    --rm \
    --net=host \
    -v ${A_LOAM_DIR}:/root/catkin_ws/src/A-LOAM/ \
    ros:aloam \
    /bin/bash -c \
    "cd /root/catkin_ws/; \
    catkin config \
        --cmake-args \
            -DCMAKE_BUILD_TYPE=Release; \
        catkin build; \
        source devel/setup.bash; \
        roslaunch aloam_velodyne aloam_velodyne_HDL_64.launch rviz:=false"
fi

wait $ROSCORE_PID
wait $RVIZ_PID

if [[ $? -gt 128 ]]
then
    kill $ROSCORE_PID
    kill $RVIZ_PID
fi
```

# tmux
- tmux 이용해서 bind 하자!

```
$ sudo apt install tmux
```
## 단축키
- <Ctrl+b> >> % : 나누기
- [참고](https://dgkim5360.tistory.com/entry/the-first-steps-for-tmux-terminal-multiplexer)
