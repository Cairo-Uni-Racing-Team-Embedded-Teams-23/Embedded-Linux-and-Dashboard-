######################################################################################
#   File name:       Dashboard.py
#   Authors:         - Abdelaziz Mohammad  
#                    - Ziad Tarek
#   Date:            6/10/2022
#   Organization:    Cairo University Racing Team - Formula Student
#   Description:     Python file for Dashboard GUI
######################################################################################

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from DataController import *

import sys , time , random
import pyqtgraph as pg


#Class for showing the logo of the team before showing the window
class SplashScreen(QtWidgets.QSplashScreen):
    def __init__(self):
        super(QtWidgets.QSplashScreen, self).__init__()

        #Read Team Logo
        pixMap = QtGui.QPixmap("images\logo.png")
        self.setPixmap(pixMap)

        #Show the Logo for 3 seconds 
        self.show()
        time.sleep(3)


#Class for Dashboard Window
class Dashboard(QtWidgets.QMainWindow):

    def __init__(self ): 
        super(Dashboard, self).__init__()
       
        #Load the ui file
        uic.loadUi("dashboard_colored.ui",self)

        #Dictionary for Holding Data
        self.__dataController = SingletonController()

        #Define Widgets
        self.__speedDialWidget = self.findChild(QtWidgets.QDial,"speedDial")
        self.__speedLabel = self.findChild(QtWidgets.QLabel,"speedLabel")

        self.__weightSlider  = self.findChild(QtWidgets.QSlider,"weightSlider")
        self.__heightSlider = self.findChild(QtWidgets.QSlider,"heightSlider")
        self.__weightLabel = self.findChild(QtWidgets.QLabel,"weightLabel")
        self.__heightLabel = self.findChild(QtWidgets.QLabel,"heightLabel")

        self.__voltLcd = self.findChild(QtWidgets.QLCDNumber,"voltageLCD")
        self.__currentLcd = self.findChild(QtWidgets.QLCDNumber,"currentLCD")
        self.__tempLcd = self.findChild(QtWidgets.QLCDNumber,"tempLCD")
        self.__voltLabel = self.findChild(QtWidgets.QLabel,"voltageLabel")
        self.__currentLabel = self.findChild(QtWidgets.QLabel,"currentLabel")
        self.__tempLabel = self.findChild(QtWidgets.QLabel,"tempLabel")
        self.__currentStateLabel = self.findChild(QtWidgets.QLabel,"currentStateLabel")


        self.__progressbar = self.findChild(QtWidgets.QProgressBar, "progressBar")
        self.__chargeLabel = self.findChild(QtWidgets.QLabel,"chargeLabel")
        self.__graphWidget = pg.PlotWidget()
        self.__timer = QtCore.QTimer()
        self.__frame = self.findChild(QtWidgets.QFrame, "frame")
        self.__stateLabel = self.findChild(QtWidgets.QLabel, "label")

        #Show Axes of Plot Widget
        #self.layout = QtWidgets.QVBoxLayout()
        #self.__frame.setLayout(self.layout)
        #self.layout.addWidget(self.__graphWidget)

        self.__button = self.findChild(QtWidgets.QPushButton,"pushButton")

        #Background color mode
        self.__whiteMode = self.findChild(QtWidgets.QAction,"actionWhite")
        self.__darkMode = self.findChild(QtWidgets.QAction,"actionDark")
        self.__formulaMode = self.findChild(QtWidgets.QAction,"actionFormula")       

        #Connect Functionality

        self.__whiteMode.triggered.connect(lambda: self.__changeMode("White"))
        self.__darkMode.triggered.connect(lambda: self.__changeMode("Dark"))
        self.__formulaMode.triggered.connect(lambda: self.__changeMode("Formula"))

        self.__x = list(range(100))
        self.__y = [random.randint(0, 100) for _ in range(100)]

        #self.__playlistProgress()
        #self.__timerHandle()
        self.__plot(self.__x, self.__y, "Sensor1", 'r')

        #Show Notches
        self.__speedDialWidget.setNotchesVisible(True)

        #Set Min and Max Values for Dial Widget
        self.__speedDialWidget.setRange(0,300)

        #Set Min and Max Values for weight slider 
        self.__weightSlider.setRange(0,300)

        #Set Min and Max Values for height slider 
        self.__heightSlider.setRange(0,300)    
        
        #Start the scheduler 
        self.__scheduler_ms(20)

        #Show Widget
        self.show()

    #Custom plot function to plot the graph with customized options    
    def __plot(self, x, y, plotname, color):
        self.__graphWidget.setBackground('w')
        pen = pg.mkPen(color=color, width=2, style=QtCore.Qt.DotLine)
        self.__graphWidget.setTitle(plotname, color="b", size="20pt")
        styles = {'color': 'r', 'font-size': '14px'}
        self.__graphWidget.setLabel('left', 'Temperature (°C)', **styles)
        self.__graphWidget.setLabel('bottom', 'Hour (H)', **styles)
        self.__graphWidget.showGrid(x=True, y=True)
        self.data_line = self.__graphWidget.plot(x, y, name=plotname, pen=pen)

    def __updatePlotData(self):
        self.__x = self.__x[1:]  # Remove the first y element.
        self.__x.append(self.__x[-1] + 1)  # Add a new value 1 higher than the last.

        self.__y = self.__y[1:]  # Remove the first
        self.__y.append(random.randint(0, 100))  # Add a new random value.

        self.data_line.setData(self.__x, self.__y)  # Update the data.

    def __timerHandle(self):
        self.__timer.timeout.connect(self.__updatePlotData)
        self.__timer.start(1000)
    
    #Function to behave as a scheduler to check the values every 10ms
    def __scheduler_ms(self, time ):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(20) #20ms
        self.timer.timeout.connect(self.__readData)
        self.timer.start(time)
                                 
    #Function to behave as a task for the scheduler to be called every 10ms
    def __readData(self):
        
        #Read All values from the controller
        speed = self.__dataController.getSpeed()
        volt =  self.__dataController.getVolt()
        current = self.__dataController.getCurrent()
        temp =   self.__dataController.getTemp()
        weight = self.__dataController.getWeight()
        height = self.__dataController.getHeight()
        state = self.__dataController.getState()

        #Update the GUI widgets with new values
        self.__speedDialWidget.setValue(speed)
        self.__speedLabel.setText(f'Speed {str(speed)} Km/h')
        self.__voltLcd.display(volt)
        self.__currentLcd.display(current)
        self.__tempLcd.display(temp)
        self.__weightSlider.setValue(weight)
        self.__heightSlider.setValue(height)
        self.__weightLabel.setText(f'Weight {str(weight)}kg')
        self.__heightLabel.setText(f'Height {str(height)}m')  
        self.__stateLabel.setText(state) ###
        self.__progressbar.setValue(random.randint(0, 100))


    #Function to change background color
    def __changeMode(self, mode):

        #Check for white mode
        if mode == "White":
            self.__voltLabel.setStyleSheet("QLabel {color:black;}")
            self.__currentLabel.setStyleSheet("QLabel {color:black;}")
            self.__tempLabel.setStyleSheet("QLabel {color:black;}") 
            self.__speedLabel.setStyleSheet("QLabel {color:black;}") 
            self.__weightLabel.setStyleSheet("QLabel {color:black;}")
            self.__heightLabel.setStyleSheet("QLabel {color:black;}")
            self.__chargeLabel.setStyleSheet("QLabel {color:black;}")
            self.__currentStateLabel.setStyleSheet("QLabel {color:black;}")
            self.__stateLabel.setStyleSheet("QLabel {color:black;}")


            self.__speedDialWidget.setStyleSheet("QProgressBar {color:white;}")

            self.__voltLcd.setStyleSheet("QLCDNumber {color:red;}")
            self.__currentLcd.setStyleSheet("QLCDNumber {color:red;}")
            self.__tempLcd.setStyleSheet("QLCDNumber {color:red;}") 

            self.setStyleSheet("background-color: white;")

        #Check for dark mode    
        elif mode == "Dark":
            self.__voltLabel.setStyleSheet("QLabel {color:red;}")
            self.__currentLabel.setStyleSheet("QLabel {color:red;}")
            self.__tempLabel.setStyleSheet("QLabel {color:red;}") 
            self.__speedLabel.setStyleSheet("QLabel {color:red;}") 
            self.__weightLabel.setStyleSheet("QLabel {color:red;}")
            self.__heightLabel.setStyleSheet("QLabel {color:red;}")
            self.__chargeLabel.setStyleSheet("QLabel {color:red;}")
            self.__currentStateLabel.setStyleSheet("QLabel {color:red;}")
            self.__stateLabel.setStyleSheet("QLabel {color:red;}")



            self.__voltLcd.setStyleSheet("QLCDNumber {color:red;}")
            self.__currentLcd.setStyleSheet("QLCDNumber {color:red;}")
            self.__tempLcd.setStyleSheet("QLCDNumber {color:red;}")  

            self.setStyleSheet("background-color: black;")

            self.__speedDialWidget.setStyleSheet("QProgressBar {color:white;}")

        #Check for Formula mode
        else:
            self.__voltLabel.setStyleSheet("QLabel {color: rgb(255,255,255);}")
            self.__currentLabel.setStyleSheet("QLabel {color:rgb(255,255,255);}")
            self.__tempLabel.setStyleSheet("QLabel {color:rgb(255,255,255);}") 
            self.__speedLabel.setStyleSheet("QLabel {color:rgb(255,255,255);}") 
            self.__weightLabel.setStyleSheet("QLabel {color:rgb(255,255,255);}")
            self.__heightLabel.setStyleSheet("QLabel {color:rgb(255,255,255);}")
            self.__chargeLabel.setStyleSheet("QLabel {color:rgb(255,255,255);}")
            self.__currentStateLabel.setStyleSheet("QLabel {color:rgb(255,255,255);}")
            self.__stateLabel.setStyleSheet("QLabel {color:rgb(255,255,255);}")

            self.__voltLcd.setStyleSheet("QLCDNumber {color:rgb(255,255,255);}")
            self.__currentLcd.setStyleSheet("QLCDNumber {color:rgb(255,255,255);}")
            self.__tempLcd.setStyleSheet("QLCDNumber {color:rgb(255,255,255);}")  

            self.setStyleSheet("background-color: red;")    

            self.__speedDialWidget.setStyleSheet("QProgressBar {color:white;}")

#Init the App
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    #Display SplashScreen First , after it is finished Display the Window  
    splash = SplashScreen()  
    UIWindow = Dashboard()

    UIWindow.setWindowTitle("Dashboard Team")
    UIWindow.setWindowIcon(QtGui.QIcon('images\logo.png'))
    #UIWindow.showMaximized()   
    splash.finish(UIWindow) 

    #app.processEvents()
      
    app.exec_()          