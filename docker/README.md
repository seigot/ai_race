# ai_race 全部入りdocker環境

## 全部入りdocker環境に事前インストールしているもの

~~* jetpack4.3標準のDockerイメージがあるか調べる~~ なかった
* 今回使用するROS(melodic)環境一式
* 今回使用する機械学習ライブラリ（pytorchなど）一式
* 本リポジトリ
* 基本的なエディタ（vi,emacs）

詳しくは[Dockerfile](Dockerfile)をご参照

## dockerコンテナ使用手順

jetson nano（Jetpack4.4以上）の環境で、ターミナルから以下を実行して下さい。

- コンテナ起動

```
sudo xhost +si:localuser:root
sudo docker run --runtime nvidia --network host -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix --name ai_race_docker seigott/ai_race_docker
```

- コンテナに入るコマンド（コンテナ起動とは別のターミナルで実行）

```
sudo docker exec -it ai_race_docker /bin/bash
```

- コンテナ内での動作確認用

シミュレータ起動

```
roslaunch user_tutorial1 wheel_robot.launch
```

学習モデルを利用した推論、車両操作

```
cd ~/ai_race/catkin_ws/src/user_tutorial2/scripts
python inference_from_image.py --pretrained_model /home/jetson/ai_race_data_sample/model/sample.pth
```

学習

```
cd ~/ai_race/catkin_ws/src/learning
python3 train.py --data_csv /home/jetson/ai_race_data_sample/dataset/_2020-11-05-01-45-29_2/_2020-11-05-01-45-29.csv --model_name sample_model
```

データ取得

```
確認中
```

- コンテナ破棄

（注意）誤ってコンテナ破棄した場合、コンテナ内のデータが消えてしまいます。

```
sudo docker rm -f ai_race_docker
```

- 参考 <br>

以下<br>
[nvidia-docker/wiki](https://github.com/NVIDIA/nvidia-docker/wiki/NVIDIA-Container-Runtime-on-Jetson) <br>

## dockerコンテナ使用注意事項

* コンテナ内の本リポジトリが最新版になっていない事があります。git pullして下さい。
* ネイティブ環境と比べて動作が遅いかもしれません。
* もしパッケージ追加したい場合、コンテナ起動毎にインストールが必要です。

## Dockerコマンドをsudoなしで実行する

```
# dockerグループがなければ作る
sudo groupadd docker

# 現行ユーザをdockerグループに所属させる
sudo gpasswd -a $USER docker

# dockerデーモンを再起動する (CentOS7の場合)
sudo systemctl restart docker

# exitして再ログインすると反映される。
exit
```

参考 <br>
[Dockerコマンドをsudoなしで実行する方法](https://qiita.com/DQNEO/items/da5df074c48b012152ee) <br>

## ビルド手順

以下を実行

```
docker build -t seigott/ai_race_docker .
```

pushする場合は以下

```
docker login
docker push seigott/ai_race_docker .
docker logout
```

## 参考（にする予定）
JetPack4.3 <br>
[https://developer.nvidia.com/jetpack-43-archive](https://developer.nvidia.com/jetpack-43-archive) <br>
JetPack 4.4 includes L4T 32.4.3 with these highlights: <br>
[https://developer.nvidia.com/jetpack-sdk-44-archive](https://developer.nvidia.com/jetpack-sdk-44-archive) <br>

nvidia-docker/wiki <br>
[nvidia-docker/wiki](https://github.com/NVIDIA/nvidia-docker/wiki/NVIDIA-Container-Runtime-on-Jetson) <br>
nvidia:l4t-base <br>
[nvidia:l4t-base](https://ngc.nvidia.com/catalog/containers/nvidia:l4t-base) <br>
nvidia:deepstream <br>
[nvidia:deepstream](https://ngc.nvidia.com/catalog/containers/nvidia:deepstream) <br>
[https://github.com/atinfinity/sdk_manager_docker](https://github.com/atinfinity/sdk_manager_docker) <br>
 <br>
[https://docs.nvidia.com/deeplearning/frameworks/install-tf-jetson-platform/index.html](https://docs.nvidia.com/deeplearning/frameworks/install-tf-jetson-platform/index.html) <br>
 <br>
Nvidia jetson-nano camera <br>
[JetsonでCSIカメラ(nvcamerasrc)をdockerコンテナ内から使う](https://o-84.com/article/jetson-csi-camera-nvcamerasrc-on-docker-container/) <br>
 <br>
Jetson forums <br>
[forums.developer.nvidia.com](https://forums.developer.nvidia.com/c/agx-autonomous-machines/jetson-embedded-systems/jetson-nano/76/l/latest) <br>
<br>
Jetson_Zoo<br>
[https://elinux.org/Jetson_Zoo](https://elinux.org/Jetson_Zoo)<br>
Machine Learning Container for Jetson and JetPack<br>
[https://ngc.nvidia.com/catalog/containers/nvidia:l4t-ml](https://ngc.nvidia.com/catalog/containers/nvidia:l4t-ml) <br>
> note: the l4t-ml containers require JetPack 4.4 or newer
<br>
以下を参考にすればDockerコンテナ内からホスト側のディスプレイに表示できる<br>
nvidia-docker/wiki <br>
[nvidia-docker/wiki](https://github.com/NVIDIA/nvidia-docker/wiki/NVIDIA-Container-Runtime-on-Jetson) <br>
Hello World!!<br>
<br>
すっぴんのdocker<br>
tensorflow<br>
[https://hub.docker.com/r/tensorflow/tensorflow](https://hub.docker.com/r/tensorflow/tensorflow) <br>
pytorch<br>
[https://hub.docker.com/r/pytorch/pytorch](https://hub.docker.com/r/pytorch/pytorch) <br>
