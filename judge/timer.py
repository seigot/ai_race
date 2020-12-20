## qt5
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys 
## http communication
import requests
from time import sleep
import json
import os
import datetime

JUDGESERVER_REQUEST_URL="http://127.0.0.1:5000/judgeserver/request"
JUDGESERVER_UPDATEDATA_URL="http://127.0.0.1:5000/judgeserver/updateData"
JUDGESERVER_GETSTATE_URL="http://127.0.0.1:5000/judgeserver/getState"

class Window(QMainWindow): 
  
    def __init__(self): 
        super().__init__() 
  
        # setting title 
        self.setWindowTitle("Python Stop watch") 

        # setting geometry
        upper_left = (100,100)
        width_height = (600, 240)
        self.setGeometry(upper_left[0], upper_left[1],
                         width_height[0], width_height[1]) 

        # calling method 
        self.UiComponents() 

        # showing all the widgets 
        self.show() 

    # method for widgets 
    def UiComponents(self): 

        # creating a label to show the time 
        self.label = QLabel(self)
        label_upper_left = (20, 10)
        label_width_height = (560, 130)
        self.label.setGeometry(label_upper_left[0], label_upper_left[1], 
                               label_width_height[0], label_width_height[1]) 
        self.label.setStyleSheet("border : 4px solid black;") 
        self.label.setText(self.gettimertext())
        self.label.setFont(QFont('Arial', 25))
        self.label.setAlignment(Qt.AlignCenter) 
  
        # create init button 
        init = QPushButton("Init", self) 
        init_upper_left = (15, 150)
        init_width_height = (90, 40)
        init.setGeometry(init_upper_left[0], init_upper_left[1], 
                         init_width_height[0], init_width_height[1])
        init.pressed.connect(self.Init)

        # create start button
        start = QPushButton("Start", self) 
        start_upper_left = (110, 150)
        start_width_height = (90, 40)
        start.setGeometry(start_upper_left[0], start_upper_left[1],
                          start_width_height[0], start_width_height[1])
        start.pressed.connect(self.Start)

        # create stop button 
        stop = QPushButton("Stop", self) 
        stop_upper_left = (205, 150)
        stop_width_height = (90, 40)
        stop.setGeometry(stop_upper_left[0], stop_upper_left[1],
                          stop_width_height[0], stop_width_height[1])
        stop.pressed.connect(self.Stop)

        # create Manual Recovery button
        ManualRecovery = QPushButton("Manual\nRecovery", self) 
        ManualRecovery_upper_left = (300, 150)
        ManualRecovery_width_height = (90, 40)
        ManualRecovery.setGeometry(ManualRecovery_upper_left[0], ManualRecovery_upper_left[1],
                          ManualRecovery_width_height[0], ManualRecovery_width_height[1])
        ManualRecovery.pressed.connect(self.ManualRecovery)
        ManualRecovery.setFont(QFont("Meiryo", 9))

        # create lap_count Plus/Minus button 
        lapcountPlus = QPushButton("Lap++", self) 
        lapcountPlus_upper_left = (15, 195)
        lapcountPlus_width_height = (90, 40)
        lapcountPlus.setGeometry(lapcountPlus_upper_left[0], lapcountPlus_upper_left[1],
                             lapcountPlus_width_height[0], lapcountPlus_width_height[1])
        lapcountPlus.pressed.connect(self.LapCount_plus) 

        lapcountMinus = QPushButton("Lap--", self) 
        lapcountMinus_upper_left = (110, 195)
        lapcountMinus_width_height = (90, 40)
        lapcountMinus.setGeometry(lapcountMinus_upper_left[0], lapcountMinus_upper_left[1],
                             lapcountMinus_width_height[0], lapcountMinus_width_height[1])
        lapcountMinus.pressed.connect(self.LapCount_minus)

        # create CourseOutCount Plus/Minus button 
        CourseOutCountPlus = QPushButton("CourseOut++", self) 
        CourseOutCountPlus_upper_left = (205, 195)
        CourseOutCountPlus_width_height = (90, 40)
        CourseOutCountPlus.setGeometry(CourseOutCountPlus_upper_left[0], CourseOutCountPlus_upper_left[1],
                             CourseOutCountPlus_width_height[0], CourseOutCountPlus_width_height[1])
        CourseOutCountPlus.pressed.connect(self.CourseOutCount_plus) 
        CourseOutCountPlus.setFont(QFont("Meiryo", 9))

        CourseOutCountMinus = QPushButton("CourseOut--", self) 
        CourseOutCountMinus_upper_left = (300, 195)
        CourseOutCountMinus_width_height = (90, 40)
        CourseOutCountMinus.setGeometry(CourseOutCountMinus_upper_left[0], CourseOutCountMinus_upper_left[1],
                             CourseOutCountMinus_width_height[0], CourseOutCountMinus_width_height[1])
        CourseOutCountMinus.pressed.connect(self.CourseOutCount_minus)
        CourseOutCountMinus.setFont(QFont("Meiryo", 9))

        # create RecoveryCount Plus/Minus button 
        RecoveryCountPlus = QPushButton("Recovery++", self) 
        RecoveryCountPlus_upper_left = (395, 195)
        RecoveryCountPlus_width_height = (90, 40)
        RecoveryCountPlus.setGeometry(RecoveryCountPlus_upper_left[0], RecoveryCountPlus_upper_left[1],
                             RecoveryCountPlus_width_height[0], RecoveryCountPlus_width_height[1])
        RecoveryCountPlus.pressed.connect(self.RecoveryCount_plus) 
        RecoveryCountPlus.setFont(QFont("Meiryo", 9))

        RecoveryCountMinus = QPushButton("Recovery--", self) 
        RecoveryCountMinus_upper_left = (490, 195)
        RecoveryCountMinus_width_height = (90, 40)
        RecoveryCountMinus.setGeometry(RecoveryCountMinus_upper_left[0], RecoveryCountMinus_upper_left[1],
                             RecoveryCountMinus_width_height[0], RecoveryCountMinus_width_height[1])
        RecoveryCountMinus.pressed.connect(self.RecoveryCount_minus)
        RecoveryCountMinus.setFont(QFont("Meiryo", 9))

        # creating a timer object 
        timer = QTimer(self) 
        timer.timeout.connect(self.callback_showTime)
        timer.start(500) # update the timer by n(msec)

    # timer callback function 
    def callback_showTime(self):
        # showing text 
        self.label.setText(self.gettimertext())

    def httpGetReqToURL(self, url):
        resp = requests.get(url)
        data = json.loads(resp.text)
        return data

    # http request
    def httpPostReqToURL(self, url, data):
        res = requests.post(url,
                            json.dumps(data),
                            headers={'Content-Type': 'application/json'}
                            )
        return res

    # init button
    def Init(self):
        url = JUDGESERVER_REQUEST_URL
        req_data = {"change_state": "init"}
        res = self.httpPostReqToURL(url, req_data)
        return res

    # start button
    def Start(self):
        url = JUDGESERVER_REQUEST_URL
        req_data = {"change_state": "start"}
        res = self.httpPostReqToURL(url, req_data)
        return res

    # stop button
    def Stop(self):
        url = JUDGESERVER_REQUEST_URL
        req_data = {"change_state": "stop"}
        res = self.httpPostReqToURL(url, req_data)
        return res

    # ManualRecovery button
    def ManualRecovery(self):
        url = JUDGESERVER_UPDATEDATA_URL
        req_data = {
            # "courseout_count": 1,
            "is_courseout": 1
        }
        res = self.httpPostReqToURL(url, req_data)
        return res

    # lap count button
    def LapCount_plus(self):
        # request POST data to server
        url = JUDGESERVER_UPDATEDATA_URL
        req_data = {"lap_count": 1}
        res = self.httpPostReqToURL(url, req_data)
        return res

    def LapCount_minus(self):
        # request POST data to server
        url = JUDGESERVER_UPDATEDATA_URL
        req_data = {"lap_count": -1}
        res = self.httpPostReqToURL(url, req_data)
        return res

    # courseout count button
    def CourseOutCount_plus(self):
        # request POST data to server
        url = JUDGESERVER_UPDATEDATA_URL
        req_data = {"courseout_count": 1}
        res = self.httpPostReqToURL(url, req_data)
        return res

    def CourseOutCount_minus(self):
        # request POST data to server
        url = JUDGESERVER_UPDATEDATA_URL
        req_data = {"courseout_count": -1}
        res = self.httpPostReqToURL(url, req_data)
        return res

    # recovery count button
    def RecoveryCount_plus(self):
        # request POST data to server
        url = JUDGESERVER_UPDATEDATA_URL
        req_data = {"recovery_count": 1}
        res = self.httpPostReqToURL(url, req_data)
        return res

    def RecoveryCount_minus(self):
        # request POST data to server
        url = JUDGESERVER_UPDATEDATA_URL
        req_data = {"recovery_count": -1}
        res = self.httpPostReqToURL(url, req_data)
        return res

    def gettimertext(self):
        # request GET data to server
        url = JUDGESERVER_GETSTATE_URL
        data = self.httpGetReqToURL(url)

        time_mode = int(data["judge_info"]["time_mode"])
        if time_mode == 1:
            elapsed_time = data["judge_info"]["elapsed_time"]["system_time"]
            time_mode_str = "System Time: "
        else:
            elapsed_time = data["judge_info"]["elapsed_time"]["ros_time"]
            time_mode_str = "ROS Time: "
        time_max = int(data["judge_info"]["time_max"])

        lap_count = data["judge_info"]["lap_count"]
        recovery_count = data["judge_info"]["recovery_count"]
        courseout_count = data["judge_info"]["courseout_count"]
        #courseout_count = 0
        judgestate = data["judge_info"]["judgestate"]

        # timer text
        passed_time_str = str('{:.2f}'.format(elapsed_time))
        time_max_str = str('{:}'.format(time_max))
        lap_count_str = str(lap_count)
        recovery_count_str = str(recovery_count)
        courseout_count_str = str(courseout_count)
        judgestate_str = str(judgestate)

        text = "JudgeState: " + judgestate_str + "\n" \
               + time_mode_str + passed_time_str + " / " + time_max_str + " (s)""\n" \
               + "LAP: " + lap_count_str + "  " \
               + "CourseOut: " + courseout_count_str + "  " \
               + "Recovery: " + recovery_count_str

        return text

# create pyqt5 app 
App = QApplication(sys.argv) 
  
# create the instance of our Window 
window = Window() 
  
# start the app 
sys.exit(App.exec()) 
