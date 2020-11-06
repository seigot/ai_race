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

- SWAPファイル追加【必須】 <br>
初回起動時に[[Jetson Nano関係のTIPSまとめ Swapファイルの設定](https://qiita.com/karaage0703/items/b14c249aa33112669ee4)]を参考に、SWAPファイル6GB追加 <br>

```
git clone https://github.com/JetsonHacksNano/installSwapfile
cd installSwapfile
./installSwapfile.sh
```

メモリ追加されていることを以下コマンドで確認

```
free -mh
# SWAP領域が増えていることを確認
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

python3用ライブラリ

```
# opencv python2,3
# ### opencv python はソースからビルドする必要がある
cd ~
git clone https://github.com/mdegans/nano_build_opencv
cd nano_build_opencv
./build_opencv.sh 3.4.10

# sklearn python3
#pip3 install scikit-learn
#pip3 install matplotlib
#sudo apt-get -y install python3-tk
# tensorflow python2,3
# pandas python2,3
# pip3 install cython
# pip3 install numpy
# pip3 install -U pandas

# pytorch v1.4 python2,3
### pytorch
wget https://nvidia.box.com/shared/static/c3d7vm4gcs9m728j6o5vjay2jdedqb55.whl
mv c3d7vm4gcs9m728j6o5vjay2jdedqb55.whl torch-1.4.0-cp36-cp36m-linux_aarch64.whl
pip3 install torch-1.4.0-cp36-cp36m-linux_aarch64.whl
wget https://nvidia.box.com/shared/static/yhlmaie35hu8jv2xzvtxsh0rrpcu97yj.whl
mv yhlmaie35hu8jv2xzvtxsh0rrpcu97yj.whl  torch-1.4.0-cp27-cp27mu-linux_aarch64.whl
pip install torch-1.4.0-cp27-cp27mu-linux_aarch64.whl
### torch vision
pip install future
pip install torchvision
### torch2trt
git clone https://github.com/NVIDIA-AI-IOT/torch2trt
cd torch2trt
python setup.py install
```

- ライブラリバージョン <br>
<br>
検証環境（マスター） <br>

|  ライブラリ  |  バージョン(python3)  |　 バージョン(python)  |
| ---- | ---- | ---- |
|  pytorch  |  1.3  |  -  |
|  torchvision  |  -  |  -  |
|  sklearn  |  0.19.1  |  -  |
|  pandas  |  1.1.3  |  -  |
|  cv2  |  3.4.10  |  -  |

検証環境（マスター追従のテスト用１） <br>

|  ライブラリ  |  バージョン(python3)  |　 バージョン(python)  |
| ---- | ---- | ---- |
|  pytorch  |  ~~1.6.0~~ 1.4.0  |  1.4.0  |
|  torchvision  |  0.2.2  |  0.2.2  |
|  sklearn  |  0.23.2  |  -  |
|  pandas  |  0.22.0 ~~(1.1.3必須かも)~~  |  -  |
|  cv2  |  3.4.10  |  3.4.10   |

参考 <br>
[pytorchとtensoflowのバージョンをコマンドラインから調べる](https://qiita.com/seigot/items/0b81f601e5c9e30d0e46) <br>

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
<br>
ROS動作確認用（仮） <br>

```
roslaunch tutorial1 wheel_robot.launch
roslaunch tutorial2 wheel_robot.launch
roslaunch tutorial3 wheel_robot.launch
roslaunch tutorial4 wheel_robot.launch
roslaunch tutorial5 wheel_robot.launch
roslaunch tutorial6 wheel_robot.launch
```

機械学習の動作確認用（仮） <br>

```
## rosbag取得
roslaunch user_tutorial1 wheel_robot.launch
roslaunch user_tutorial1 rosbag.launch output_path:=/home/ubuntu
rqt # robot steering -> v,rad指定

## rosbag --> image/command 変換
cd ~/ai_race/catkin_ws/src/utility/scripts
mkdir -p /Images_from_rosbag
sudo chmod 777 /Images_from_rosbag
python rosbag_to_images_and_commands.py **.bag   # bagファイルから画像とコマンドを取得
python listup_all_rosbag_timestamp.py *.bag               # 時刻表示できる

## 学習 
cd learning (学習用フォルダへ移動) 
python3 train.py --data_csv <csvのパス> --model_name <保存するモデル名>  
#### 以下のような形式でモデルファイルが保存されます
ls ~/ai_race/catkin_ws/srcexperiments/models/checkpoints/sim_race_test.model_epoch=*.pth

## 推論(trtなし trt=比較的軽量なモデル) 
roscd user_tutorial2/scripts 
python inference_from_image.py --pretrained_model <学習させたモデル>  

## 推論(trtあり） 
#### 準備（準備は最初の一回でOK） 
python3 inference_from_image.py --trt_conversion --pretrained_model <学習させたモデル> --trt_model <保存するtrtモデル名>   
#### 実行 
python inference_from_image.py --trt_module --trt_model <保存したtrtモデル名> 
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
[PyTorch for Jetson](https://forums.developer.nvidia.com/t/pytorch-for-jetson-version-1-7-0-now-available/72048) <br>

## Finnaly

~~ HAVE FUN ! ~~
