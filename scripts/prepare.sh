#!/bin/bash -x

# エラー時はエラー終了する
set -e
# 未定義変数参照時はエラーにする
set -u

# default option parameter
LEVEL=1
GAME_TIME=240
PACKAGE_NAME="your_environment"

# option
while getopts l:p:t: OPT
do
    case $OPT in
        "l" ) LEVEL=$OPTARG ;;
        "p" ) PACKAGE_NAME=$OPTARG ;;
        "t" ) GAME_TIME=$OPTARG ;;
    esac
done

echo "start prepare.sh"
echo "LEVEL: ${LEVEL}"
echo "PACKAGE_NAME: ${PACKAGE_NAME}"
echo "GAME_TIME: ${GAME_TIME}"


# init judge server, timer window, etc
gnome-terminal -- python3 ../judge/judgeServer.py --gametime ${GAME_TIME}
sleep 1
gnome-terminal -- python3 ../judge/timer.py
# [future work] if necessary, register some data to server here.

# init simulator, course and vehicle
roslaunch ${PACKAGE_NAME} sim_environment.launch level:=${LEVEL}
#roslaunch your_environment your_environment.launch level:=${LEVEL}
#roslaunch sim_environment sim_environment.launch level:=${LEVEL}


