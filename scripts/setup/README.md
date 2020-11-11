# setup

* インストール手順を自動化するスクリプト
* 失敗した時点で停止します。状況により手動インストールを併用下さい。
* （場合により全自動にならないことがあります。Pull Requestのボランティア募集中です。） <br>

## 使い方

sudo apt-get update 時にパスワードを聞かれないようにする

```
$ sudo visudo    # user:jetsonの場合
# User privilege specification
jetson ALL=NOPASSWD: ALL
```

スクリプト実行

```
cd ~
mkdir -p tmp; cd tmp;
git clone https://github.com/seigot/ai_race
cd ai_race/scripts/setup
time ./auto_setup.sh
```

## Tips
* opencvインストール時はgdmを選択
