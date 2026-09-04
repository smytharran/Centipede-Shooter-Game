'''
In this example, when the circuit playground is tilted left (x < -3)
the left arrow key is pressed.
The key is only released when x is not < 3.
Notice that key codes are different in pygame as in circuitpython!
Code written by Laura Maye.
'''

import usb_hid
import time
from adafruit_circuitplayground import cp
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from sensorlightdisplay import SensorLightDisplay
kbd = Keyboard(usb_hid.devices)

flipped_x = 0
acceleration_peak = 9.81
brightPurple = [128, 0, 191]
pureBlue = [0, 0, 255]

sldisp = SensorLightDisplay(0.1)


while True:
    x = cp.acceleration[0]

    if x < 0:
        flipped_x = x * -1
    else:
        flipped_x = x

    if flipped_x <= acceleration_peak:
        # problem 1: if x < - 3, press left arrow
        if x < - 3:
            kbd.press(Keycode.LEFT_ARROW) # used to press AND NOT RELEASE a key on the keyboard
        else:
            kbd.release(Keycode.LEFT_ARROW)
        if x >  3:
            kbd.press(Keycode.RIGHT_ARROW) # used to press AND NOT RELEASE a key on the keyboard
        else:
            kbd.release(Keycode.RIGHT_ARROW)

    if cp.button_a:
        kbd.press(Keycode.SPACE)
        kbd.release(Keycode.SPACE)

    if cp.button_b:
        kbd.press(Keycode.Z)
        kbd.release(Keycode.Z)

    x = cp.acceleration[0] # retrieve the x acceleration value
    y = cp.acceleration[1] # retrieve the y acceleration value
    acceleration_values = [x,y]
    #sldisp.control_feedback_x(x, brightPurple)
    sldisp.advanced_control_feedback(x)

    time.sleep(0.1)
