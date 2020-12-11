#!/bin/bash -x

# エラー時はエラー終了する
set -e
# 未定義変数参照時はエラーにする
set -u

# default option parameter
LEVEL=1
GAME_TIME=240
PACKAGE_NAME="your_environment"
WITH_GUI="false" #"true"
WITH_CONTROLLER="true" #"false"

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

bash prepare.sh -l ${LEVEL} -p ${PACKAGE_NAME} -t ${GAME_TIME} -g ${WITH_GUI} -c ${WITH_CONTROLLER}
