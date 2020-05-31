import threading
import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QTimer, QTime, QObject
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QGridLayout, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QMessageBox, QPushButton)
from PyQt5.uic import loadUi

import time
import paho.mqtt.client as mqtt

broker = "broker.hivemq.com"
port = 1883
topicsubs = "foo"
topicpubs = "foo"
msgsub = ""
radiobutton = 0

class MyMQTTClass(mqtt.Client):

    def on_message(self, mqttc, obj, msg):
        print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
        msgpayload = str(msg.payload.decode("utf-8"))
        global msgsub; msgsub = msgpayload
        main_window.update_sub()
        print("end")

    def on_log(self, mqttc, obj, level, string):
        print(string)

    def run(self):
        self.connect(broker, port, 60)
        

class MainWindow(QtWidgets.QMainWindow):
    
    
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('mqtt_GUI.ui', self)

        
              
        self.pushButtonSet.clicked.connect(self.ButtonSet_On)
        self.radioButtonSub.toggled.connect(self.RadioButtonSub_On)
        self.pushButtonPubs.clicked.connect(self.ButtonPub_On)
        self.lineSubsTopic.textEdited.connect(self.subTopicChanged)

        timer = QTimer(self)
        timer.timeout.connect(self.refresh)
        timer.start(10)
        
    
    def ButtonSet_On(self):
        host = self.lineBroker.text()
        global broker; broker = str(host)
        por = self.linePort.text()
        global port; port = int(por)

        if(broker == "" or port == ""):
            self.checkBrokerPort()
        else:
            rc = mqttc.run()
            mqttc.loop_start()
            self.status.setText("CONNECTED")
            print("changged")
        

    def ButtonPub_On(self):
        msgpub = self.plainTextPubs.toPlainText()
        tpcpub = self.linePubstopic.text()
        
        if (tpcpub == ""):
            self.checkPubTopic()
            print("null")
            
        else:
            mqttc.publish(tpcpub, msgpub)
            print("published")
            
        
    def RadioButtonSub_On(self):
        radiobuttonsu = self.sender()
        tpcsub = self.lineSubsTopic.text()
        if radiobuttonsu.isChecked():
            if(tpcsub == ""):
                self.radioButtonSub.setChecked(False)
                self.checkSubTopic()
                print("THTH")
                RB = 0
            else:
                RB = 1
                print("subcribed")
        else:
            RB = 0
            print("unsubcribed")
            

        global radiobutton; radiobutton = RB

    
        

    def refresh(self):
        ttext = self.plainTextSubs.toPlainText()
        self.plainTextSubs.setPlainText(msgsub)
            
    def subTopicChanged(self):
        tpcsub = self.lineSubsTopic.text()
        global topicsubs; topicsubs = tpcsub
        if(tpcsub == ""):
            print("null")
            
        else:
            mqttc.subscribe(topicsubs)
            
        print(topicsubs)
              
        
    def update_sub(self):
        if (radiobutton == 1):
            self.plainTextSubs.appendPlainText(msgsub)
            print("show message")
        

    def checkPubTopic(self):
        ret = QMessageBox.warning(self, "Application",
                "Please, fill the topic publish!!!",
                QMessageBox.Ok)
    
        if ret == QMessageBox.Ok:
                return False

        return True

    def checkSubTopic(self):
        ret2 = QMessageBox.warning(self, "Application",
                "Please, fill the topic subcribe!!!",
                QMessageBox.Ok)
    
        if ret2 == QMessageBox.Ok:
                return False
            
        return True

    def checkBrokerPort(self):
        ret3 = QMessageBox.warning(self, "Application",
                "Please, fill the Broker and Port!!!",
                QMessageBox.Ok)
    
        if ret3 == QMessageBox.Ok:
                return False
            
        return True
            

if __name__ == '__main__':
  
    mqttc = MyMQTTClass()

    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow()

    main_window.show()

    sys.exit(app.exec_())

    

    
