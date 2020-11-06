# ai_race
機械学習を学ぶことを目的とした、AIで車両を操作して走行タイムを競うゲームです。 <br>
<br>
## 1. 準備

### 1.0. jetson nano準備

記載予定 <br>
[こちら](https://qiita.com/seigot/items/115e25d0ae7149047760)にjetson nanoの備品を記載<br>
（シミュレータや機械学習は通常のPCでできなくもないが、環境統一のため、以降の環境構築や動作確認はjetson nanoを基準に行う） <br>

### 1.1. jetson起動

以下からイメージファイルを入手する。 <br>
 <br>
Jetpack 4.4.1が良いと思われる（検証中） <br>

```
Jetpack 4.4.1
https://developer.nvidia.com/embedded/jetpack
```

以下は、Jetpack 4.3 Archive

```
Jetpack 4.3 Archive
https://developer.nvidia.com/jetpack-43-archive
 -> JetPack 4.3 - Installing JetPack:
 -> https://developer.nvidia.com/jetson-nano-sd-card-imager-3231
```

入手後、イメージファイルをSDカードに書き込んで、JetsonNanoに挿して起動する。<br>
起動後、ネットワークに接続する。<br>

- SWAPファイル追加
初回起動時に[[Jetson Nano関係のTIPSまとめ Swapファイルの設定](https://qiita.com/karaage0703/items/b14c249aa33112669ee4)]を参考に、SWAPファイル6GB追加 <br>

```
git clone https://github.com/JetsonHacksNano/installSwapfile
cd installSwapfile
./installSwapfile.sh
```

メモリ追加されていることを以下コマンドで確認

```
free -mh
```

### 1.2. ROS(melodic)のインストール

terminalから以下を実行する。

```
git clone https://github.com/karaage0703/jetson-nano-tools
cd jetson-nano-tools
./install-ros-melodic.sh
```

参考 <br>
[Jetson NanoにROSをインストールする方法](https://qiita.com/karaage0703/items/aa54e086f0a2f165d3e9)


### 1.3. その他、パッケージのインストール

- ROS関連のパッケージ

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

- 機械学習用ライブラリ（仮）

```
# opencv
--#pip3 install -U pip--
--#python3 -m pip install opencv-python--
# ### opencv はソースからビルドする必要があるみたいなので確認中
# git clone https://github.com/mdegans/nano_build_opencv
# cd nano_build_opencv
# ./build_opencv.sh 3.4.10

# sklearn
#pip3 install scikit-learn
#pip3 install matplotlib
#sudo apt-get -y install python3-tk
# pytorch v1.6
# tensorflow
# pandas
```

- ライブラリバージョン <br>
<br>
検証環境（マスター） <br>

|  ライブラリ  |  バージョン  |
| ---- | ---- |
|  pytorch  |  1.3  |
|  sklearn  |  0.19.1  |
|  pandas  |  1.1.3  |
|  cv2  |  3.4.10  |

検証環境（マスター追従のテスト用１） <br>

|  ライブラリ  |  バージョン  |
| ---- | ---- |
|  pytorch  |  1.6.0  |
|  sklearn  |  0.23.2  |
|  pandas  |  0.22.0(1.1.3必須かも)  |
|  cv2  |  xxx(3.4.10必須かも)  |

### 1.4. 初期設定

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

### 2.1. コマンドからの実行手順

以下を実行して下さい（仮）

```
roslaunch tutorial1 wheel_robot.launch
roslaunch tutorial2 wheel_robot.launch
roslaunch tutorial3 wheel_robot.launch
roslaunch tutorial4 wheel_robot.launch
roslaunch tutorial5 wheel_robot.launch
roslaunch tutorial6 wheel_robot.launch
```

### 2.2. サンプルコードの説明

記載予定

シミュレータ起動

```
ex.)
bash scripts/prepare.sh
```

学習

```
ex.)
bash scripts/start.sh 1
```

推論

```
ex.)
bash scripts/start.sh 2
```

### 2.3. 走行タイム計測器

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

## 3. ルール

[こちら](document/rule.md)に記載予定

## FAQ

[こちら](document/FAQ.md)に記載予定

## 備考

記載予定

## 参考
[Jetson NanoにROSをインストールする方法](https://qiita.com/karaage0703/items/aa54e086f0a2f165d3e9) <br>
[Jetson Nano関係のTIPSまとめ Swapファイルの設定](https://qiita.com/karaage0703/items/b14c249aa33112669ee4) <br>
[NVIDIA Jetson Nanoで OpenCV 3をビルドしてインストールする方法、NVCaffe等の OpenCV 4未対応を動かす](http://www.neko.ne.jp/~freewing/raspberry_pi/nvidia_jetson_nano_build_opencv_3410/) <br>
[https://github.com/mdegans/nano_build_opencv](https://github.com/mdegans/nano_build_opencv) <br>

## Finnaly

~~ HAVE FUN ! ~~
