#!/bin/bash

export HOME_JETSON=/home/jetson
source $HOME_JETSON/.bashrc

function setup_package(){
    cd $HOME_JETSON/catkin_ws/src
    git clone http://github.com/seigot/ai_race
    pushd $HOME_JETSON/catkin_ws
    catkin build
    echo "source $HOME_JETSON/catkin_ws/devel/setup.bash" >> $HOME_JETSON/.bashrc
    source devel/setup.sh
    popd
}

function setup_ai_race_env(){

    # general praparation
    mkdir -p $HOME_JETSON/Images_from_rosbag

    # setup ai_race_data_sample
    cd $HOME_JETSON
    git clone http://github.com/seigot/ai_race_data_sample
}

setup_package
setup_ai_race_env

