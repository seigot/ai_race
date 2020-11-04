# ai_race
ai_race repository


## 1.準備

### 1.1 jetson起動

以下からイメージファイルを入手する。

```
Jetpack 4.3 Archive
https://developer.nvidia.com/jetpack-43-archive
 -> JetPack 4.3 - Installing JetPack:
 -> https://developer.nvidia.com/jetson-nano-sd-card-imager-3231
```

入手後、イメージファイルをSDカードに書き込んで、JetsonNanoに挿して起動する。


### 1.2 ROS(melodic)のインストール

terminalから以下を実行する。

```
git clone https://github.com/karaage0703/jetson-nano-tools
cd jetson-nano-tools
./install-ros-melodic.sh
```

参考 <br>
[Jetson NanoにROSをインストールする方法](https://qiita.com/karaage0703/items/aa54e086f0a2f165d3e9)


### 1.3 その他、パッケージのインストール

```
# joint state controller
sudo apt install -y ros-melodic-ros-control ros-melodic-ros-controllers  ros-melodic-joint-state-controller ros-melodic-effort-controllers ros-melodic-position-controllers ros-melodic-joint-trajectory-controller
# gazebo
sudo apt-get install -y gazebo9
sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'
wget http://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -
sudo apt-get update -y
sudo apt-get install -y ros-melodic-gazebo-ros-pkgs ros-melodic-gazebo-ros-control
echo "export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:~/ai_race/catkin_ws/src:~/ai_race/catkin_ws/src/sim_world/models" >> ~/.bashrc
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:~/ai_race/catkin_ws/src:~/ai_race/catkin_ws/src/sim_world/models
# camera image
sudo apt-get install -y ros-melodic-uvc-camera
sudo apt-get install -y ros-melodic-image-*
```

### 1.4 初期設定

```
echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc
source /opt/ros/melodic/setup.bash
cd ~
git clone http://github.com/seigot/ai_race
cd ~/ai_race/catkin_ws
catkin_make
source devel/setup.sh
```

* Docker環境

[こちら](docker/README.md)で検討中

## 2. サンプルコードの実行

### 2.1 コマンドからの実行手順

以下を実行して下さい（仮）

```
roslaunch tutorial1 wheel_robot.launch
roslaunch tutorial2 wheel_robot.launch
roslaunch tutorial3 wheel_robot.launch
roslaunch tutorial4 wheel_robot.launch
roslaunch tutorial5 wheel_robot.launch
roslaunch tutorial6 wheel_robot.launch
```

### 2.2 サンプルコードの説明

記載予定

### 2.3 審判サーバ

記載予定

```
# install pyqt5 and NumPy
sudo apt-get install -y python3-pip
sudo apt-get install -y python3-pyqt5
pip3 install --upgrade pip
pip3 install numpy
```

```
python3 judge/timer.py
```

## ルール

[こちら](document/rule.md)に記載予定

## FAQ

[こちら](document/FAQ.md)に記載予定

## 備考

記載予定

## 参考
[Jetson NanoにROSをインストールする方法](https://qiita.com/karaage0703/items/aa54e086f0a2f165d3e9)
