#!/bin/bash -x

# usage
#  bash start.sh --trt_model=$HOME/ai_race_data_sample/model/plane/sample_plane_trt.pth

# default
TRT_MODEL="$HOME/ai_race_data_sample/model/plane/sample_plane_trt.pth"
IMAGE_TOPIC_NAME="/front_camera/image_exp"

# parse option
while [ $# -gt 0 ]
do
  case $1 in
    --trt_model=*) TRT_MODEL="${1#--trt_model=}";;
    --image_topic_name=*) IMAGE_TOPIC_NAME="${1#--image_topic_name=}";;
    -*) opterr=true; echo "invalid option: $1";;
    *)  argv+=("$1");; # argv++
  esac
  shift
done

echo "start start.sh"
echo ${TRT_MODEL}

roslaunch learning inference_from_image.launch trt_model:=$TRT_MODEL image_topic_name:=$IMAGE_TOPIC_NAME
