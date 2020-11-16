# judgeサーバ（仮）

10/29 作成中<br>
10/30 簡易版を作成<br>
11/15 serve化お試し<br>

## 動作確認コマンド
準備

```
pip3 install flask
```

judge server起動

```
python3 judgeServer.py
```

別ターミナルで、timerウィンドウ起動

```
python3 timer.py
```

init/start/stop/LapCountボタンを押す

### できてないこと

- startトリガーの自動化（車両が動いたらstartとか、今は手動です）
- LapCount更新自動化（今は手動です）
- Stop状態の定義（タイマーストップ要る？）
- JudgeServer IPアドレス指定（実機、sim/学習環境分離時に必要かもしれない）
- JudgeServer情報の配信
- コース情報、車両情報の指定（もし必要ならば）

# 参考

[https://www.geeksforgeeks.org/pyqt5-digital-stopwatch/](https://www.geeksforgeeks.org/pyqt5-digital-stopwatch/)<br>
[pyqt5で、レースの経過時間と周回を測ってくれるようなウィンドウを作成する](https://qiita.com/seigot/items/258e96381269e2aa2cd1)<br>
