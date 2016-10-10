import subprocess

def getCapsLockStaus():
    capsOn = subprocess.Popen('xset -q | grep Caps | awk \'{print $4}\'', stdout=subprocess.PIPE, shell=True)
    caps = str(capsOn.stdout.read())[2:-3]
    return caps



def getNumLockStaus():
    numOn = subprocess.Popen('xset -q | grep Caps | awk \'{print $8}\'', stdout=subprocess.PIPE, shell=True)
    num = str(numOn.stdout.read())[2:-3]
    return num