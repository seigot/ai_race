FROM nvcr.io/nvidia/l4t-ml:r32.4.4-py3
LABEL maintainer="seigot<s.takada.3o3@gmail.com>"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -yq wget curl git build-essential vim sudo lsb-release locales bash-completion tzdata && \
    apt-get install -yq emacs && \
    apt-get install -yq gnupg gnupg2 gnupg1 && \
    apt-get install -yq gosu

# Replace 1000 with your user / group id
RUN export uid=1000 gid=1000 && \
    mkdir -p /home/jetson && \
    echo "jetson:x:${uid}:${gid}:JETSON,,,:/home/jetson:/bin/bash" >> /etc/passwd && \
    echo "jetson:x:${uid}:" >> /etc/group && \
    echo "jetson ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/jetson && \
    chmod 0440 /etc/sudoers.d/jetson && \
    chown ${uid}:${gid} -R /home/jetson

# install ROS
RUN git clone https://github.com/karaage0703/jetson-nano-tools /tmp/jetson-nano-tools && \
    gosu jetson /tmp/jetson-nano-tools/install-ros-melodic.sh

# install package
RUN sudo apt install -y ros-melodic-ros-control ros-melodic-ros-controllers  ros-melodic-joint-state-controller ros-melodic-effort-controllers ros-melodic-position-controllers ros-melodic-joint-trajectory-controller && \
    sudo apt-get install -y gazebo9 && \
    sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list' && \
    wget http://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add - && \
    sudo apt-get update -y && \
    sudo apt-get install -y ros-melodic-gazebo-ros-pkgs ros-melodic-gazebo-ros-control && \
    echo "export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/home/jetson/ai_race/catkin_ws/src:/home/jetson/ai_race/catkin_ws/src/sim_world/models" >> /home/jetson/.bashrc && \
    export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/home/jetson/ai_race/catkin_ws/src:/home/jetson/ai_race/catkin_ws/src/sim_world/models && \
    sudo apt-get install -y ros-melodic-uvc-camera && \
    sudo apt-get install -y ros-melodic-image-*

#USER jetson
#ENV HOME /home/jetson

ADD install.sh  /
RUN /install.sh
ADD start.sh /
ENTRYPOINT ["/start.sh"]
