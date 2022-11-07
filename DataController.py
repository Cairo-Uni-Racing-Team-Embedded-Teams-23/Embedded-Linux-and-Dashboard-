######################################################################################
#   File name:       DataController.py
#   Authors:         - Abdelaziz Mohammad  
#                    - Ziad Tarek
#   Date:            7/10/2022
#   Organization:    Cairo University Racing Team - Formula Student
#   Description:     Python file controlling data displayed in GUI
######################################################################################

import random , sys
from PyQt5 import QtCore , QtWidgets


#Class for controlling Data displayed in gUI
class SingletonController:

    #Variable to Track Instantions of singleton class
    __instance = None

    #Function to be called before init function returning same object every instantiation
    def __new__(cls):

        if cls.__instance is None:
            cls.__instance = super(SingletonController,cls).__new__(cls)   

            #Dictionary for Holding Data
            cls.__Data = {

                        'volt' : 12 ,
                        'current': 1,
                        'temp' : 25,
                        'state' : 'poweron',
                        'speed': 112,
                        'weight': 60 ,
                        'height': 120,
                        'charge': 35

                   }


  

        return cls.__instance               

    def __init__(self):
        #Scheduler for writing new random values every 1 second ( Testing ) 
        self.timer2 = QtCore.QTimer()
        self.timer2.timeout.connect( self.__writeData)
        self.timer2.start(1000)

    #Function to set volt value
    def setVolt(self,volt):
        self.__Data["volt"] = volt  

    #Function to set current value
    def setCurrent(self,current):
        self.__Data["current"] = current  
        
    #Function to set temp value
    def setTemp(cls,temp):
        cls.__Data["temp"] = temp                                

    #Function to set speed value
    def setSpeed(self,speed):
        self.__Data["speed"] = speed 

    #Function to set weight value
    def setWeight(self,weight):
        self.__Data["weight"] = weight   

    #Function to set height value
    def setHeight(self,height):
        self.__Data["height"] = height   

    #Function to read volt value
    def getVolt(self):
        return self.__Data["volt"]   

    #Function to read current value
    def getCurrent(self):
        return self.__Data["current"]     

    #Function to read temp value
    def getTemp(self):
        return self.__Data["temp"]  

    #Function to read speed value
    def getSpeed(self):
        return self.__Data["speed"]  

    #Function to read weight value
    def getWeight(self):
        return self.__Data["weight"] 

    #Function to read height value
    def getHeight(self):
        return self.__Data["height"] 

    #Function to read state value
    def getState(self):
        return self.__Data["state"]  

    #Function for printing the values
    def printAll(self):
        print(self.__Data)

    #Function for writing values
    def __writeData(self):

        self.setTemp(random.randint(0,100))    
        self.setHeight(random.randint(0,100))
        self.setSpeed(random.randint(0,100))
        self.setCurrent(random.randint(0,100))   
        self.setVolt(random.randint(0,100))   
        self.setWeight(random.randint(0,100))
    

app = QtWidgets.QApplication(sys.argv)
dataController = SingletonController()


