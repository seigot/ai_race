# -*- coding: utf-8 -*-
import os
import datetime
import time
import argparse
import json
import threading
## flask
from flask import Flask, request, jsonify, render_template
from flask import send_from_directory
## for server debug logger
import logging
from logging.handlers import RotatingFileHandler

## general definition
DEFAULT_GAME_TIME=240

## flask
app = Flask(__name__)


class GameManagerClass:

    ####
    # State
    #  Init --> Start --> Stop
    ####
    
    def __init__(self, args):
        self.time_max = args.gametime # [sec]
        self.initGameData()

    def setJudgeState(self, state):
        app.logger.info("setState")
        if state != "init" and state != "start" and state != "stop":
            print("invalid state." + state)
            return False

        self.judgestate = state
        return True

    def initGameData(self):
        self.setJudgeState("init")
        self.start_time = 0.00
        self.passed_time = 0.00
        self.lap_count = 0

    def startGame(self):
        self.setJudgeState("start")
        self.start_time = time.time()
        return True

    def stopGame(self):
        if self.judgestate == "stop":
            return True
        self.setJudgeState("stop")
        self.writeResult()
        return True

    def requestToServer(self, body):
        app.logger.info("requestToServer")

        # check what is requested
        ## change_state
        if "change_state" in body:
            change_state = body["change_state"]
            if change_state == "init":
                self.initGameData()
            elif change_state == "start":
                self.startGame()
            elif change_state == "stop":
                self.stopGame()
            else:
                print("invalid request")
                return False
        else:
            print("invalid request")
            return False
        return True

    def updateTime(self):
        app.logger.info("updateTime")
        if self.judgestate == "init":
            self.passed_time = 0.00
            return False

        # update time
        self.passed_time = time.time() - self.start_time
        # check if time is over
        if self.passed_time >= self.time_max:
            self.stopGame()

        app.logger.info("passed_Time {}".format(self.passed_time))
        return True

    def updateData(self, body):
        app.logger.info("updateData")

        # check which data is requested to update
        ## lap count
        if "lap_count" in body:
            self.lap_count = self.lap_count + int(body["lap_count"])
        else:
            print("invalid RaceData")
            return False
        return True

    def getGameStateJson(self):
        self.updateTime()

        # state data to json
        json = {
            "field_info": {
                "description": "field information",
            },
            "vehicle_info": {
                "description": "vehicle information",
            },
            "judge_info": {
                "description": "judge information",
                "time": self.passed_time,
                "time_max": self.time_max,
                "lap_count": self.lap_count,
                "judgestate": self.judgestate,
            },
            "debug_info": {
                "description": "debug information",
            },
        }
        return json

    def writeResult(self):
        ## For Debug, output Result file.
        script_dir = os.path.dirname(os.path.abspath(__file__))
        log_file_path = script_dir + "/log/" + "game_result.log"
        with open(log_file_path, "w") as f:
            jsondata = self.getGameStateJson()
            json.dump(jsondata, f)
            app.logger.info("Write Result {}".format(jsondata))


### API definition
@app.route('/')
def index():
    ip = request.remote_addr
    app.logger.info("GET /(root) "+ str(ip))
    return render_template('index.html')

#@app.route('/favicon.ico')
#def favicon():
#    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='static/')

@app.route('/judgeserver/request', methods=['POST'])
def requestToJudge():
    print("request to POST /judgeserver/request")
    body = request.json
    ip = request.remote_addr
    app.logger.info("POST /judgeserver/request " + str(ip) + str(body))
    response = GameManager.requestToServer(body)
    res = response
    app.logger.info("RESPONSE /judgeserver/request " + str(ip) + str(res))
    return jsonify(res)

@app.route('/judgeserver/updateData', methods=['POST'])
def updateData():
    print("request to POST /judgeserver/updateData")
    body = request.json
    ip = request.remote_addr
    app.logger.info("POST /judgeserver/updateData " + str(ip) + str(body))
    response = GameManager.updateData(body)
    res = response
    app.logger.info("RESPONSE /judgeserver/updateData " + str(ip) + str(res))
    return jsonify(res)

@app.route('/judgeserver/getState', methods=['GET'])
def getState():
    print("request to GET /judgeserver/getState")
    ip = request.remote_addr
    #app.logger.info("GET /judgeserver/getState " + str(ip))
    state_json = GameManager.getGameStateJson()
    res = state_json
    #app.logger.info("RESPONSE /judgeserver/getState "+ str(ip) + str(res))
    return jsonify(res)

def parse_argument():
    # argument parse
    parser = argparse.ArgumentParser(description='judger server')
    parser.add_argument('--gametime', '--gt', default=int(DEFAULT_GAME_TIME), type=int, help='game time [sec]')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    # global object judge
    GameManager = GameManagerClass(parse_argument())

    # app for debug
    now = datetime.datetime.now()
    now_str = now.strftime("%y%m%d_%H%M%S")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_file_path = script_dir + "/log/" + now_str + ".log"
    handler = RotatingFileHandler(log_file_path, maxBytes = 1000000, backupCount=100)
    handler.setLevel(logging.INFO)
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True, host='0.0.0.0', port=5000)
