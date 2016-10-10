import threading
import time
import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
from Xlib.display import Display
from Xlib import X
from Xlib.ext import record
from Xlib.protocol import rq

from PyQt5 import QtWidgets, QtCore, QtGui

import LockStatus

disp = None
disp = Display()
root = disp.screen().root


caps = LockStatus.getCapsLockStaus()
num = LockStatus.getNumLockStaus()

button = 60

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        super(SystemTrayIcon, self).__init__(icon, parent)
        menu = QtWidgets.QMenu(parent)
        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(parent.close)
        self.setContextMenu(menu)

class windows(QtWidgets.QWidget):
    def __init__(self):
        super(windows, self).__init__()
        self.second = t2()
        self.second.start()
        self.second.send.connect(self.test)

        if caps == "on":
            self.capIcon = SystemTrayIcon(QtGui.QIcon('images/capsOn.png'),self)
            self.capIcon.show()
            self.capsCount = 1
        elif caps == "off":
            self.capIcon = SystemTrayIcon(QtGui.QIcon('images/capsOff.png'), self)
            self.capIcon.show()
            self.capsCount = 2

        if num == "on":
            self.numIcon = SystemTrayIcon(QtGui.QIcon('images/numOn.png'),self)
            self.numIcon.show()
            global numCount
            self.numCount = 1

        elif num == "off":
            self.numIcon = SystemTrayIcon(QtGui.QIcon('images/numOff.png'), self)
            self.numIcon.show()
            global numCount
            self.numCount = 2


    def test(self):
        if button == 66:
            self.capsCount += 1
            if self.capsCount%2 == 0:
                self.capIcon.setIcon(QtGui.QIcon('images/capsOff.png'))

            else:
                self.capIcon.setIcon(QtGui.QIcon('images/capsOn.png'))

        elif button == 77:
            self.numCount += 1
            if self.numCount%2 == 0:
                self.numIcon.setIcon(QtGui.QIcon('images/numOff.png'))
            else:
                self.numIcon.setIcon(QtGui.QIcon('images/numOn.png'))




class t1(threading.Thread):
    global window
    def run(self):
        app = QtWidgets.QApplication([])
        window = windows()
        window.setWindowTitle("t1")
        sys.exit(app.exec_())



class t2(QtCore.QThread):
    send = pyqtSignal()
    def run(self):

        class hand(QtCore.QThread):


            def handler(reply):
                """ This function is called when a xlib event is fired """
                data = reply.data
                while len(data):
                    event, data = rq.EventField(None).parse_binary_value(data, disp.display, None, None)
                    # KEYCODE IS FOUND USERING event.detail
                    global button
                    button = int(event.detail)

                    if event.type == X.KeyPress:
                        if (event.detail == 66) or (event.detail == 77) :
                            self.send.emit()
            # get current display
            # disp = Display()
            # root = disp.screen().root

            # Monitor keypress and button press
            ctx = disp.record_create_context(
                0,
                [record.AllClients],
                [{
                    'core_requests': (0, 0),
                    'core_replies': (0, 0),
                    'ext_requests': (0, 0, 0, 0),
                    'ext_replies': (0, 0, 0, 0),
                    'delivered_events': (0, 0),
                    'device_events': (X.KeyReleaseMask, X.ButtonReleaseMask),
                    'errors': (0, 0),
                    'client_started': False,
                    'client_died': False,
                }])

            disp.record_enable_context(ctx, handler)
            disp.record_free_context(ctx)

            while True:
                # Infinite wait, doesn't do anything as no events are grabbed
                event = root.display.next_event()




first = t1()
first.start()



