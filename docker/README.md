# ai_race docker環境

検討中<br>
TODO<br>
* jetpack4.3標準のDockerイメージがあるか調べる
* AIのライブラリ（tensorflow/pytorchなど）のインストール手順を調べる

## dockerコンテナ起動手順（仮）

以下を実行（仮）

```
sudo xhost +si:localuser:root
sudo docker run --runtime nvidia --network host -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix seigott/ai_race_docker
```

以下を参考 <br>
[nvidia-docker/wiki](https://github.com/NVIDIA/nvidia-docker/wiki/NVIDIA-Container-Runtime-on-Jetson) <br>

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
