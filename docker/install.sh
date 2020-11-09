#!/bin/bash

export HOME_JETSON=/home/jetson
source $HOME_JETSON/.bashrc

function setup_package(){
    cd $HOME_JETSON
    git clone http://github.com/seigot/ai_race
    pushd $HOME_JETSON/ai_race/catkin_ws
    catkin_make
    echo "source $HOME_JETSON/ai_race/catkin_ws/devel/setup.sh" >> $HOME_JETSON/.bashrc
    source devel/setup.sh
    popd
}

function setup_ai_race_env(){

    mkdir -p $HOME_JETSON/Images_from_rosbag

    # setup ai_race_data_sample
    cd $HOME_JETSON
    git clone http://github.com/seigot/ai_race_data_sample

    # delete unnecessary file
    #rm -fr $HOME_JETSON/catkin_ws # delete unnecessary directory..
}

setup_package
setup_ai_race_env

