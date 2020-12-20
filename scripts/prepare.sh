#!/bin/bash -x

# エラー時はエラー終了する
set -e
# 未定義変数参照時はエラーにする
set -u

# default option parameter
LEVEL=1
GAME_TIME=240
TIME_MODE=2
PACKAGE_NAME="your_environment"
WITH_GUI="true"
WITH_CONTROLLER="false"

# option
while getopts l:p:t:g:c: OPT
do
    case $OPT in
        "l" ) LEVEL=$OPTARG ;;
        "p" ) PACKAGE_NAME=$OPTARG ;;
        "t" ) GAME_TIME=$OPTARG ;;
        "g" ) WITH_GUI="$OPTARG" ;;
        "c" ) WITH_CONTROLLER="$OPTARG" ;;
    esac
done

echo "start prepare.sh"
echo "LEVEL: ${LEVEL}"
echo "PACKAGE_NAME: ${PACKAGE_NAME}"
echo "GAME_TIME: ${GAME_TIME}"
echo "TIME_MODE: ${TIME_MODE} (1:SYSTEM TIME/2:ROS Time)"
echo "WITH_GUI: ${WITH_GUI}"
echo "WITH_CONTROLLER: ${WITH_CONTROLLER}"

# warning
function output_warning(){
    local LEVEL=$1
    local CNT=0
    echo "---"
    # check if install package
    if [ ${LEVEL} != "1" ]; then
	array=(
	    ros-melodic-cob-srvs
	)
	for e in ${array[@]}; do
	    if ! dpkg -l | grep --quiet "${e}"; then
		echo "!!! [Warning] ${e} not installed, install by following !!!"
		echo "\$ sudo apt install ${e}"
		sudo apt install -y ${e}
		echo "install end. if error end, please install manually..."
		echo "!!! --------------------------------------------- !!!"
		CNT=$(($CNT+1))
	    fi
	done
    fi
    echo "---"
}
output_warning ${LEVEL}

# init judge server, timer window, etc
gnome-terminal -- python3 ../judge/judgeServer.py --gametime ${GAME_TIME} --timemode ${TIME_MODE}
sleep 1
gnome-terminal -- python3 ../judge/timer.py
# [future work] if necessary, register some data to server here.

# init simulator, course and vehicle
roslaunch ${PACKAGE_NAME} sim_environment.launch level:=${LEVEL} gui:=${WITH_GUI} controller:=${WITH_CONTROLLER}

#roslaunch your_environment your_environment.launch level:=${LEVEL}
#roslaunch sim_environment sim_environment.launch level:=${LEVEL}


