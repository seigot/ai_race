#!/bin/bash -x

# エラーが起こったら異常終了させる
set -E

function failure(){
    echo "error end!!"
    exit 1
}

# エラー発生時にコールする関数を設定 
trap failure ERR

#DEBIAN_FRONTEND=noninteractive

function setup_swap_file(){
    cd ~
    if [ -d "./installSwapfile" ]; then
	echo "skip"
	return 0
    fi
    git clone https://github.com/JetsonHacksNano/installSwapfile
    cd installSwapfile
    ./installSwapfile.sh
    # SWAP領域が増えていることを確認
    free -mh
}

function install_basic_package(){
    sudo apt-get update
    sudo apt-get install -y net-tools git
    sudo apt-get install -y python-pip
    # install pyqt5 and NumPy
    sudo apt-get install -y python3-pip
    sudo apt-get install -y python3-pyqt5
    pip3 install --upgrade pip
    pip3 install numpy
    # for judge server
    pip3 install flask
    pip3 install requests
    python -m pip install requests
    # pygame
    sudo apt-get update -y
    sudo apt-get install -y libsdl-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev
    sudo apt-get install -y libsmpeg-dev libportmidi-dev libavformat-dev libswscale-dev
    sudo apt-get install -y libfreetype6-dev
    sudo apt-get install -y libportmidi-dev
    sudo pip3 install pgzero
    python -m pip install pygame==1.9.6
    # scikit learn
    sudo apt install -y gfortran
}

function install_ros(){
    # check if already install ros
    if [ ! -z `rosversion -d` ];then
	echo "ros already installed, skip install ros"
	return 0
    fi

    cd ~
    sudo rm -rf jetson-nano-tools
    git clone https://github.com/karaage0703/jetson-nano-tools
    cd jetson-nano-tools
    ./install-ros-melodic.sh
    echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc
    source /opt/ros/melodic/setup.bash
}

function install_ros_related_packages(){
    # joint state controller, and ros package
    sudo apt install -y ros-melodic-ros-control ros-melodic-ros-controllers  ros-melodic-joint-state-controller ros-melodic-effort-controllers ros-melodic-position-controllers ros-melodic-joint-trajectory-controller
    sudo apt install ros-melodic-cob-srvs
    # gazebo
    sudo apt-get install -y gazebo9
    sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'
    wget http://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -
    sudo apt-get update -y
    sudo apt-get install -y ros-melodic-gazebo-ros-pkgs ros-melodic-gazebo-ros-control
    echo "export GAZEBO_MODEL_PATH=:${HOME}/catkin_ws/src/ai_race/ai_race:${HOME}/catkin_ws/src/ai_race/ai_race/sim_world/models" >> ~/.bashrc
    export GAZEBO_MODEL_PATH=:${HOME}/catkin_ws/src/ai_race/ai_race:${HOME}/catkin_ws/src/ai_race/ai_race/sim_world/models
    # camera image
    sudo apt-get install -y ros-melodic-uvc-camera
    sudo apt-get install -y ros-melodic-image-*
}

function install_torch(){
    ### pytorch from pip image (v1.4)
    wget https://nvidia.box.com/shared/static/yhlmaie35hu8jv2xzvtxsh0rrpcu97yj.whl -O torch-1.4.0-cp27-cp27mu-linux_aarch64.whl
    sudo apt-get install -y python-pip libopenblas-base libopenmpi-dev
    python -m pip install torch-1.4.0-cp27-cp27mu-linux_aarch64.whl
    wget https://nvidia.box.com/shared/static/c3d7vm4gcs9m728j6o5vjay2jdedqb55.whl -O torch-1.4.0-cp36-cp36m-linux_aarch64.whl
    sudo apt-get install -y python3-pip libopenblas-base libopenmpi-dev
    pip3 install torch-1.4.0-cp36-cp36m-linux_aarch64.whl
}

function install_torchvision(){
    ### torch vision (v0.2.2)
    # https://forums.developer.nvidia.com/t/pytorch-for-jetson-version-1-7-0-now-available/72048
    pip install future
    pip3 install future
    sudo apt-get install libjpeg-dev zlib1g-dev libpython3-dev libavcodec-dev libavformat-dev libswscale-dev

    cd ~
    sudo rm -rf torchvision
    git clone --branch v0.5.0 https://github.com/pytorch/vision torchvision
    cd torchvision
    export BUILD_VERSION=0.2.2
    sudo python setup.py install
    sudo python3 setup.py install
    cd ../
    pip install 'pillow<7'
    
    #pip install future
    #pip install torchvision==0.2.2
    #pip3 install future
    #pip3 install torchvision==0.2.2
}

function install_torch2trt(){
    ### torch2trt
    cd ~
    sudo rm -rf torch2trt
    git clone https://github.com/NVIDIA-AI-IOT/torch2trt
    cd torch2trt
    git checkout d1fa6f9f20c6c4c57a9486680ab38c45d0d94ec3
    sudo python setup.py install
    sudo python3 setup.py install
}

function install_sklearn(){
    ### sklearn python3
    pip3 install scikit-learn
    #pip3 install matplotlib
    #sudo apt-get -y install python3-tk
}

function install_numpy(){
    echo "skip"
    ### pandas python2,3 (defaultを使えばよい)
    #pip3 install cython
    #pip3 install numpy
    #pip3 install -U pandas
}

function install_opencv(){
    ### opencv python
    ### opencv python はソースからビルドする必要がある. 8～10時間ほど掛かる.
    cd ~
    sudo rm -rf nano_build_opencv
    git clone https://github.com/mdegans/nano_build_opencv
    cd nano_build_opencv
    yes | ./build_opencv.sh 3.4.10
}

function setup_this_repository(){
    mkdir -p ~/Images_from_rosbag
    cd ~/catkin_ws/src

    if [ -d "./ai_race" ]; then
	echo "skip ai_race directory already exist.."
	return 0
    fi
    echo "clone sample repository.."
    git clone http://github.com/seigot/ai_race
    cd ~/catkin_ws
    catkin build
    source devel/setup.bash
    echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
}

function check_lib_version(){
    python3 -c 'import torch; print(torch.__version__) '
    python3 -c "import torchvision;print(torchvision.__version__);"
    python3 -c "import cv2 ;print(cv2.__version__);"
    python3 -c "import sklearn;print(sklearn.__version__);"
    python3 -c "import pandas as pd ;print(pd.__version__);"
    python -c 'import torch; print(torch.__version__) '
    python -c "import torchvision;print(torchvision.__version__);"
    python -c "import cv2 ;print(cv2.__version__);"
}

echo "start install"
setup_swap_file
install_basic_package
install_ros
install_ros_related_packages
install_torch
install_torchvision
install_torch2trt
install_sklearn
install_numpy
install_opencv
setup_this_repository
check_lib_version
echo "finish install"
