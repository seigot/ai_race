FROM nvcr.io/nvidia/l4t-ml:r32.4.4-py3
LABEL maintainer="seigot<s.takada.3o3@gmail.com>"

ENV DEBIAN_FRONTEND=noninteractive

# install basic package
RUN apt-get update && \
    apt-get install -yq wget curl git build-essential vim sudo lsb-release locales bash-completion tzdata \
    emacs \
    gnupg gnupg2 gnupg1 \
    gosu \
    unzip \
    less

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

# install python package
RUN sudo apt-get install -y python3-pip && \
    sudo apt-get install -y python-pip

# install pyqt5 and Numpy for timer
RUN sudo apt-get install -y python3-pip && \
    sudo apt-get install -y python3-pyqt5 && \
    pip3 install --upgrade pip && \
    pip3 install numpy

# pytorch
RUN pip --version && \
    pip3 --version
RUN wget https://nvidia.box.com/shared/static/c3d7vm4gcs9m728j6o5vjay2jdedqb55.whl && \
    mv c3d7vm4gcs9m728j6o5vjay2jdedqb55.whl torch-1.4.0-cp36-cp36m-linux_aarch64.whl && \
    pip3 install torch-1.4.0-cp36-cp36m-linux_aarch64.whl
RUN wget https://nvidia.box.com/shared/static/yhlmaie35hu8jv2xzvtxsh0rrpcu97yj.whl && \	
    mv yhlmaie35hu8jv2xzvtxsh0rrpcu97yj.whl torch-1.4.0-cp27-cp27mu-linux_aarch64.whl && \
    python -m pip install torch-1.4.0-cp27-cp27mu-linux_aarch64.whl

# torch vision
RUN sudo apt-get install -y libopenblas-base libopenmpi-dev && \
    sudo apt-get install -y libjpeg-dev zlib1g-dev && \
    python -m pip install 'pillow<7' && \
    python -m pip install future && \
    python -m pip install torchvision==0.2.2
    #pip3 install future && \
    #pip3 install torchvision==0.2.2

# torch2trt
RUN git clone https://github.com/NVIDIA-AI-IOT/torch2trt /tmp/torch2trt
#    gosu jetson python3 /tmp/torch2trt/setup.py install && \
#    gosu jetson python /tmp/torch2trt/setup.py install

# install opencv python3
RUN git clone https://github.com/mdegans/nano_build_opencv /tmp/nano_build_opencv
ADD build_opencv.patch /.
RUN patch -p0 < /build_opencv.patch && \
    cat /tmp/nano_build_opencv/build_opencv.sh && \
    gosu jetson /tmp/nano_build_opencv/build_opencv.sh 3.4.10

#USER jetson
#ENV HOME /home/jetson

# install & build this repository
ADD install.sh  /
RUN /install.sh

# install additional package
RUN apt-get update && \
    apt-get install -yq \
    	    net-tools \
	    openssh-server

ENTRYPOINT ["/start.sh"]
