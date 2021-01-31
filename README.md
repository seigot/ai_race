# ai_race
機械学習を学ぶことを目的とした、AIで車両を操作して走行性能を競うゲームです。 <br>
<br>
## 1. 準備

ご質問は、[FAQ](FAQ.md)に集約します。

### 1.0. jetson nano準備

記載予定 <br>
[こちら](https://qiita.com/seigot/items/115e25d0ae7149047760)にjetson nanoの備品を記載<br>
（シミュレータや機械学習は通常のPCでできなくもないが、環境統一のため、以降の環境構築や動作確認はjetson nanoを基準に行う） <br>

### 1.1. jetson nano起動

以下からイメージファイルを取得する。 <br>
 <br>
推奨バージョンはJetpack 4.4.1  <br>

```
# Jetpack 4.4.1 archive
https://developer.nvidia.com/jetpack-sdk-441-archive

# latest version
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

* 学習用データ、学習モデル【参考】

[こちら](https://github.com/seigot/ai_race_data_sample)にsampleデータを置いています。運営の動作確認用です。

* Docker環境【参考】

[こちら](docker/jetson/README.md)にDocker環境の利用手順を置いています。運営の動作確認用です。

## 2. インストール

結構時間が掛かります。<br>
とりあえず動かしたい方は[こちら](docker/jetson/README.md)のDocker環境をお試し頂いてもOKです。 <br>
「#」から始まる行はコメントです。 <br>

### 自動インストールスクリプト【推奨】

[こちら](https://github.com/seigot/ai_race/blob/main/scripts/setup/README.md)に、以下 2.0.～2.4. を自動実行するスクリプトを用意しています。 <br>
自動インストールスクリプトを使うか、以下の手順を手動で実行してインストールしてください。


### 2.0 SWAPファイル追加してメモリ増強【必須】 <br>

```
cd ~
git clone https://github.com/JetsonHacksNano/installSwapfile
cd installSwapfile
./installSwapfile.sh
# SWAP領域が増えていることを確認
free -mh
```

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
git checkout d1fa6f9f20c6c4c57a9486680ab38c45d0d94ec3   # 動作確認済みのバージョン（Wed Nov 4時点）に戻す
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
|  torch2trt  |  -  |  -  |  動作確認済みのバージョン `git checkout d1fa6f9f20c6c4c57a9486680ab38c45d0d94ec3`  |
|  sklearn  |  0.23.2  |  Not_Installed  |  -  |
|  pandas  |  0.22.0 ~~(1.1.3必須かも)~~  |  Not_Installed  |  -  |
|  cv2  |  3.4.10  |  3.4.10   |  -  |
|  pygame  |  1.9.6  |  1.9.6  |  -  |

参考 <br>
[pytorchとtensoflowのバージョンをコマンドラインから調べる](https://qiita.com/seigot/items/0b81f601e5c9e30d0e46) <br>

### 2.4. ai_raceリポジトリの取得とビルド

（例）https://github.com/seigot/ai_race リポジトリの場合

```
mkdir -p ~/Images_from_rosbag
cd ~/catkin_ws/src
git clone http://github.com/seigot/ai_race         # 自分のリポジトリを取得する場合は、ここのURLを変えて下さい。
cd ~/catkin_ws
catkin build
source devel/setup.bash
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
```

別リポジトリのビルドや、パッケージ追加時の再ビルド手順は、[FAQ #catkin_wsを再buildするにはどうすればよい？](https://github.com/seigot/ai_race/blob/main/FAQ.md)をご参考下さい。

## 3. サンプルコード

### 3.1. サンプルコードの実行
別々のターミナルで実行して下さい。<br>

#### サンプルデータのダウンロード <br>

```
cd $HOME
git clone http://github.com/seigot/ai_race_data_sample
```

#### シミュレータ起動

```
cd ~/catkin_ws/src/ai_race/scripts
bash prepare.sh
```

![simulator_sample_plane.png](https://github.com/seigot/ai_race/blob/main/document/simulator_sample_plane.png)

#### 学習モデルを利用した推論、車両操作

サンプルデータのダウンロードして使う場合の例。<br>
以下の通り実行する。

```
# 分割しているsampleデータを結合する
cd $HOME/ai_race_data_sample/model/plane
cat sample_plane_trt_p* > sample_plane_trt.pth
# 推論
cd ~/catkin_ws/src/ai_race/ai_race/learning/scripts
python inference_from_image.py --trt_module --trt_model $HOME/ai_race_data_sample/model/plane/sample_plane_trt.pth
```

![inference_sample_plane.png](https://github.com/seigot/ai_race/blob/main/document/inference_sample_plane.png)

#### 学習モデルを作成

サンプルデータを使って学習モデルを作成する場合の例。<br>
動作確認用に`--n_epoch 3`を指定して約30分程で終わるようにしています。<br>

```
cd ~/catkin_ws/src/ai_race/ai_race/learning/scripts
python3 train.py --data_csv $HOME/ai_race_data_sample/dataset/plane/_2020-11-17-01-34-45/_2020-11-17-01-34-45.csv --model_name sample_model --n_epoch 3
```

`train.py`の実行ログを参照し、学習モデル(`*.pth`)ファイルが作成できていることを確認下さい。<br>
`train.py`の引数に与えられるパラメータは以下で確認できます。`--n_epoch NN`等のパラメータは適宜調整して下さい。<br>

```
python3 train.py -h
```

#### 学習モデルの軽量化

JetsonNanoに合わせて学習モデルを軽量化する。(trtあり版と呼ばれるもの) <br>
作成した学習モデルのパスが、`$HOME/ai_race_data_sample/model/plane/sample_plane.pth` である場合の例。一度実行すると約10分程掛かります。<br>

```
python3 trt_conversion.py --pretrained_model $HOME/ai_race_data_sample/model/plane/sample_plane.pth --trt_model sample_model_trt.pth
```

`trt_conversion.py`の実行ログを参照し、`--trt_model`に指定したファイルが作成できていることを確認下さい。<br>
その後は前述同様、軽量化した学習モデルを利用して推論、車両操作を行って下さい。

#### 学習用データの取得 (Optional)

rqt, joystick, 各種コントローラーで車両操作し、学習用のデータ（画像、コマンド操作ログ）を取得する。<br>
サンプルデータでは期待する性能を出ない等、課題を感じた場合は、学習データを独自に取得することをお勧めします。<br>
以下を実行することで、keyboardから車両操作ができます。<br>

```
cd ~/catkin_ws/src/ai_race/ai_race/utility/scripts
python keyboard_con_pygame_videosave.py

### `ESC`キー押下で終了
### 終了後、学習データ（画像とコマンド）を格納したディレクトリがあることをコマンドから確認する
ls ${HOME}/Images_from_rosbag/
```

上記実行後、左下の「？」のうち`keyboard_con....py`が表示されてるものを押して、<br>
その状態で以下キーを押すと車両が動く。<br>

```
キー　車両の動き
l 進む
a 左にまがる
d 右にまがる
```

`keyboard_con_pygame_videosave.py`の停止は`ESC`キーを押下して下さい。<br>
その後、`${HOME}/Images_from_rosbag/`以下に学習データ（画像とコマンド）が格納されます。<br>
<br>
以上で作成したデータを、学習モデル作成に使用下さい。

### 3.2. 各種コマンドの説明

#### 学習用データの取得、学習モデルを作成、学習モデルを利用した推論用コマンド <br>

* Step1.学習用データの取得

`bash prepare.sh`を実行した状態で、別ターミナルから以下を実行

```
## 学習用データ取得
## rosbag取得
roslaunch sim_environment rosbag.launch output_path:=<出力ファイルのディレクトリ 絶対パス指定>
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
cd learning/scripts (学習用フォルダへ移動) 
python3 train.py --data_csv <csvのパス フルパス指定> --model_name <保存するモデル名>  
#### 実行ログ記載のディレクトリにモデルが保存されます
```

* Step3.学習モデルを使って推論、車両操作

`bash prepare.sh`を実行した状態で、別ターミナルから以下を実行

```
## 学習モデルを利用した推論、車両操作
## 推論(trtなし trt=比較的軽量なモデル) 
cd ~/catkin_ws/src/ai_race/ai_race/learning/scripts
python inference_from_image.py --pretrained_model <学習させたモデル フルパス指定> 
```

* Step3+.学習モデルを軽量化して推論、車両操作

```
## 推論(trtあり）
#### 準備（準備は最初の一回でOK） 
cd ~/catkin_ws/src/ai_race/ai_race/learning/scripts
python3 trt_conversion.py --pretrained_model <学習させたモデル フルパス指定> --trt_model <保存するtrtモデル名>   
#### 指定したディレクトリにモデルが保存されます
#### 実行 
python inference_from_image.py --trt_module --trt_model <保存したtrtモデル名 フルパス指定> 
```

### 3.3 ディレクトリ構成

|  ディレクトリ  |  内容  |　 備考  |
| ---- | ---- | ---- |
|  ./ai_race/learning  |  機械学習スクリプト  |  -  |
|  ./ai_race/utility  |  学習データ取得ツール　  |  -  |
|  ./ai_race/your_environment  |  各参加者の作成コードを格納するためのディレクトリ（ここにコードを置くと運営側のアップデートとconflictしない）  |  主に参加者向け  |
|  ./scripts  |  起動、終了スクリプト  |  -  |
|  ./ai_race/sim_world  |  シミュレータ用モデルデータ  |  主に運営向け  |
|  ./ai_race/sim_environment  |  シミュレータ用ROSノード等  |  主に運営向け  |
|  ./judge  |  審判サーバ  |  主に運営向け  |
|  ./document  |  公開資料  |  主に運営向け  |
|  ./docker  |  docker環境  |  主に運営向け  |
|  ./ai_race/example  |  シミュレータ用モデルデータのサンプル  |  ROS/シミュレータ等、学びたい人向けチュートリアル  |


```
(主要なファイルを抜粋)
├── README.md                           # 本Readme
├── ai_race
│   ├── learning
│   │   └── scripts                     # 機械学習スクリプト
│   │       ├── MyDataSet.py            # 学習モデル作成用スクリプト
│   │       ├── train.py                # 学習モデル作成用スクリプト
│   │       ├── inference_from_image.py # 推論による車両操作用スクリプト
│   │       └── trt_conversion.py       # 学習モデル軽量化用スクリプト（TRT版に変換する用）
│   ├── utility
│   │   └── scripts                              # 学習データ取得ツール
│   │       ├── joycon.py                        # 車両操作用
│   │       ├── keyboard_con_pygame2.py          # 車両操作用
│   │       ├── listup_all_rosbag_timestamp.py   # rosbag timestamp表示用
│   │       └── rosbag_to_images_and_commands.py # rosbag-->image,comand変換用
│   │  
│   ├── your_environment       # 各参加者の作成コードを格納するためのディレクトリ
│   │   │                      # （ここにコードを置くと運営側のアップデートとconflictしない）
│   │   ├── launch
│   │   │   └── sim_environment.launch  # 参加者独自で学習データ取得する場合の、シミュレータモデル追加用ひな形ファイル
│   │   └── scripts
│   │       └── your_train.py           # 参加者独自でtrain.pyを作成する場合のひな形ファイル
│   │   
│   ├── example                   # シミュレータ用モデルデータのサンプル	
│   │   └── tutorial1-7 
│   ├── sim_environment           # シミュレータ用ROSノード等	
│   └── sim_world                 # シミュレータ用モデルデータ
│   
├── FAQ.md            # FAQ
├── docker            # docker環境
├── document          # 公開資料
├── judge             # 審判サーバ
└── scripts           # 起動用スクリプト
    ├── prepare.sh    # シミュレータ環境起動用(level1-3対応)
    ├── start.sh      # [大会用] 開始スクリプト
    └── stop.sh       # [大会用] 停止スクリプト
```

### 3.4 学習モデル自作のはじめかた

#### 本リポジトリのfork

まず、Githubアカウントを取得して本リポジトリを自リポジトリにforkして下さい。

> リポジトリのフォークの例 <br>
> 
> 0. GitHubアカウントを作成/ログインする。 <br>
> 1. GitHub で、[https://github.com/seigot/ai_race](https://github.com/seigot/ai_race)リポジトリに移動します <br>
> 2. ページの右上にある [Fork] をクリックします。 <br>
> 参考：[リポジトリをフォークする](https://docs.github.com/ja/free-pro-team@latest/github/getting-started-with-github/fork-a-repo) <br>

#### 学習用データの取得、チューニング、学習モデル作成

forkしたリポジトリで各々の学習データ取得、チューニング、学習モデル作成をしてください。<br>
変更ファイルは、運営とのconflictを避けるために`your_environmentディレクトリ`以下に登録することをお勧めします。<br>

- 学習データの取得を工夫する

サンプルの`学習用データの取得`を参考に、車両を自ら操作して学習データを取得することが可能です。<br>
`走行経路`や`入力画像のバリエーション`など、各々工夫をしてみてください。<br>
<br>
※ 学習データ自体はサイズが大きいため、ファイルの受渡しはgithub以外でやりとりすることをお勧めします。<br>
　（Githubは1ファイル最大が50MBまで、1GB 以下を推奨という制約があり、大きなファイルを扱うのに適しているとはいえない）<br>

- チューニング、学習モデルの作成を工夫する

train.pyや周辺ファイルを参考に、各種パラメータを調整することが可能です。<br>
機械学習アルゴリズム選定など含め、各々工夫をしてみてください。<br>

#### 自リポジトリの学習モデルを公式リリースする

学習モデルを公式リリースする場合は、Githubリリースの機能を使うと簡単なのでお勧めです。

> 学習モデルを提出（バイナリリリース）する場合の手順参考 <br>
> [リポジトリのリリースを管理する](https://docs.github.com/ja/free-pro-team@latest/github/administering-a-repository/managing-releases-in-a-repository) <br>
> 7.オプションで、コンパイルされたプログラムなどのバイナリファイルをリリースに含めるには、ドラッグアンドドロップするかバイナリボックスで手動で選択します。 <br>

#### 本リポジトリの最新バージョン取り込み

今後、本リポジトリもバージョンアップしていく予定です。<br>
本リポジトリのバージョンアップを取り込む場合は、forkしたリポジトリにて以下を実行して下さい。<br>

```
git checkout main                                          # ローカルのmainブランチに移動
git remote add upstream https://github.com/seigot/ai_race  # fork元のリポジトリをupstream という名前でリモートリポジトリに登録（名前はなんでもいい。登録済みならスキップ）
git fetch upstream                                         # upstream から最新のコードをfetch
git merge upstream/main                                    # upstream/main を ローカルのmaster にmerge
git push                                                   # 変更を反映
```

参考：[github で fork したリポジトリで本家に追従する](https://please-sleep.cou929.nu/track-original-at-forked-repo.html)

#### Pull Requestを送る（Optional）

本リポジトリへ修正リクエストを送ることが可能です。詳しくは参考をご参照下さい。<br>
<br>
※追記　Pull Request練習用リポジトリを作成しました。<br>
[test_pull_request](https://github.com/seigot/test_pull_request)<br>
<br>
参考：<br>
[GitHub-プルリクエストの作成方法](https://docs.github.com/ja/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request)<br>
[[実践] はじめてのPull Requestをやってみよう](https://qiita.com/wataryooou/items/8dce6b6d5f54ab2cef04)<br>
[【GitHub】Pull Requestの手順](https://qiita.com/aipacommander/items/d61d21988a36a4d0e58b)<br>


### 3.5 SimpleNetを使う

デフォルトでは、ニューラルネットワークとしてResNet-18を使うようになっていますが、自分でニューラルネットワークを作成する場合のサンプルとして、[シンプルなニューラルネットワーク(SimpleNet)](https://github.com/seigot/ai_race/blob/main/ai_race/learning/scripts/samplenet.py#L35)を用意しています。<br>
ResNet-18ではなくSimpleNetを使う場合は、`train.py`, `trt_conversion.py`, `inference_from_image.py`の実行時に、`--model simplenet`オプションを付けてください。
```
cd ~/catkin_ws/src/ai_race/ai_race/learning/scripts
python3 train.py --model simplenet　 --data_csv $HOME/ai_race_data_sample/dataset/plane/_2020-11-17-01-34-45/_2020-11-17-01-34-45.csv --model_name sample_model
python3 trt_conversion.py --model simplenet --pretrained_model <学習させたモデル フルパス指定> --trt_model <保存するtrtモデル名>
python inference_from_image.py --model simplenet --trt_module --trt_model <保存したtrtモデル名 フルパス指定> 
```

## 4. ルール

### 4.1. 概要

学習モデルにより推論し、車両を操作して走行性能を競います。<br>
今回は以下のルールを採用予定です。<br>
* 制限時間4分以内に、コースを何週回れるかを競う。<br>
* 後述するコースのうち、最もシンプルなlevel1を使う。<br>
* コースアウトは、自力復帰困難な場合はスタート地点に復帰して走行を継続する。<br>

[こちら](https://github.com/seigot/ai_race/blob/main/document/rule.md) に詳細を記載予定 <br>

### 4.2. 経過時間と周回回数の計測方法

前述の`prepare.sh`実行時に起動するタイマーと、周回カウンターを使い自動計測します。<br>

### 4.3 コース

以下のコースを用意しました。<br>

|  -  |  level1  |  level1 with透明壁  |  level1 advance  |
| ---- | ---- | ---- | ---- |
|  名称  |  Plane  |  Plane(with透明壁)  |  Plane(advance)  |
|  外観  |  ![medium_track_plane-2.png](https://github.com/seigot/ai_race/blob/main/document/medium_track_plane-2.png)  |  ![medium_track_plane_tomei-kabe.png](https://github.com/seigot/ai_race/blob/main/document/medium_track_plane_tomei-kabe.png)  |  ![medium_track_plane3_advance.png](https://github.com/seigot/ai_race/blob/main/document/medium_track_plane3_advance.png)  |
|  特徴  |  地面：一様な模様です  |  地面：一様な模様です  |  地面：一様な模様+周辺に草が生えています。<br>草エリア走行時は速度が落ちます。  |
|  障害物  |  なし  |  赤い点線部分に透明の壁があります  |  赤い点線部分に透明の壁があります  |
|  起動コマンド  |  bash prepare.sh -l 1  |  bash prepare.sh -l 1t  |  bash prepare.sh -l 1a  |
|  学習データのサンプル  |  あり（１週分）[url](https://github.com/seigot/ai_race_data_sample/tree/main/dataset/plane)  |  なし  |  なし  |
|  備考  |  今回のルールで採用  |  初回起動前に、[FAQ](FAQ.md)を参考に再度catkin buildして下さい  |  初回起動前に、[FAQ](FAQ.md)を参考に再度catkin buildして下さい  |

|  -  |  level2  |  level3  |
| ---- | ---- | ---- |
|  名称  |  Medium Track  |  Hard track  |
|  外観  |  ![medium_track-2.png](https://github.com/seigot/ai_race/blob/main/document/medium_track-2.png)  |  ![hard_track.png](https://github.com/seigot/ai_race/blob/main/document/hard_track.png)  |
|  特徴  |  地面：濃淡付きの模様です  |  地面：サーキット型の模様です。カーブが急で、速度を調整しないと曲がれない  |
|  障害物  |  なし  |  三角コーンを置くかも  |
|  起動コマンド  |  bash prepare.sh -l 2  |  bash prepare.sh -l 3  |
|  学習データのサンプル  |  あり（１週分）[url](https://github.com/seigot/ai_race_data_sample/tree/main/dataset/medium) |  なし  |
|  備考  |  optional  |  optional（準備中）  |

### 4.4 提出して頂くもの

* level1コースで動作する学習モデルを提出して下さい。（学習モデルは、前述のJetsonNano向けに軽量化したtrtあり版をお願いします） <br>
* 提出方法は、Githubリリースの機能を使うと簡単なのでお勧めです。この場合はGithubリポジトリ名/リリースURLを教えて下さい。<br>

> 学習モデルを提出（バイナリリリース）する場合の手順参考 <br>
> [リポジトリのリリースを管理する](https://docs.github.com/ja/free-pro-team@latest/github/administering-a-repository/managing-releases-in-a-repository) <br>
> 7.オプションで、コンパイルされたプログラムなどのバイナリファイルをリリースに含めるには、ドラッグアンドドロップするかバイナリボックスで手動で選択します。 <br>

* 途中経過含めて、上位の結果はどこかに載せたいと考えています。<br>

## FAQ

[こちら](FAQ.md)に記載

## 参考
[Jetson NanoにROSをインストールする方法](https://qiita.com/karaage0703/items/aa54e086f0a2f165d3e9) <br>
[Jetson Nano関係のTIPSまとめ Swapファイルの設定](https://qiita.com/karaage0703/items/b14c249aa33112669ee4) <br>
[NVIDIA Jetson Nanoで OpenCV 3をビルドしてインストールする方法、NVCaffe等の OpenCV 4未対応を動かす](http://www.neko.ne.jp/~freewing/raspberry_pi/nvidia_jetson_nano_build_opencv_3410/) <br>
[https://github.com/mdegans/nano_build_opencv](https://github.com/mdegans/nano_build_opencv) <br>
[PyTorch for Jetson](https://forums.developer.nvidia.com/t/pytorch-for-jetson-version-1-7-0-now-available/72048) <br>
[https://github.com/NVIDIA-AI-IOT/torch2trt](https://github.com/NVIDIA-AI-IOT/torch2trt) <br>
RESPECT  [OneNightRobocon](https://github.com/OneNightROBOCON) <br>
[リポジトリをフォークする](https://docs.github.com/ja/free-pro-team@latest/github/getting-started-with-github/fork-a-repo) <br>
[github で fork したリポジトリで本家に追従する](https://please-sleep.cou929.nu/track-original-at-forked-repo.html) <br>
[リポジトリのリリースを管理する](https://docs.github.com/ja/free-pro-team@latest/github/administering-a-repository/managing-releases-in-a-repository) <br>

## Finally

~~ HAVE FUN ! ~~
