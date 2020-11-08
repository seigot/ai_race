#!/bin/bash

export HOME=/home/jetson

function setup_package(){
    cd $HOME
    git clone http://github.com/seigot/ai_race
    cd $HOME/ai_race/catkin_ws
    catkin_make
    echo "$HOME/ai_race/catkin_ws/devel/setup.sh" >> $HOME/.bashrc
    source devel/setup.sh
}

function setup_ai_race_env(){
    mkdir -p $HOME/Images_from_rosbag
}

setup_package
setup_ai_race_env

