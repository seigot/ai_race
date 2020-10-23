# ai_race
ai_race repository


## 準備

### ROS(melodic)のインストール

記載予定

### その他、パッケージのインストール

記載予定

```
sudo apt install -y ros-melodic-ros-control ros-melodic-ros-controllers  ros-melodic-joint-state-controller ros-melodic-effort-controllers ros-melodic-position-controllers ros-melodic-joint-trajectory-controller
```

### 初期設定

記載予定

```
rm -r ~/catkin_ws
mkdir -p ~/catkin_ws/src
cd catkin_ws/src
git clone http://github.com/seigot/ai_race
cd catkin_ws/src
catkin_make
source devel/setup.sh
```

### 起動

記載予定

```
roslaunch tutrual1 wheel_robot.launch
```

### サンプルコードの実行

記載予定

## 備考

記載予定
