# setup

* インストール手順を自動化するスクリプト
* 失敗した時点で停止します。状況により手動インストールを併用下さい。
* （Jetpack 4.4.1 で確認済、場合により全自動にならないことがあります。Pull Requestのボランティア募集中です。） <br>

## 使い方

### sudo apt-get update 時にパスワードを聞かれないようにする（[参考](https://www.hiroom2.com/2018/10/23/ubuntu-1810-sudo-ja/)）

```
$ sudo visudo    # 以下の行に追加する
# Allow members of group sudo to execute any command
%sudo  ALL=(ALL:ALL) NOPASSWD:ALL
```

備考： "esc+:wq" でエディタを終了

### 対話処理は先に実行しておく

[How To Install "gdm3" Package on Ubuntu](https://zoomadmin.com/HowToInstall/UbuntuPackage/gdm3)

```
sudo apt-get update -y
sudo apt-get install -y gdm3  ## 対話ウィンドウが出たら --> OK --> gdm3 を選択
```

備考：自動化したい

### スクリプト実行

```
cd ~
mkdir -p tmp; cd tmp;
git clone https://github.com/seigot/ai_race
cd ai_race/scripts/setup
time ./auto_setup.sh
```

## Tips
* 6時間以上掛かる

```
$ time ./auto_setup.sh
real 405m14.993s
user 350m6.152s
sys 19m4.228s
```

* 2020/11/15以降の追加処理（主に、それ以前に`auto_setup.sh`実行した人むけ）

```
# for judge server
pip3 install flask

# pygame
sudo apt-get update -y
sudo apt-get install -y libsdl-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev
sudo apt-get install -y libsmpeg-dev libportmidi-dev libavformat-dev libswscale-dev
sudo apt-get install -y libfreetype6-dev
sudo apt-get install -y libportmidi-dev
sudo pip3 install pgzero

# requests
pip3 install requests
python -m pip install requests

# pygame python
python -m pip install pygame==1.9.6

# mkdir
mkdir -p ~/Images_from_rosbag

# scikit learn
sudo apt install -y gfortran
```
