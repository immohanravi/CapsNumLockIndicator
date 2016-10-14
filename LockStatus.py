# Author: Mohan Ravi
# Vesrion: 1.0
# Dependencies: PyQt5, Xlib, Python3.5
# Description: Caps and Num lock indicator using python
# License: GPL Version 3 https://www.gnu.org/licenses/gpl-3.0.txt

import subprocess
def getCapsLockStaus():
    capsOn = subprocess.Popen('xset -q | grep Caps | awk \'{print $4}\'', stdout=subprocess.PIPE, shell=True)
    caps = str(capsOn.stdout.read())[2:-3]
    return caps



def getNumLockStaus():
    numOn = subprocess.Popen('xset -q | grep Caps | awk \'{print $8}\'', stdout=subprocess.PIPE, shell=True)
    num = str(numOn.stdout.read())[2:-3]
    return num


