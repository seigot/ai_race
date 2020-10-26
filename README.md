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

記載予定

```
sudo apt install -y ros-melodic-ros-control ros-melodic-ros-controllers  ros-melodic-joint-state-controller ros-melodic-effort-controllers ros-melodic-position-controllers ros-melodic-joint-trajectory-controller
sudo apt-get install -y gazebo9
sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'
wget http://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -
sudo apt-get update
sudo apt-get install ros-melodic-gazebo-ros-pkgs ros-melodic-gazebo-ros-control
```

### 1.4 初期設定

記載予定

```
source /opt/ros/melodic/setup.bash
echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc
rm -r ~/catkin_ws
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src
git clone http://github.com/seigot/ai_race
cd ~/catkin_ws
catkin_make
source devel/setup.sh
```

## 2. サンプルコードの実行

### 2.1 コマンドからの実行手順

以下を実行して下さい（仮）

```
roslaunch tutrual1 wheel_robot.launch
```

### 2.2 サンプルコードの説明

記載予定

### 審判サーバ

記載予定

## 3. 備考

記載予定

## 参考
[Jetson NanoにROSをインストールする方法](https://qiita.com/karaage0703/items/aa54e086f0a2f165d3e9)
