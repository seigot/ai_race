#!/bin/bash

# エラーが起こったら異常終了させる
set -E

cd ~/catkin_ws/src/ai_race/ai_race

read -p "チーム全員で実行するとコンフリクトするため一人だけ実行してください、続けますか? (y/N): " yn
case "$yn" in
  [yY]*) echo hello;;
  *) echo "abort"
  exit;;
esac

catkin_create_pkg your_environment

cd your_environment

mkdir config
cp ../sim_environment/config/joint_position_control.yaml ./config

mkdir learning
#cp ../learning/inference_from_image.py ./learning
#cp ../learning/road_following_model_trt.pth ./learning
cp ../learning/MyDataSet.py ./learning
cp ../learning/train.py ./learning

mkdir launch
cp ../sim_environment/launch/* ./launch

mkdir utility
cp ../utility/scripts/* ./utility
