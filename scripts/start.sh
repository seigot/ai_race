#!/bin/bash -x

echo "start start.sh"

pushd /home/jetson/ai_race/catkin_ws/src/user_tutorial2/scripts
python inference_from_image.py --pretrained_model /home/jetson/ai_race/catkin_ws/src/experiments/models/checkpoints/sim_race_joycon_ResNet18_6_epoch=20.pth
popd
