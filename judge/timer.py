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

        # update frequency
        self.TimerUpdate_mSec = 500
        
        # setting geometry
        upper_left = (100,100)
        width_height = (600, 320)
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
        label_upper_left = (10, 10)
        label_width_height = (580, 210)
        self.label.setGeometry(label_upper_left[0], label_upper_left[1], 
                               label_width_height[0], label_width_height[1]) 
        self.label.setStyleSheet("border : 4px solid black;") 
        self.label.setText(self.gettimertext())
        self.label.setFont(QFont('Arial', 25))
        self.label.setAlignment(Qt.AlignCenter) 
  
        # create init button 
        init = QPushButton("Init", self) 
        init_upper_left = (15, 230)
        init_width_height = (90, 40)
        init.setGeometry(init_upper_left[0], init_upper_left[1], 
                         init_width_height[0], init_width_height[1])
        init.pressed.connect(self.Init)

        # create start button
        start = QPushButton("Start", self) 
        start_upper_left = (110, 230)
        start_width_height = (90, 40)
        start.setGeometry(start_upper_left[0], start_upper_left[1],
                          start_width_height[0], start_width_height[1])
        start.pressed.connect(self.Start)

        # create stop button 
        stop = QPushButton("Stop", self) 
        stop_upper_left = (205, 230)
        stop_width_height = (90, 40)
        stop.setGeometry(stop_upper_left[0], stop_upper_left[1],
                          stop_width_height[0], stop_width_height[1])
        stop.pressed.connect(self.Stop)

        # create Manual Recovery button
        ManualRecovery = QPushButton("Manual\nRecovery", self) 
        ManualRecovery_upper_left = (300, 230)
        ManualRecovery_width_height = (90, 40)
        ManualRecovery.setGeometry(ManualRecovery_upper_left[0], ManualRecovery_upper_left[1],
                          ManualRecovery_width_height[0], ManualRecovery_width_height[1])
        ManualRecovery.pressed.connect(self.ManualRecovery)
        ManualRecovery.setFont(QFont("Meiryo", 9))

        # create ConeCount button
        name_coneA = "cone_A"
        ConeA = QPushButton(name_coneA, self) 
        ConeA_upper_left = (395, 230)
        ConeA_width_height = (50, 20)
        ConeA.setGeometry(ConeA_upper_left[0], ConeA_upper_left[1],
                          ConeA_width_height[0], ConeA_width_height[1])
        ConeA.pressed.connect(lambda: self.UpdateConeCount(name_coneA))
        ConeA.setFont(QFont("Meiryo", 8))

        name_coneB = "cone_B"
        ConeB = QPushButton(name_coneB, self) 
        ConeB_upper_left = (445, 230)
        ConeB_width_height = (50, 20)
        ConeB.setGeometry(ConeB_upper_left[0], ConeB_upper_left[1],
                          ConeB_width_height[0], ConeB_width_height[1])
        ConeB.pressed.connect(lambda: self.UpdateConeCount(name_coneB))
        ConeB.setFont(QFont("Meiryo", 8))        

        name_coneC = "cone_C"
        ConeC = QPushButton(name_coneC, self) 
        ConeC_upper_left = (495, 230)
        ConeC_width_height = (50, 20)
        ConeC.setGeometry(ConeC_upper_left[0], ConeC_upper_left[1],
                          ConeC_width_height[0], ConeC_width_height[1])
        ConeC.pressed.connect(lambda: self.UpdateConeCount(name_coneC))
        ConeC.setFont(QFont("Meiryo", 8))

        name_coneD = "cone_D"
        ConeD = QPushButton(name_coneD, self) 
        ConeD_upper_left = (545, 230)
        ConeD_width_height = (50, 20)
        ConeD.setGeometry(ConeD_upper_left[0], ConeD_upper_left[1],
                          ConeD_width_height[0], ConeD_width_height[1])
        ConeD.pressed.connect(lambda: self.UpdateConeCount(name_coneD))
        ConeD.setFont(QFont("Meiryo", 8))

        name_coneE = "cone_E"
        ConeE = QPushButton(name_coneE, self) 
        ConeE_upper_left = (395, 250)
        ConeE_width_height = (50, 20)
        ConeE.setGeometry(ConeE_upper_left[0], ConeE_upper_left[1],
                          ConeE_width_height[0], ConeE_width_height[1])
        ConeE.pressed.connect(lambda: self.UpdateConeCount(name_coneE))
        ConeE.setFont(QFont("Meiryo", 8))

        name_coneF = "cone_F"        
        ConeF = QPushButton(name_coneF, self) 
        ConeF_upper_left = (445, 250)
        ConeF_width_height = (50, 20)
        ConeF.setGeometry(ConeF_upper_left[0], ConeF_upper_left[1],
                          ConeF_width_height[0], ConeF_width_height[1])
        ConeF.pressed.connect(lambda: self.UpdateConeCount(name_coneF))
        ConeF.setFont(QFont("Meiryo", 8))

        name_coneG = "cone_G"
        ConeG = QPushButton(name_coneG, self) 
        ConeG_upper_left = (495, 250)
        ConeG_width_height = (50, 20)
        ConeG.setGeometry(ConeG_upper_left[0], ConeG_upper_left[1],
                          ConeG_width_height[0], ConeG_width_height[1])
        ConeG.pressed.connect(lambda: self.UpdateConeCount(name_coneG))
        ConeG.setFont(QFont("Meiryo", 8))

        # create lap_count Plus/Minus button 
        lapcountPlus = QPushButton("Lap++", self) 
        lapcountPlus_upper_left = (15, 275)
        lapcountPlus_width_height = (90, 40)
        lapcountPlus.setGeometry(lapcountPlus_upper_left[0], lapcountPlus_upper_left[1],
                             lapcountPlus_width_height[0], lapcountPlus_width_height[1])
        lapcountPlus.pressed.connect(self.LapCount_plus) 

        lapcountMinus = QPushButton("Lap--", self) 
        lapcountMinus_upper_left = (110, 275)
        lapcountMinus_width_height = (90, 40)
        lapcountMinus.setGeometry(lapcountMinus_upper_left[0], lapcountMinus_upper_left[1],
                             lapcountMinus_width_height[0], lapcountMinus_width_height[1])
        lapcountMinus.pressed.connect(self.LapCount_minus)

        # create CourseOutCount Plus/Minus button 
        CourseOutCountPlus = QPushButton("CourseOut++", self) 
        CourseOutCountPlus_upper_left = (205, 275)
        CourseOutCountPlus_width_height = (90, 40)
        CourseOutCountPlus.setGeometry(CourseOutCountPlus_upper_left[0], CourseOutCountPlus_upper_left[1],
                             CourseOutCountPlus_width_height[0], CourseOutCountPlus_width_height[1])
        CourseOutCountPlus.pressed.connect(self.CourseOutCount_plus) 
        CourseOutCountPlus.setFont(QFont("Meiryo", 9))

        CourseOutCountMinus = QPushButton("CourseOut--", self) 
        CourseOutCountMinus_upper_left = (300, 275)
        CourseOutCountMinus_width_height = (90, 40)
        CourseOutCountMinus.setGeometry(CourseOutCountMinus_upper_left[0], CourseOutCountMinus_upper_left[1],
                             CourseOutCountMinus_width_height[0], CourseOutCountMinus_width_height[1])
        CourseOutCountMinus.pressed.connect(self.CourseOutCount_minus)
        CourseOutCountMinus.setFont(QFont("Meiryo", 9))

        # create RecoveryCount Plus/Minus button 
        RecoveryCountPlus = QPushButton("Recovery++", self) 
        RecoveryCountPlus_upper_left = (395, 275)
        RecoveryCountPlus_width_height = (90, 40)
        RecoveryCountPlus.setGeometry(RecoveryCountPlus_upper_left[0], RecoveryCountPlus_upper_left[1],
                             RecoveryCountPlus_width_height[0], RecoveryCountPlus_width_height[1])
        RecoveryCountPlus.pressed.connect(self.RecoveryCount_plus) 
        RecoveryCountPlus.setFont(QFont("Meiryo", 9))

        RecoveryCountMinus = QPushButton("Recovery--", self) 
        RecoveryCountMinus_upper_left = (490, 275)
        RecoveryCountMinus_width_height = (90, 40)
        RecoveryCountMinus.setGeometry(RecoveryCountMinus_upper_left[0], RecoveryCountMinus_upper_left[1],
                             RecoveryCountMinus_width_height[0], RecoveryCountMinus_width_height[1])
        RecoveryCountMinus.pressed.connect(self.RecoveryCount_minus)
        RecoveryCountMinus.setFont(QFont("Meiryo", 9))

        # creating a timer object 
        timer = QTimer(self) 
        timer.timeout.connect(self.callback_showTime)
        timer.start(self.TimerUpdate_mSec) # update the timer by n(msec)

    # timer callback function 
    def callback_showTime(self):
        # showing text 
        text = self.gettimertext()
        if text is None:
            return
        self.label.setText(text)

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

    # ConeCount button
    def UpdateConeCount(self, name):
        url = JUDGESERVER_UPDATEDATA_URL
        req_data = {
            "cone": {
                "name" : name,
                "count" : 1
                }
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
            lap_time_lst = data["judge_info"]["lap_time"]["system_time"]
            time_mode_str = "System Time: "
        else:
            elapsed_time = data["judge_info"]["elapsed_time"]["ros_time"]
            lap_time_lst = data["judge_info"]["lap_time"]["ros_time"]
            time_mode_str = "ROS Time: "
        time_max = int(data["judge_info"]["time_max"])

        lap_count = data["judge_info"]["lap_count"]
        recovery_count = data["judge_info"]["recovery_count"]
        courseout_count = data["judge_info"]["courseout_count"]
        cone_collision_counts = data["judge_info"]["collision_count"]["cone"]
        #print(cone_collision_counts)
        #courseout_count = 0
        judgestate = data["judge_info"]["judgestate"]

        # get lap_time
        lap_time_lst_length = len(lap_time_lst)
        if lap_time_lst_length <= 0:
            lap_time = 0
        else:
            lap_time = lap_time_lst[lap_time_lst_length - 1]

        # timer text
        passed_time_str = str('{:.2f}'.format(elapsed_time))
        time_max_str = str('{:}'.format(time_max))
        lap_count_str = str(lap_count)
        recovery_count_str = str(recovery_count)
        courseout_count_str = str(courseout_count)
        judgestate_str = str(judgestate)
        lap_time_str = str('{:.2f}'.format(lap_time))
        cone_collision_counts_str = str(cone_collision_counts)
        # update check
        if elapsed_time > (time_max + self.TimerUpdate_mSec/1000):
            return None
        
        # update timer text
        text = "JudgeState: " + judgestate_str + "\n" \
               + time_mode_str + passed_time_str + " / " + time_max_str + " (s)" + "\n" \
               + "LAP Time: " + lap_time_str + " (s)" + "\n" \
               + "LAP: " + lap_count_str + "  " \
               + "CourseOut: " + courseout_count_str + "  " \
               + "Recovery: " + recovery_count_str + "\n" \
               + "Cone Collision: " + cone_collision_counts_str 

        return text

# create pyqt5 app 
App = QApplication(sys.argv) 
  
# create the instance of our Window 
window = Window() 
  
# start the app 
sys.exit(App.exec()) 
