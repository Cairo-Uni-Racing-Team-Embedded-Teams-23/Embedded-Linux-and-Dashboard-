import random
class absclass :
    speed = 0
    volt = 0

    @property
    def speed (self):
        return absclass.speed
    @property
    def volt(self):
        return absclass.volt

    @speed.setter
    def speed(self,value):
        absclass.speed=value
    @volt.setter
    def volt(self, value):
        absclass.volt = value

    @speed.deleter
    def speed(self):
        absclass.speed = None
    @volt.deleter
    def volt(self):
        absclass.volt = None
        
###emulation of how data will be setted from terminal
class setter_class:
    def __init__(self):
        absclass.speed = random.randint(0,300)
        absclass.volt = random.randint(0,300)
##emulation of how gui will get data
class getter_class_gui:
    def __init__(self):
        self.speed=absclass.speed
        self.volt=absclass.volt
    def print_speed(self):
        print("speed {}\n".format(self.speed))
    def print_volt(self):
        print("volt {}\n".format(self.volt))

a=setter_class()
b=getter_class_gui()
b.print_speed()
b.print_volt()


