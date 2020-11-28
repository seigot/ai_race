#!/bin/bash -x

# エラー時はエラー終了する
set -e
# 未定義変数参照時はエラーにする
set -u

# default option parameter
LEVEL=1

# option
while getopts l: OPT
do
    case $OPT in
        "l" ) LEVEL=$OPTARG; echo "LEVEL: $LEVEL";;
    esac
done

echo "start prepare.sh"

# init judge server, timer window, etc
gnome-terminal -- python3 ../judge/judgeServer.py
sleep 1
gnome-terminal -- python3 ../judge/timer.py
# [future work] if necessary, register some data to server here.

# init simulator, course and vehicle

if [ "$LEVEL" -eq 1 ];then
    ## LEVEL1
    roslaunch user_tutorial1 wheel_robot_with_surveillance.launch track_name:="medium_track_plane.world" gui:="true"
elif [ "$LEVEL" -eq 2 ];then
    ## LEVEL2
    roslaunch user_tutorial1 wheel_robot_with_surveillance.launch track_name:="medium_track.world" gui:="true"
elif [ "$LEVEL" -eq 3 ];then
    ## LEVEL3
    ## temporal, planning to update later..
    echo "temporal, planning to update later.."
    roslaunch user_tutorial1 wheel_robot_with_surveillance.launch track_name:="hard_track.world" gui:="true"
else
    echo "invalid LEVEL option -l $LEVEL"
fi

