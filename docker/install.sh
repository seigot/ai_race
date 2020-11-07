#!/bin/bash

HOME=/home/jetson

function setup_package(){
    echo "source /opt/ros/melodic/setup.bash" >> $HOME/.bashrc
    source /opt/ros/melodic/setup.bash
    cd $HOME
    git clone http://github.com/seigot/ai_race
    cd $HOME/ai_race/catkin_ws
    catkin_make
    source devel/setup.sh
}

function setup_ai_race_env(){
    mkdir -p $HOME/Images_from_rosbag
}

setup_package
setup_ai_race_env

