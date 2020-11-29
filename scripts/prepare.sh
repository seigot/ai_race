#!/bin/bash -x

# エラー時はエラー終了する
set -e
# 未定義変数参照時はエラーにする
set -u

# default option parameter
LEVEL=1
PACKAGE_NAME="sim_environment"

# option
while getopts l:p: OPT
do
    case $OPT in
        "l" ) LEVEL=$OPTARG ;;
        "p" ) PACKAGE_NAME=$OPTARG ;;
    esac
done

echo "start prepare.sh"
echo "LEVEL: ${LEVEL}"
echo "PACKAGE_NAME: ${PACKAGE_NAME}"

# init judge server, timer window, etc
gnome-terminal -- python3 ../judge/judgeServer.py
sleep 1
gnome-terminal -- python3 ../judge/timer.py
# [future work] if necessary, register some data to server here.

# init simulator, course and vehicle
roslaunch ${PACKAGE_NAME} sim_environment.launch level:=${LEVEL}


