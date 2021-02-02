# FAQ

## 必要な機材は何があるか？
基本的に、JetsonNano+周辺機材があれば完結できるように準備しています。<br>

## ファン取り付け／ファンコネクタ／電源ジャンパー接続

接続について、以下の通りアドバイスを頂きました。<br>

![pin.png](https://github.com/seigot/ai_race/blob/main/document/pin.png)

```
1.ファン取り付け 
  かなり細かい作業になり、ピンセットと細いプラスドライバー(No.2 or 1)が必須です。(100均に売っているようです) 
  向きについては吹き付ける方向(ラベルをヒートシンク側)にするのが一般的と思われます。
2.ファンコネクタ 
  4ピンがあり、基板外側から黒・赤となるように挿入します。 
3.電源ジャンパー 
  デフォルトはMicro USBからの電源供給になっています。 
  ACアダプタからの供給は図の部分にジャンパーを接続します。
```

## イメージファイルをSDカードに書き込みはどうすればよい？

以下が参考になります。ddコマンドでも書込み可能と思います。 <br>
[Etcherを使ってSDカードにラズパイのOSイメージを書き込む方法](https://raspi-japan.com/2018/10/16/sd-format-etcher/) <br>
[etcher](https://www.balena.io/etcher/)

## ネットワーク接続は必要か？
各種データやライブラリのダウンロード／インストールのために、JetsonNanoへネットワーク接続が必要です。<br>
有線で一般回線への接続をお勧めします。<br>
もし特別な事情があり一般回線以外に繋ぐ場合、秘情報をJetsonNanoに格納しないようにしてください。<br>

## インストール手順が長いようにみえる
インストール自動化スクリプトを作成しています。以下を参照下さい。<br>
[setup](https://github.com/seigot/ai_race/blob/main/scripts/setup/README.md)<br>

## インストール自動化スクリプト実行中に、scikit learnインストールエラー（error: library mach has Fortran sources but no Fortran compiler found）

以下と同件の可能性があります。<br>
[jetson nanoでscikit learnインストール時にエラー（error: library mach has Fortran sources but no Fortran compiler found）](https://qiita.com/seigot/items/7564b3901c48e10840f3)<br>
この場合は、以下で解決するようです。<br>

```
sudo apt install -y gfortran
```

## シミュレータ起動しても、モデルが表示されずに終了する

`GAZEBO_MODEL_PATH`が実際のパスに合っていない可能性があります。<br>
パスは`cat ~/.bashrc`で確認可能です。<br>

```
cat ~/.bashrc
GAZEBO_MODEL_PATH=xxx  # ここのパス
```

`~/.bashrc`のパスを変えるか、シンボリックリンクを作成することで解決すると思います。<br>
（例）`/home/${USER_NAME}`へのシンボリックリンクを、`/home/jetson`に作成する場合。<br>

```
cd /home
USER_NAME=`whoami`
sudo ln -s ${USER_NAME} jetson
```

## `python -c "from torch2trt import TRTModule"`実行時にエラー終了する。

以下エラーログの場合、[こちら](https://qiita.com/seigot/items/5927c58688c4d40a5a86)と類似の可能性があります。

```
$ python -c "from torch2trt import TRTModule"
WARNING: TensorRT Python 2 support is deprecated, and will be dropped in a future version!
Traceback (most recent call last):
  File "<string>", line 1, in <module>
...
  File "/usr/lib/python2.7/copy.py", line 182, in deepcopy
    rv = reductor(2)
TypeError: can't pickle method_descriptor objects
```

[https://github.com/NVIDIA-AI-IOT/torch2trt](https://github.com/NVIDIA-AI-IOT/torch2trt)リポジトリアップデートの影響を受けている可能性があります。<br>
以下で、動作確認済みのバージョン（Wed Nov 4時点）に戻すと解消する可能性があります。<br>

```
cd ~/torch2trt                                          # torch2trtを、git cloneしたリポジトリへ移動
git checkout d1fa6f9f20c6c4c57a9486680ab38c45d0d94ec3   # 動作確認済みのバージョン（Wed Nov 4時点）に戻す
sudo python setup.py install                            # 再インストール
sudo python3 setup.py install                           # 再インストール
```

動作確認済みのバージョン（Wed Nov 4時点）に戻せているかは、以下コマンドで確認可能です。

```
$ cd ~/torch2trt      # torch2trtを、git cloneしたリポジトリへ移動
$ git log -1          # 動作確認済みのバージョン（Wed Nov 4時点）に戻せているか確認、以下ログが出ればOK
commit d1fa6f9f20c6c4c57a9486680ab38c45d0d94ec3 (HEAD -> master, origin/master, origin/HEAD)
Author: John <jwelsh@nvidia.com>
Date:   Wed Nov 4 13:45:36 2020 -0500
    Sandeepkumar skb groupnorm plugin (#437)
    * added plugin for GroupNorm
    Co-authored-by: sandeepkumar-skb <sandeep.skb@uber.com>
```

## catkin_wsを再buildするにはどうすればよい？

以下の通り実行して下さい。

(例) `~/catkin_ws`以下を、再度catkin buildする場合

```
cd ~/catkin_ws
catkin clean -y
catkin build
source devel/setup.bash
```

(例) 既存のリポジトリを削除、別リポジトリを取得して再度catkin buildする場合

```
cd ~/catkin_ws/src
sudo rm -r ai_race                                 # [注意]ai_raceリポジトリを削除します、ローカルの変更を失わないよう注意して下さい。
git clone http://github.com/seigot/ai_race         # 自分のリポジトリを取得する場合は、ここのURLを変えて下さい。
cd ~/catkin_ws
catkin clean -y
catkin build
source devel/setup.bash
```

## level1t(with透明壁),level1a(advance)の初回起動前にcatkin_wsを再buildするにはどうすればよい？

以下を実施して下さい。level1t,1a用に追加した機能を有効化するために必要です。<br>
（コースアウト検知機能のためにcatkin再build、自動復帰機能のためにros-melodic-cob-srvs、が必要）<br>
<br>
`~/catkin_ws`以下を、再度catkin buildする場合

```
cd ~/catkin_ws
catkin clean -y
catkin build
source devel/setup.bash
```

加えて、以下パッケージのインストールも必要です。

```
sudo apt install -y ros-melodic-cob-srvs
```

## 1～2時間着手するならどのあたりが良いか。
機械学習の学習モデル生成パラメータ／ネットワーク検討周りがよいと思います。<br>
学習モデル生成はepoch回数により時間が掛かるので、コマンド実行後はJetsonに後は任せるなど工夫下さい。<br>
次点で、走行性能評価、学習データ取得だと思われますがこれらはもう少し時間が掛かると思います。<br>

## 実機走行について
Jetracerを2台ほど用意しようと検討中<br>

## 電源をACアダプターから供給するにはどうすればよい？

以下を参考に、JetsonNano上の2ピンにジャンパを挿してください。その後、ACアダプターを挿してください。<br>
（ジャンパを挿さないとUSB電源共有設定となり、少しパワーが落ちます）<br>

> [Jetson Nanoで組み込みAIを試す（2）](https://monoist.atmarkit.co.jp/mn/articles/1907/01/news037.html) <br>
> 図8 <br>
> 一方右の2ピンだが、これは電源ソースの選択で、開放状態だとUSBポートから、 <br>
> ジャンパピンを挿してショートするとACアダプターからの供給となる。 ということでジャンパピンを挿しておく <br>

## Jetpack 4.3で環境構築は可能？

Jetpack 4.3 自体も環境構築可能とは思いますが、cut&tryが必要です。Jetpack 4.3 自体は、以下Archiveから取得可能です。 <br>
Jetpack 4.4 以降を推奨している理由は、公式にdockerコンテナや各種ライブラリが多くサポートされているためです。 <br>
何か特別な理由がない限りは、Jetpack 4.4以降をお勧めします。 <br>

```
Jetpack 4.3 Archive
https://developer.nvidia.com/jetpack-43-archive
 -> JetPack 4.3 - Installing JetPack:
 -> https://developer.nvidia.com/jetson-nano-sd-card-imager-3231
```

Jetpack 4.4.1 archiveは以下の通りです。

```
Jetpack 4.4.1 archive
https://developer.nvidia.com/jetpack-sdk-441-archive
```

## Jetson nanoにVNC接続するにはどうすればよい？

以下のJetson開発者向けサイトの通り実施すればよさそうです。（MacOSでの実績あり）<br>
[Setting Up VNC](https://developer.nvidia.com/embedded/learn/tutorials/vnc-setup)<br>
以下、tigerVNCや、デスクトップ共有を使った手順でも実績があるようです。よりよい手順があれば教えて頂けると助かります。<br>
[Jetson Nanoにリモートデスクトップ(VNC)環境を用意する](https://qiita.com/iwatake2222/items/a3bd8d0527dec431ef0f) <br>
[5Getting Started with the NVIDIA Jetson Nano Developer Kit](https://www.hackster.io/news/getting-started-with-the-nvidia-jetson-nano-developer-kit-43aa7c298797) <br>

## 機械学習をPC上のUbuntu等で行うにはどうすればよい？（JetsonNanoではなく）
PC上のUbuntu等に機械学習の処理を任せることは可能と思いますが、環境構築が難しいかもしれません。 <br>
環境構築手順の確立のアドバイス/ボランティア募集しています。 <br>
pytorch等のライブラリバージョンを一致させることがポイントかと思います。<br>

## Proxy環境下で環境構築するために何か必要な手順はありますか
各種パッケージ取得、ダウンロード時にProxyサーバ経由する必要があると思います。（例. apt-get,git,curl,必要に応じてdocker...etc）<br>
特別な理由がなければ、Proxy環境以外での環境構築、及び利用をお勧めします。<br>
Proxy利用自体が各ネットワーク事情に依存すると思いますので、Proxy環境で使用する場合のサポートは困難です。<br>

## forkしたリポジトリに最新バージョン取り込みたい

本リポジトリのバージョンアップを取り込む場合は、forkしたリポジトリにて以下を実行して下さい。

```
git checkout main                                          # ローカルのmainブランチに移動
git remote add upstream https://github.com/seigot/ai_race  # fork元のリポジトリをupstream という名前でリモートリポジトリに登録（名前はなんでもいい。登録済みならスキップ）
git fetch upstream                                         # upstream から最新のコードをfetch
git merge upstream/main                                    # upstream/main を ローカルのmaster にmerge
git push                                                   # 変更を反映
```

参考：[github で fork したリポジトリで本家に追従する](https://please-sleep.cou929.nu/track-original-at-forked-repo.html)

## `train.py/trt_conversion.py/inference_from_image.py`の実行ログの期待値がほしい

[実行ログ](https://github.com/seigot/ai_race/blob/main/document/exec_log.md)に記載しました。<br>
ただし、最新コードでは出力ログが変わることがあります。<br>

## レース当日に運営側で実行したコマンドはどのようなものか

以下の通りです。ご参考。

- 学習モデルの実行手順<br>
[https://github.com/seigot/ai_race_score/tree/main/check](https://github.com/seigot/ai_race_score/tree/main/check)<br>

- 走行ログのrecord/replay

```
cd ~/catkin_ws/src/ai_race/scripts
./prepare_pos.sh -l 1t -g false -r true            # -r true  : 走行ログをrecordする。ログは"Position_Logs/_2021-01-22-22-48-38/pos.csv"等に保存される。
./prepare_pos.sh -l 1t -g false -z pos.csv         # -z *.csv : 指定した走行ログをreplayする。軌跡は旗で表示される。
./prepare_pos.sh -l 1t -g false -r true -z pos.csv # 走行ログをrecordしつつ、指定した走行ログをreplayする。

推論は「学習モデルの実行手順」の通り実施
```

- 動画編集は以下（3倍速、領域を切り出す、先頭n秒削除、カットと結合）<br>
[コマンドラインからmp4を倍速に変換する](https://qiita.com/seigot/items/4d89c42a992569fa1890)<br>

## xxx
