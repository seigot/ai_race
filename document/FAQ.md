# FAQ

## 電源をACアダプターから供給するにはどうすればよい？

ACアダプターから電源供給するために、<br>
以下の通り、JetsonNano上の2ピンにジャンパを挿してください。その後、ACアダプターを挿してください。<br>
（ジャンパを挿さないとUSB電源共有設定となり、少しパワーが落ちます）<br>

> [Jetson Nanoで組み込みAIを試す（2）](https://monoist.atmarkit.co.jp/mn/articles/1907/01/news037.html)
> 図8
> 一方右の2ピンだが、これは電源ソースの選択で、開放状態だとUSBポートから、
> ジャンパピンを挿してショートするとACアダプターからの供給となる。
> ということでジャンパピンを挿しておく

## イメージファイルをSDカードに書き込みはどうすればよい？

以下が参考になります。ddコマンドでも書込み可能と思います。 <br>
[Etcherを使ってSDカードにラズパイのOSイメージを書き込む方法](https://raspi-japan.com/2018/10/16/sd-format-etcher/)
[etcher](https://www.balena.io/etcher/)

## Jetpack 4.3で環境構築は可能？

Jetpack 4.4 以降を推奨している理由は、公式にdockerコンテナや各種ライブラリが多くサポートされているためです。 <br>
Jetpack 4.3 自体も環境構築可能とは思いますが、cut&tryが必要です。Jetpack 4.3 自体は、以下Archiveから取得可能です。 <br>

```
Jetpack 4.3 Archive
https://developer.nvidia.com/jetpack-43-archive
 -> JetPack 4.3 - Installing JetPack:
 -> https://developer.nvidia.com/jetson-nano-sd-card-imager-3231
```

## Jetson nanoにVNC接続するにはどうすればよい？

以下のJetson開発者向けサイトの通り実施すればよさそうです。（MacOSでの実績あり）<br>
[Setting Up VNC](https://developer.nvidia.com/embedded/learn/tutorials/vnc-setup)<br>

## xxx
