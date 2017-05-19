"""
Script for controlling raspberry pi motor driver

Tested on seeedstudios' motor driver board
http://wiki.seeed.cc/Raspberry_Pi_Motor_Driver_Board_v1.0/
"""

import sys
from time import sleep
from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QAction
from gpiozero import DigitalOutputDevice, PWMOutputDevice, OutputDeviceBadValue

def abs(val):
    if val >= 0:
        return val
    else:
        return -val

def clamp(val):
    if val >= 1.0:
        return 1
    if val <= -1.0:
        return 1
    else:
        return abs(val)

class Motor:
    """Controll a singel motor"""

    def __init__(self, forward, backward, pwm):
        self.forward = DigitalOutputDevice(forward)
        self.backward = DigitalOutputDevice(backward)
        self.pwm = PWMOutputDevice(pwm, True, 0, 1000)

    def speed(self, speed):
        """Modify the speed and direction of the motor"""

        self.direction(speed)
        self.pwm.value = clamp(speed)

    def direction(self, speed):
        """Set the direction of the motor based on the speed"""

        if speed > 0:
            self.forward.on()
            self.backward.off()
        else:
            self.forward.off()
            self.backward.on()

    def close(self):
        """Call to release all resources"""

        self.forward.close()
        self.backward.close()
        self.pwm.close()



class MotorDriver:
    """Represents the motor driver board"""

    def __init__(self):
        self.motora = Motor(23, 24, 25)
        self.motorb = Motor(17, 27, 22)

        self.speeda = 0
        self.speedb = 0

    def speed(self, speeda, speedb):
        """Modify speed and direction of all motors by passing deltas"""

        self.speeda += speeda
        self.speedb += speedb

        self.motora.speed(self.speeda)
        self.motorb.speed(self.speedb)

    def close(self):
        """Release all resources"""

        self.motora.close()
        self.motorb.close()

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.driver = MotorDriver()
        self.delta_speed = 0.05

        self.slider = QSlider(self)
        self.slider.move(50, 50)
        self.slider.resize(50, 500)

        f = QAction(self)
        f.setShortcut("W")
        f.triggered.connect(self.forward)

        b = QAction(self)
        b.setShortcut("S")
        b.triggered.connect(self.backward)

        r = QAction(self)
        r.setShortcut("D")
        r.triggered.connect(self.right)

        l = QAction(self)
        l.setShortcut("A")
        l.triggered.connect(self.left)

        self.slider.addAction(f)
        self.slider.addAction(b)
        self.slider.addAction(r)
        self.slider.addAction(l)

        self.resize(1080, 720)
        self.setWindowTitle("Motor controller")
        self.show()

    def forward(self):
        self.driver.speed(self.delta_speed, self.delta_speed)

    def backward(self):
        self.driver.speed(-self.delta_speed, -self.delta_speed)

    def right(self):
        self.driver.speed(self.delta_speed, -self.delta_speed)

    def left(self):
        self.driver.speed(-self.delta_speed, self.delta_speed)

    def close(self):
        self.driver.close()

# TODO: Tidy this up
app = QApplication(sys.argv)
w = Window()
e = app.exec_()
w.close()
exit(e)
