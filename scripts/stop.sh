#!/bin/bash

function try_kill_process(){
    PROCESS_NAME=$1
    if [ -z "$PROCESS_NAME" ]; then
	return 0
    fi
    
    PROCESS_ID=`ps -e -o pid,cmd | grep ${PROCESS_NAME} | grep -v grep | awk '{print $1}'`
    if [ -z "$PROCESS_ID" ]; then
	echo "no process like... ${PROCESS_NAME}"
	return 0
    fi
    echo "kill process ... ${PROCESS_NAME}"
    kill $PROCESS_ID
    
}

function stop_process(){    
    try_kill_process "roscore"
    try_kill_process "judgeServer.py"
    try_kill_process "timer.py"
    try_kill_process "window_management"
    try_kill_process "keyboard_con_pygame"
    try_kill_process "wheel_robot"
    try_kill_process "prepare"
    try_kill_process "inference"
}

stop_process
