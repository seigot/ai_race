FROM nvcr.io/nvidia/l4t-ml:r32.4.4-py3
LABEL maintainer="seigot<s.takada.3o3@gmail.com>"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -yq wget curl git build-essential vim sudo lsb-release locales bash-completion tzdata && \
    apt-get install -yq emacs vi

# Replace 1000 with your user / group id
RUN export uid=1000 gid=1000 && \
    mkdir -p /home/jetson && \
    echo "jetson:x:${uid}:${gid}:JETSON,,,:/home/jetson:/bin/bash" >> /etc/passwd && \
    echo "jetson:x:${uid}:" >> /etc/group && \
    echo "jetson ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/jetson && \
    chmod 0440 /etc/sudoers.d/jetson && \
    chown ${uid}:${gid} -R /home/jetson

USER jetson
ENV HOME /home/jetson

ADD  start.sh  /
RUN  chmod +x /start.sh
RUN  /start.sh
