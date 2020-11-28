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

mkdir -p learning/scripts
#cp ../learning/scripts/inference_from_image.py ./learning/scripts
#cp ../learning/scripts/road_following_model_trt.pth ./learning/scripts
cp ../learning/scripts/MyDataSet.py ./learning/scripts
cp ../learning/scripts/train.py ./learning/scripts

mkdir launch
cp ../sim_environment/launch/* ./launch

mkdir utility
cp ../utility/scripts/* ./utility
