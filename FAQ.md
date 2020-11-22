# FAQ

## 必要な機材は何があるか？
基本的に、JetsonNano+周辺機材があれば完結できるように準備しています。<br>

## ネットワーク環境はどれくらい必要か？
各種ダウンロード／インストールのために、JetsonNanoへネットワーク接続が必要です。<br>
特に秘情報は扱わないので、一般回線への接続をお勧めします。<br>
一般回線以外の場合、秘情報をJetsonNanoに格納しないようにしてください。<br>

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

## イメージファイルをSDカードに書き込みはどうすればよい？

以下が参考になります。ddコマンドでも書込み可能と思います。 <br>
[Etcherを使ってSDカードにラズパイのOSイメージを書き込む方法](https://raspi-japan.com/2018/10/16/sd-format-etcher/) <br>
[etcher](https://www.balena.io/etcher/)

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

## xxx
