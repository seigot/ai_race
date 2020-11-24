FROM nvidia/cuda:10.1-cudnn7-devel-ubuntu18.04
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

#USER jetson
ENV HOME /home/jetson

# install additional package
RUN apt-get update && \
    apt-get install -yq \
    	    net-tools \
	    openssh-server \
	    x11-apps

#RUN  git clone https://github.com/seigot/ai_race_data_sample /home/ubuntu/ai_race_data_sample
#RUN  sudo ln -s /home/ubuntu /home/jetson

# install ROS/package/python package/pyqt5.../pygame
# pytorch/torchvision/torch3trt/opencv3..
# from ai_race script
RUN  touch /tmp/test
#RUN  sudo apt upgrade -y libignition-math2
# auto setup
RUN  git clone https://github.com/seigot/ai_race /tmp/ai_race
RUN  /tmp/ai_race/scripts/setup/auto_setup_for_Linux.sh

# gnome-terminal
RUN apt-get install -yq dbus-x11; \
    echo 'eval `dbus-launch --sh-syntax`' >> /home/jetson/.bashrc

# command
COPY start.sh  /tmp/.
RUN  chmod +x /tmp/start.sh
ENTRYPOINT ["/tmp/start.sh"]

