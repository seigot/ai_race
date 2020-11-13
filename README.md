# ai_race
機械学習を学ぶことを目的とした、AIで車両を操作して走行タイムを競うゲームです。 <br>
<br>
## 1. 準備

### 1.0. jetson nano準備

記載予定 <br>
[こちら](https://qiita.com/seigot/items/115e25d0ae7149047760)にjetson nanoの備品を記載<br>
（シミュレータや機械学習は通常のPCでできなくもないが、環境統一のため、以降の環境構築や動作確認はjetson nanoを基準に行う） <br>

### 1.1. jetson nano起動

以下からイメージファイルを取得する。 <br>
 <br>
Jetpack 4.4.1 以降を推奨 <br>

```
Jetpack 4.4.1
https://developer.nvidia.com/embedded/jetpack
```

取得後、イメージファイルをSDカードに書き込んで、JetsonNanoに挿して起動する。<br>
起動後、ネットワークに接続する。<br>

```
* お勧め設定 
ユーザ名: jetson
パスワード: (任意)
# お勧め設定は、順次追記予定。ユーザ名を共通化するとフルパス指定が要る時にハマる確率が減る。
```

* SWAPファイル追加してメモリ増強【必須】 <br>

```
cd ~
git clone https://github.com/JetsonHacksNano/installSwapfile
cd installSwapfile
./installSwapfile.sh
# SWAP領域が増えていることを確認
free -mh
```

* 学習用データ、学習モデル【参考】

[こちら](https://github.com/seigot/ai_race_data_sample)にsampleデータを置いています。運営の動作確認用です。

* Docker環境【参考】

[こちら](docker/README.md)にDocker環境の利用手順を置いています。運営の動作確認用です。

## 2. インストール

結構時間が掛かります。<br>
[こちら](https://github.com/seigot/ai_race/blob/main/scripts/setup/README.md)で、以下 2.1.～2.4. を自動実行するスクリプトを作成 <br>
とりあえず動かしたい方は[こちら](docker/README.md)のDocker環境をお試し頂いてもOKです。 <br>
「#」から始まる行はコメントです。 <br>

### 2.1. 基本的なパッケージをインストール <br>

```
sudo apt-get update
sudo apt-get install -y net-tools git
sudo apt-get install -y python-pip
# install pyqt5 and NumPy
sudo apt-get install -y python3-pip
sudo apt-get install -y python3-pyqt5
pip3 install --upgrade pip
pip3 install numpy
```

### 2.2. ROSのインストール

- ROS(melodic)のインストール

```
# インストール手順参考:
# https://www.stereolabs.com/blog/ros-and-nvidia-jetson-nano/
# こちらの手順を自動化している、karaage0703さんのjetson-nano-toolsを使わせて頂きます。
# catkin_wsも自動で作成してくれます。
cd ~
git clone https://github.com/karaage0703/jetson-nano-tools
cd jetson-nano-tools
./install-ros-melodic.sh
echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc
source /opt/ros/melodic/setup.bash
```

- ROS関連パッケージのインストール

```
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
```

### 2.3. 機械学習ライブラリのインストール

```
# インストール手順参考:
# https://forums.developer.nvidia.com/t/pytorch-for-jetson-version-1-7-0-now-available/72048
# https://github.com/NVIDIA-AI-IOT/torch2trt
# https://github.com/mdegans/nano_build_opencv
# 上記のサイト等を参考にした上で、必要なコマンドを下記に記載しています。


### pytorch from pip image (v1.4)
wget https://nvidia.box.com/shared/static/yhlmaie35hu8jv2xzvtxsh0rrpcu97yj.whl -O torch-1.4.0-cp27-cp27mu-linux_aarch64.whl
sudo apt-get install -y python-pip libopenblas-base libopenmpi-dev
pip install torch-1.4.0-cp27-cp27mu-linux_aarch64.whl
wget https://nvidia.box.com/shared/static/c3d7vm4gcs9m728j6o5vjay2jdedqb55.whl -O torch-1.4.0-cp36-cp36m-linux_aarch64.whl
sudo apt-get install -y python3-pip libopenblas-base libopenmpi-dev
pip3 install torch-1.4.0-cp36-cp36m-linux_aarch64.whl

### torch vision (v0.2.2)
# https://forums.developer.nvidia.com/t/pytorch-for-jetson-version-1-7-0-now-available/72048
pip install future
pip3 install future
sudo apt-get install libjpeg-dev zlib1g-dev libpython3-dev libavcodec-dev libavformat-dev libswscale-dev
cd ~
git clone --branch v0.5.0 https://github.com/pytorch/vision torchvision
cd torchvision
export BUILD_VERSION=0.2.2
sudo python setup.py install
sudo python3 setup.py install
cd ../
pip install 'pillow<7'

### torch2trt
cd ~
git clone https://github.com/NVIDIA-AI-IOT/torch2trt
cd torch2trt
sudo python setup.py install
sudo python3 setup.py install

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
```

- ライブラリバージョン <br>

推奨環境 <br>

|  ライブラリ  |  バージョン(python3)  |　 バージョン(python)  |  備考  |
| ---- | ---- | ---- | ---- |
|  pytorch  |  ~~1.6.0~~ 1.4.0  |  1.4.0  |  -  |
|  torchvision  |  0.2.2  |  0.2.2  |  -  |
|  torch2trt  |  -  |  -  |  -  |
|  sklearn  |  0.23.2  |  Not_Installed  |  -  |
|  pandas  |  0.22.0 ~~(1.1.3必須かも)~~  |  Not_Installed  |  -  |
|  cv2  |  3.4.10  |  3.4.10   |  -  |

参考 <br>
[pytorchとtensoflowのバージョンをコマンドラインから調べる](https://qiita.com/seigot/items/0b81f601e5c9e30d0e46) <br>

### 2.4. ai_raceリポジトリの取得とビルド

（例）https://github.com/seigot/ai_race リポジトリの場合

```
cd ~/catkin_ws/src
git clone http://github.com/seigot/ai_race
cd ~/catkin_ws
catkin build
source devel/setup.bash
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
```

## 3. サンプルコード

### 3.1. サンプルコードの実行

別々のターミナルで実行して下さい。<br>
<br>
#### サンプルデータのダウンロード <br>

```
cd $HOME
git clone http://github.com/seigot/ai_race_data_sample
```

#### シミュレータ起動

```
roslaunch user_tutorial1 wheel_robot.launch
```

![simulator_sample.png](https://github.com/seigot/ai_race/blob/main/document/simulator_sample.png)

#### 学習モデルを利用した推論、車両操作

サンプルデータのダウンロードして使う場合の例。<br>
以下の通り実行する。

```
cd $HOME/catkin_ws/src/ai_race/ai_race/user_tutorial2/scripts
python inference_from_image.py --pretrained_model $HOME/ai_race_data_sample/model/sample.pth
```

![inference_simulator_sample.png](https://github.com/seigot/ai_race/blob/main/document/inference_sample.png)

比較的軽量なモデルを使う場合（通称：trtあり版）は以下の通り実行する。

```
# trtデータ準備(分割しているsample_trtデータを結合する)
cd $HOME/ai_race_data_sample/model
cat sample_trt_p* > sample_trt.pth
# 推論
cd $HOME/catkin_ws/src/ai_race/ai_race/user_tutorial2/scripts
python inference_from_image.py --trt_module --trt_model $HOME/ai_race_data_sample/model/sample_trt.pth
```

#### 学習

サンプルデータのダウンロードして使う場合の例。

```
cd $HOME/catkin_ws/src/ai_race/ai_race/learning
python3 train.py --data_csv $HOME/ai_race_data_sample/dataset/_2020-11-05-01-45-29_2/_2020-11-05-01-45-29.csv --model_name sample_model
```

#### 学習用データ取得

rqt, joystick, 各種コントローラーで車両操作し、rosbagを取得する

```
### rqt, joystick, 各種コントローラーを使って取得する
roslaunch user_tutorial1 rosbag.launch output_path:=$HOME
```

### 3.2. 各種コマンドの説明

#### 学習用データの取得、学習、学習モデルを利用した推論用コマンド <br>

* Step1.学習用データの取得

`roslaunch user_tutorial1 wheel_robot.launch`を実行した状態で、別ターミナルから以下を実行

```
## 学習用データ取得
## rosbag取得
roslaunch user_tutorial1 rosbag.launch output_path:=<出力ファイルのディレクトリ 絶対パス指定>
rqt # rqtを使う場合。robot steering -> 車両制御パラメータ（v,rad）指定

## rosbag --> image/command 変換
cd ~/catkin_ws/src/ai_race/ai_race/utility/scripts
mkdir -p /Images_from_rosbag
sudo chmod 777 /Images_from_rosbag
python rosbag_to_images_and_commands.py **.bag   # bagファイルから学習用データ（画像と車両制御パラメータ）を取得
python listup_all_rosbag_timestamp.py *.bag               # 時刻表示できる
```

* Step2.学習用データから、学習モデルを作成

```
## 学習 
cd learning (学習用フォルダへ移動) 
python3 train.py --data_csv <csvのパス フルパス指定> --model_name <保存するモデル名>  
#### 以下のディレクトリにモデルが保存されます
ls ~/catkin_ws/src/ai_race/ai_raceexperiments/models/checkpoints/*.pth
```

* Step3.学習モデルを使って推論、車両操作

`roslaunch user_tutorial1 wheel_robot.launch`を実行した状態で、別ターミナルから以下を実行

```
## 学習モデルを利用した推論、車両操作
## 推論(trtなし trt=比較的軽量なモデル) 
roscd user_tutorial2/scripts 
python inference_from_image.py --pretrained_model <学習させたモデル フルパス指定> 
```

* Step3+.学習モデルを軽量化して推論、車両操作

```
## 推論(trtあり）
#### 準備（準備は最初の一回でOK） 
roscd user_tutorial2/scripts 
python3 trt_conversion.py --pretrained_model <学習させたモデル フルパス指定> --trt_model <保存するtrtモデル名>   
#### 指定したディレクトリにモデルが保存されます
#### 実行 
python inference_from_image.py --trt_module --trt_model <保存したtrtモデル名 フルパス指定> 
```

#### ROS動作確認用コマンド <br>

主に環境構築の動作確認用です。

```
roslaunch tutorial1 wheel_robot.launch
roslaunch tutorial2 wheel_robot.launch
roslaunch tutorial3 wheel_robot.launch
roslaunch tutorial4 wheel_robot.launch
roslaunch tutorial5 wheel_robot.launch
roslaunch tutorial6 wheel_robot.launch
roslaunch tutorial7 wheel_robot.launch
```

## 4. ルール

学習モデルにより推論し、車両を操作して走行タイムを競います。<br>
<br>
2020/11/9-20、ルール作成中、ご意見募集中!!<br>
[こちら](document/rule.md)に記載予定 <br>

### 4.x. 走行タイム計測方法

記載予定 <br>
<br>
以下のタイマーを使う予定<br>

```
python3 judge/timer.py
```

### 4.x コース

いくつかコースを準備しようと試みています <br>

|  -  |  level1  |　 level2  |  level3  |
| ---- | ---- | ---- | ---- |
|  特徴  |  xxx  |  xxx  |  xxx  |
|  xxx  |  xxx  |  xxx  |  xxx  |
|  xxx  |  xxx  |  xxx  |  xxx  |
|  xxx  |  xxx  |  xxx  |  xxx  |
|  xxx  |  xxx  |  xxx  |  xxx  |

### 4.x 評価するもの

* 最終的に、学習モデルを評価する予定 <br>
* 本リポジトリをforkして頂き、各ユーザのリポジトリで学習モデルを作成して頂く予定 <br>　
* 評価タイムはどこかに載せたい（途中経過含む）<br>

## FAQ

[こちら](document/FAQ.md)に記載予定

## 参考
[Jetson NanoにROSをインストールする方法](https://qiita.com/karaage0703/items/aa54e086f0a2f165d3e9) <br>
[Jetson Nano関係のTIPSまとめ Swapファイルの設定](https://qiita.com/karaage0703/items/b14c249aa33112669ee4) <br>
[NVIDIA Jetson Nanoで OpenCV 3をビルドしてインストールする方法、NVCaffe等の OpenCV 4未対応を動かす](http://www.neko.ne.jp/~freewing/raspberry_pi/nvidia_jetson_nano_build_opencv_3410/) <br>
[https://github.com/mdegans/nano_build_opencv](https://github.com/mdegans/nano_build_opencv) <br>
[PyTorch for Jetson](https://forums.developer.nvidia.com/t/pytorch-for-jetson-version-1-7-0-now-available/72048) <br>
[https://github.com/NVIDIA-AI-IOT/torch2trt](https://github.com/NVIDIA-AI-IOT/torch2trt) <br>

## Finally

~~ HAVE FUN ! ~~
