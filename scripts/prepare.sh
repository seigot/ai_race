#!/bin/bash -x

# エラー時はエラー終了する
set -e
# 未定義変数参照時はエラーにする
set -u

# default option parameter
LEVEL=1

# option
while getopts l:a: OPT
do
    case $OPT in
        "l" ) LEVEL=$OPTARG; echo "LEVEL: $LEVEL";;
    esac
done

echo "start prepare.sh"

# init judge server, timer window, etc
gnome-terminal -e "python3 judge/judgeServer.py"
sleep 1
gnome-terminal -e "python3 judge/timer.py"
# [future work] if necessary, register some data to server here.

# init simulator, course and vehicle
roslaunch user_tutorial1 wheel_robot.launch
