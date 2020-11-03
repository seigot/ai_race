#!/bin/bash

HOME=/home/jetson

#function install_ros(){
#    cd $HOME
#    git clone https://github.com/karaage0703/jetson-nano-tools
#    cd jetson-nano-tools
#    ./install-ros-melodic.sh
#}

#function install_package(){
#    # joint state controller
#    sudo apt install -y ros-melodic-ros-control ros-melodic-ros-controllers  ros-melodic-joint-state-controller ros-melodic-effort-controllers ros-melodic-position-controllers ros-melodic-joint-trajectory-controller
#    # gazebo
#    sudo apt-get install -y gazebo9
#    sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'
#    wget http://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -
#    sudo apt-get update -y
#    sudo apt-get install -y ros-melodic-gazebo-ros-pkgs ros-melodic-gazebo-ros-control
#    echo "export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:~/ai_race/catkin_ws/src:~/ai_race/catkin_ws/src/sim_world/models" >> ~/.bashrc
#    export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:~/ai_race/catkin_ws/src:~/ai_race/catkin_ws/src/sim_world/models
#    # camera image
#    sudo apt-get install -y ros-melodic-uvc-camera
#    sudo apt-get install -y ros-melodic-image-*
#}

function setup_package(){
    echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc
    source /opt/ros/melodic/setup.bash
    cd $HOME
    git clone http://github.com/seigot/ai_race
    cd $HOME/ai_race/catkin_ws
    catkin_make
    source devel/setup.sh
}

#install_ros
#install_package
setup_package

#コンテナを起動し続ける
#tail -f /dev/null

