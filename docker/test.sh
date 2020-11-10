#!/bin/bash -x

# エラーが起こったら異常終了させる
set -E

function failure(){
    echo "error end!!"
    exit 1
}

# エラー発生時にコールする関数を設定 
trap failure ERR

function set_swap_file(){
    git clone https://github.com/JetsonHacksNano/installSwapfile
    cd installSwapfile
    ./installSwapfile.sh
    # SWAP領域が増えていることを確認
    free -mh
}

function install_basic_package(){
    sudo apt-get update
    sudo apt-get install -y net-tools git
    # install pyqt5 and NumPy
    sudo apt-get install -y python3-pip
    sudo apt-get install -y python3-pyqt5
    pip3 install --upgrade pip
    pip3 install numpy
}

function install_ros(){
    git clone https://github.com/karaage0703/jetson-nano-tools
    cd jetson-nano-tools
    ./install-ros-melodic.sh
    echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc
    source /opt/ros/melodic/setup.bash
}

function install_ros_related_packages(){
    # joint state controller, and ros package
    sudo apt install -y ros-melodic-ros-control ros-melodic-ros-controllers  ros-melodic-joint-state-controller ros-melodic-effort-controllers ros-melodic-position-controllers ros-melodic-joint-trajectory-controller
    # gazebo
    sudo apt-get install -y gazebo9
    sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'
    wget http://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -
    sudo apt-get update -y
    sudo apt-get install -y ros-melodic-gazebo-ros-pkgs ros-melodic-gazebo-ros-control
    echo "export GAZEBO_MODEL_PATH=:/home/jetson/catkin_ws/src/ai_race/ai_race:/home/jetson/catkin_ws/src/ai_race/ai_race/sim_world/models" >> ~/.bashrc
    export GAZEBO_MODEL_PATH=:/home/jetson/catkin_ws/src/ai_race/ai_race:/home/jetson/catkin_ws/src/ai_race/ai_race/sim_world/models
    # camera image
    sudo apt-get install -y ros-melodic-uvc-camera
    sudo apt-get install -y ros-melodic-image-*
}

function install_machine_learning_lib(){
    ### pytorch from pip image (v1.4)
    wget https://nvidia.box.com/shared/static/yhlmaie35hu8jv2xzvtxsh0rrpcu97yj.whl
    mv yhlmaie35hu8jv2xzvtxsh0rrpcu97yj.whl  torch-1.4.0-cp27-cp27mu-linux_aarch64.whl
    pip install torch-1.4.0-cp27-cp27mu-linux_aarch64.whl
    wget https://nvidia.box.com/shared/static/c3d7vm4gcs9m728j6o5vjay2jdedqb55.whl
    mv c3d7vm4gcs9m728j6o5vjay2jdedqb55.whl torch-1.4.0-cp36-cp36m-linux_aarch64.whl
    pip3 install torch-1.4.0-cp36-cp36m-linux_aarch64.whl

    ### torch vision (v0.2.2)
    pip install future
    pip install torchvision==0.2.2
    pip3 install future
    pip3 install torchvision==0.2.2

    ### torch2trt
    git clone https://github.com/NVIDIA-AI-IOT/torch2trt
    cd torch2trt
    python setup.py install
    python3 setup.py install

    ### sklearn python3
    pip3 install scikit-learn
    #pip3 install matplotlib
    #sudo apt-get -y install python3-tk

    ### pandas python2,3 (defaultを使えばよい)
    #pip3 install cython
    #pip3 install numpy
    #pip3 install -U pandas

    ### opencv python
    ### opencv python はソースからビルドする必要がある. 8～10時間ほど掛かる.
    cd ~
    git clone https://github.com/mdegans/nano_build_opencv
    cd nano_build_opencv
    ./build_opencv.sh 3.4.10
}

function setup_this_repository(){
    cd ~/catkin_ws/src
    git clone http://github.com/seigot/ai_race
    cd ~/catkin_ws
    catkin build
    source devel/setup.sh
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
install_basic_package
install_ros
install_ros_related_packages
install_machine_learning_lib
setup_this_repository
check_lib_version
echo "finish install"