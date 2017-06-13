"""
Script for å kontrollere en raspberry pi motor driver

Designet og testet for seeedstudios' motor driver board
http://wiki.seeed.cc/Raspberry_Pi_Motor_Driver_Board_v1.0/
"""

import sys

from time import sleep
from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QAction
from gpiozero import DigitalOutputDevice, PWMOutputDevice, OutputDeviceBadValue

// Returner absolutt verdien av argumentet
def abs(val):
    if val >= 0:
        return val
    else:
        return -val

// Normaliser verdien av argumentet
def norm(val):
    if val >= 1.0:
        return 1
    if val <= -1.0:
        return 1
    else:
        return abs(val)

class Motor:
    """Klasse for å kontrollere en motor"""

    def __init__(self, forward, backward, pwm):
        // Disse er inn signalene til h-blokken
        self.forward = DigitalOutputDevice(forward)
        self.backward = DigitalOutputDevice(backward)
        self.pwm = PWMOutputDevice(pwm, True, 0, 1000)

    def speed(self, speed):
        """Justerer hastigheten og rettningen til motoren"""

        self.direction(speed)
        self.pwm.value = norm(speed)

    def direction(self, speed):
        """Bestemmer rettningen basert på hastigheten"""

        if speed > 0:
            self.forward.on()
            self.backward.off()
        else:
            self.forward.off()
            self.backward.on()

    def close(self):
        """Frigjør og rydder opp"""

        self.forward.close()
        self.backward.close()
        self.pwm.close()



class MotorDriver:
    """
    Representerer motor driver brettet.
    
    Holder styr på motorenes hastighet slik at vi ikke ødelegger dem. 
    """

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
    """
    Vinduet viser informasjon om motorene og styrer motor driver brettet.
    """

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
