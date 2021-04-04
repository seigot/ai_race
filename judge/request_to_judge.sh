#!/bin/bash

##### request to judge script #####
# option
#   -h host address,
#      use like.. " -h 192.168.2.101:5000 " 
#      default: localhost:5000
#
#   -s change state parameter,
#      use like.. "-s start"
#      parameter  
#         start : start timer
#         stop  : stop timer
#         init  : init timer
#
###################################

# default parameter
HOSTADDR="localhost:5000"
REQ_STATE="start"

while getopts h:s: OPT
do
    case $OPT in
        "h" ) HOSTADDR=$OPTARG; echo "-h host = $HOSTADDR !!";;
        "s" ) REQ_STATE=$OPTARG; echo "-s state = $REQ_STATE !!";;
    esac
done

JUDGESERVER_REQUEST_URL="http://${HOSTADDR}/judgeserver/request"
JUDGESERVER_UPDATEDATA_URL="http://${HOSTADDR}/judgeserver/updateData"
JUDGESERVER_GETSTATE_URL="http://${HOSTADDR}/judgeserver/getState"

########### script ########################
# set state to "running"
echo "=================set state "running"======================"

if [ "$REQ_STATE" == "start" ]; then
    curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"change_state":"start"}' ${JUDGESERVER_REQUEST_URL}
elif [ "$REQ_STATE" == "stop" ]; then
    curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"change_state":"stop"}' ${JUDGESERVER_REQUEST_URL}
elif [ "$REQ_STATE" == "init" ]; then
    curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"change_state":"init"}' ${JUDGESERVER_REQUEST_URL}
elif [ "$REQ_STATE" == "lap_count" ]; then
    curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"lap_count":0.25}' ${JUDGESERVER_UPDATEDATA_URL}
else
    echo "invalid parameter... ${HOSTADDR}, ${REQ_STATE}"
fi



