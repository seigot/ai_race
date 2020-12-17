FROM nvcr.io/nvidia/l4t-ml:r32.4.4-py3
LABEL maintainer="seigot<s.takada.3o3@gmail.com>"

ENV DEBIAN_FRONTEND=noninteractive

# update
RUN apt-get update ;\
    apt-get -y upgrade ;\
    apt-get install -yq wget curl git build-essential vim sudo lsb-release locales bash-completion tzdata gosu

# environment setting
#RUN locale-gen en_US.UTF-8
#ENV LANG en_US.UTF-8
#ENV LANGUAGE en_US:en
#ENV LC_ALL en_US.UTF-8
RUN locale-gen ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:jp
ENV LC_ALL ja_JP.UTF-8

# Replace 1000 with your user / group id
RUN export uid=1000 gid=1000 && \
    mkdir -p /home/jetson && \
    echo "jetson:x:${uid}:${gid}:JETSON,,,:/home/jetson:/bin/bash" >> /etc/passwd && \
    echo "jetson:x:${uid}:" >> /etc/group && \
    echo "jetson ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/jetson && \
    chmod 0440 /etc/sudoers.d/jetson && \
    chown ${uid}:${gid} -R /home/jetson

# install basic package
RUN apt-get update && \
    apt-get install -yq \
    emacs \
    terminator \
    gnupg gnupg2 gnupg1 \
    unzip \
    less \
    gnome-terminal

# install ROS
RUN git clone https://github.com/karaage0703/jetson-nano-tools /tmp/jetson-nano-tools && \
    gosu jetson /tmp/jetson-nano-tools/install-ros-melodic.sh && \
    echo "source /opt/ros/melodic/setup.bash" >> /home/jetson/.bashrc

# install package
RUN sudo apt install -y ros-melodic-ros-control ros-melodic-ros-controllers  ros-melodic-joint-state-controller ros-melodic-effort-controllers ros-melodic-position-controllers ros-melodic-joint-trajectory-controller && \
    sudo apt install ros-melodic-cob-srvs && \
    sudo apt-get install -y gazebo9 && \
    sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list' && \
    wget http://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add - && \
    sudo apt-get update -y && \
    sudo apt-get install -y ros-melodic-gazebo-ros-pkgs ros-melodic-gazebo-ros-control && \
    echo "export GAZEBO_MODEL_PATH=:/home/jetson/catkin_ws/src/ai_race/ai_race:/home/jetson/catkin_ws/src/ai_race/ai_race/sim_world/models" >> /home/jetson/.bashrc && \
    sudo apt-get install -y ros-melodic-uvc-camera && \
    sudo apt-get install -y ros-melodic-image-*

# install python package
RUN sudo apt-get install -y python3-pip && \
    sudo apt-get install -y python-pip

# install pyqt5 and Numpy for timer
RUN sudo apt-get install -y python3-pip && \
    sudo apt-get install -y python3-pyqt5 && \
    pip3 install --upgrade pip && \
    pip3 install numpy && \
    pip3 install flask && \
    pip3 install requests && \
    python -m pip install requests

# pygame
RUN apt-get update -y && \
    apt-get install -y libsdl-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev && \
    apt-get install -y libsmpeg-dev libportmidi-dev libavformat-dev libswscale-dev && \
    apt-get install -y libfreetype6-dev && \
    apt-get install -y libportmidi-dev && \
    pip3 install pgzero && \
    python -m pip install pygame==1.9.6

# scikit learn
RUN sudo apt install -y gfortran

# pytorch
RUN pip --version && \
    pip3 --version
RUN wget https://nvidia.box.com/shared/static/c3d7vm4gcs9m728j6o5vjay2jdedqb55.whl && \
    mv c3d7vm4gcs9m728j6o5vjay2jdedqb55.whl torch-1.4.0-cp36-cp36m-linux_aarch64.whl && \
    pip3 install torch-1.4.0-cp36-cp36m-linux_aarch64.whl && \
    rm torch-1.4.0-cp36-cp36m-linux_aarch64.whl
RUN wget https://nvidia.box.com/shared/static/yhlmaie35hu8jv2xzvtxsh0rrpcu97yj.whl && \	
    mv yhlmaie35hu8jv2xzvtxsh0rrpcu97yj.whl torch-1.4.0-cp27-cp27mu-linux_aarch64.whl && \
    python -m pip install torch-1.4.0-cp27-cp27mu-linux_aarch64.whl && \
    rm torch-1.4.0-cp27-cp27mu-linux_aarch64.whl

# torch vision
RUN sudo apt-get install -y libopenblas-base libopenmpi-dev && \
    sudo apt-get install -y libjpeg-dev zlib1g-dev && \
    python -m pip install 'pillow<7' && \
    python -m pip install future && \
    python -m pip install torchvision==0.2.2 && \
    pip3 install future && \
    pip3 install torchvision==0.2.2

# torch2trt
RUN git clone https://github.com/NVIDIA-AI-IOT/torch2trt /tmp/torch2trt
#    gosu jetson python3 /tmp/torch2trt/setup.py install && \
#    gosu jetson python /tmp/torch2trt/setup.py install

# install opencv python3
RUN git clone https://github.com/mdegans/nano_build_opencv /tmp/nano_build_opencv
COPY build_opencv.patch /tmp/.
RUN patch -p0 < /tmp/build_opencv.patch && \
    cat /tmp/nano_build_opencv/build_opencv.sh && \
    yes | gosu jetson /tmp/nano_build_opencv/build_opencv.sh 3.4.10

#USER jetson
ENV HOME /home/jetson

# gnome-terminal
RUN apt-get install -yq dbus-x11; \
    echo 'eval `dbus-launch --sh-syntax`' >> /home/jetson/.bashrc

# install additional package
RUN apt-get update && \
    apt-get install -yq \
    	    net-tools \
	    openssh-server

# install & build this repository
COPY install.sh /tmp/.
RUN /tmp/install.sh

COPY start.sh  /tmp/.
ENTRYPOINT ["/tmp/start.sh"]
