# 実行ログ

以下は参考情報です。最新コードでは出力ログが変わることがあります。

## 2020/12/13時点　最新コードの実行ログ

#### train.py

入力：学習データ　`--data_csv`引数に与えたファイル<br>
出力：学習モデル　`--model_name`引数に与えたファイル<br>
期待値：`/home/jetson/work/experiments/models/checkpoints/*.pth`に、学習モデルファイルが出力されること<br>

```
jetson@jetson-desktop:~/catkin_ws/src/ai_race/ai_race/learning/scripts$ python3 train.py --data_csv /home/jetson/Images_from_rosbag/_2020-12-13-14-04-25/_2020-12-13-14-04-25.csv --model_name sample_model 
/home/jetson/Images_from_rosbag/_2020-12-13-14-04-25/_2020-12-13-14-04-25.csv
data set
model set
optimizer set
Train starts
batch:  10/12 , train acc: 0.627273, train loss: 0.034951
confusion_matrix
[[ 0  0]
 [22 35]]
classification_report
/home/jetson/.local/lib/python3.6/site-packages/sklearn/metrics/_classification.py:1221: UndefinedMetricWarning: Recall and F-score are ill-defined and being set to 0.0 in labels with no true samples. Use `zero_division` parameter to control this behavior.
  _warn_prf(average, modifier, msg_start, len(result))
              precision    recall  f1-score   support

           1       0.00      0.00      0.00         0
           2       1.00      0.61      0.76        57

    accuracy                           0.61        57
   macro avg       0.50      0.31      0.38        57
weighted avg       1.00      0.61      0.76        57

epoch:   1, train acc: 0.637168, train loss: 0.035825, test acc: 0.614035, test loss: 0.12942 
Saved a model checkpoint at /home/jetson/work/experiments/models/checkpoints/sim_race_sample_model_epoch=1.pth

batch:  10/12 , train acc: 0.777273, train loss: 0.022433
epoch:   2, train acc: 0.774336, train loss: 0.025137
batch:  10/12 , train acc: 0.790909, train loss: 0.020291
epoch:   3, train acc: 0.787611, train loss: 0.023251
batch:  10/12 , train acc: 0.831818, train loss: 0.01789 
epoch:   4, train acc: 0.831858, train loss: 0.019223
batch:  10/12 , train acc: 0.872727, train loss: 0.01408 
epoch:   5, train acc: 0.867257, train loss: 0.015755
batch:  10/12 , train acc: 0.931818, train loss: 0.009815
confusion_matrix
[[18  5]
 [ 4 30]]
classification_report
              precision    recall  f1-score   support

           1       0.82      0.78      0.80        23
           2       0.86      0.88      0.87        34

    accuracy                           0.84        57
   macro avg       0.84      0.83      0.83        57
weighted avg       0.84      0.84      0.84        57

epoch:   6, train acc: 0.933628, train loss: 0.010478, test acc: 0.842105, test loss: 0.020495
Saved a model checkpoint at /home/jetson/work/experiments/models/checkpoints/sim_race_sample_model_epoch=6.pth

batch:  10/12 , train acc: 0.904545, train loss: 0.012203
epoch:   7, train acc: 0.90708 , train loss: 0.012534
batch:  10/12 , train acc: 0.859091, train loss: 0.012649
epoch:   8, train acc: 0.853982, train loss: 0.014423
batch:  10/12 , train acc: 0.913636, train loss: 0.010956
epoch:   9, train acc: 0.911504, train loss: 0.013342
batch:  10/12 , train acc: 0.940909, train loss: 0.007541
epoch:  10, train acc: 0.942478, train loss: 0.007637
batch:  10/12 , train acc: 0.963636, train loss: 0.00443 
confusion_matrix
[[ 4  1]
 [18 34]]
classification_report
              precision    recall  f1-score   support

           1       0.18      0.80      0.30         5
           2       0.97      0.65      0.78        52

    accuracy                           0.67        57
   macro avg       0.58      0.73      0.54        57
weighted avg       0.90      0.67      0.74        57

epoch:  11, train acc: 0.960177, train loss: 0.005791, test acc: 0.666667, test loss: 0.100823
Saved a model checkpoint at /home/jetson/work/experiments/models/checkpoints/sim_race_sample_model_epoch=11.pth

batch:  10/12 , train acc: 0.95    , train loss: 0.007437
epoch:  12, train acc: 0.946903, train loss: 0.010217
batch:  10/12 , train acc: 0.85    , train loss: 0.015337
epoch:  13, train acc: 0.853982, train loss: 0.01633 
batch:  10/12 , train acc: 0.940909, train loss: 0.008117
epoch:  14, train acc: 0.933628, train loss: 0.010373
batch:  10/12 , train acc: 0.931818, train loss: 0.010007
epoch:  15, train acc: 0.924779, train loss: 0.014763
batch:  10/12 , train acc: 0.904545, train loss: 0.010531
confusion_matrix
[[15  9]
 [ 7 26]]
classification_report
              precision    recall  f1-score   support

           1       0.68      0.62      0.65        24
           2       0.74      0.79      0.76        33

    accuracy                           0.72        57
   macro avg       0.71      0.71      0.71        57
weighted avg       0.72      0.72      0.72        57

epoch:  16, train acc: 0.902655, train loss: 0.011367, test acc: 0.719298, test loss: 0.033263
Saved a model checkpoint at /home/jetson/work/experiments/models/checkpoints/sim_race_sample_model_epoch=16.pth

batch:  10/12 , train acc: 0.931818, train loss: 0.00628 
epoch:  17, train acc: 0.933628, train loss: 0.006984
batch:  10/12 , train acc: 0.968182, train loss: 0.005619
epoch:  18, train acc: 0.969027, train loss: 0.005742
batch:  10/12 , train acc: 0.986364, train loss: 0.002123
epoch:  19, train acc: 0.986726, train loss: 0.002295
batch:  10/12 , train acc: 0.990909, train loss: 0.00181 
epoch:  20, train acc: 0.99115 , train loss: 0.00207 
Saved a model checkpoint at /home/jetson/work/experiments/models/checkpoints/sim_race_sample_model_epoch=20.pth

finished successfully.
```

#### trt_conversion.py
入力：学習モデル　`--pretrained_model`引数に与えたファイル<br>
出力：学習モデル（TRT版）　`--trt_model`引数に与えたファイル名<br>
期待値：実行したディレクトリに、学習モデル（TRT版）が出力されること<br>

```
jetson@jetson-desktop:~/catkin_ws/src/ai_race/ai_race/learning/scripts$ python3 trt_conversion.py --pretrained_model /home/jetson/work/experiments/models/checkpoints/sim_race_sample_model_epoch=20.pth --trt_model sim_race_model_trt_20201213.pth
process start...
finished successfully.
model_path: sim_race_model_trt_20201213.pth
```

#### inference_from_image.py
入力：学習モデル（TRT版）　`--trt_model`引数に与えたファイル<br>
出力：車両制御コマンド<br>
期待値：`prepare.sh`で事前実行したシミュレータ上の車両が走り出すこと<br>

```
jetson@jetson-desktop:~/catkin_ws/src/ai_race/ai_race/learning/scripts$ python inference_from_image.py --trt_module --trt_model sim_race_model_trt_20201213.pth 
WARNING: TensorRT Python 2 support is deprecated, and will be dropped in a future version!
[1]
time_each:8.642[sec]
[1]
time_each:2.847[sec]
[1]
time_each:0.041[sec]
[1]
time_each:0.043[sec]
[1]
time_each:0.040[sec]
[1]
time_each:0.043[sec]
[1]
time_each:0.037[sec]
[1]
time_each:0.039[sec]
...
```
