# Author: Mohan Ravi
# Vesrion: 1.0
# Dependencies: PyQt5, Xlib, Python3.5
# Description: Caps and Num lock indicator using python
# License: GPL Version 3 https://www.gnu.org/licenses/gpl-3.0.txt

import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QAction
from Xlib.display import Display
from Xlib import X
from Xlib.ext import record
from Xlib.protocol import rq
import LockStatus
import about

#Variables for Global Shortcut events
disp = None
disp = Display()
root = disp.screen().root

#Gets present lock status from LockStatus module
caps = LockStatus.getCapsLockStaus()
num = LockStatus.getNumLockStaus()
ButtonClicked = 60

#Creates System Tray Icon using PyQt5 lib
class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super(SystemTrayIcon, self).__init__(icon, parent)
        menu = QtWidgets.QMenu(parent)
        exitAction = QAction("Exit",self)
        exitAction.setIcon(QtGui.QIcon('images/exit.png'))
        exitAction.triggered.connect(parent.close)
        aboutAction = QAction("About",self)
        aboutAction.setIcon(QtGui.QIcon('images/about.png'))
        menu.addAction(exitAction)
        menu.addAction(aboutAction)
        self.about = aboutPage()
        aboutAction.triggered.connect(self.about.dis)
        self.setContextMenu(menu)

#Object of file About.py which holds the code for about page user interface
class aboutPage(QtWidgets.QWidget,about.Ui_MainWindow):
    def __init__(self, parent=None):
        super(aboutPage,self).__init__(parent)
        self.setupUi(self)
    def dis(self):
        self.show()

#Main Application Window which contains Tray Icons
class windows(QtWidgets.QWidget):
    def __init__(self):
        super(windows, self).__init__()
        self.gsThread = GlobalShortCutThread()
        self.gsThread.start()
        self.gsThread.eventCapture.connect(self.changeIcon)

        if caps == "on":
            self.capIcon = SystemTrayIcon(QtGui.QIcon('images/capsON.png'),self)
            self.capIcon.show()
            self.capsCount = 1
            self.capIcon.setToolTip("Caps Lock On")
        elif caps == "off":
            self.capIcon = SystemTrayIcon(QtGui.QIcon('images/capsOFF.png'), self)
            self.capIcon.show()
            self.capsCount = 2
            self.capIcon.setToolTip("Caps Lock Off")

        if num == "on":
            self.numIcon = SystemTrayIcon(QtGui.QIcon('images/numON.png'),self)
            self.numIcon.show()
            self.numCount = 1
            self.numIcon.setToolTip("num Lock On")

        elif num == "off":
            self.numIcon = SystemTrayIcon(QtGui.QIcon('images/numOFF.png'), self)
            self.numIcon.show()
            self.numCount = 2
            self.numIcon.setToolTip("num Lock Off")

    def changeIcon(self):
        if ButtonClicked == 66:
            self.capsCount += 1
            if self.capsCount%2 == 0:
                self.capIcon.setIcon(QtGui.QIcon('images/capsOFF.png'))
                self.capIcon.setToolTip("Caps Lock Off")

            else:
                self.capIcon.setIcon(QtGui.QIcon('images/capsON.png'))
                self.capIcon.setToolTip("Caps Lock On")

        elif ButtonClicked == 77:
            self.numCount += 1
            if self.numCount%2 == 0:
                self.numIcon.setIcon(QtGui.QIcon('images/numOFF.png'))
                self.numIcon.setToolTip("num Lock Off")
            else:
                self.numIcon.setIcon(QtGui.QIcon('images/numON.png'))
                self.numIcon.setToolTip("num Lock On")

# The most important class in this projects which enables
# and receives button press events even when not in focus
class GlobalShortCutThread(QtCore.QThread):
    eventCapture = pyqtSignal()
    def run(self):
        class handle():
            def handler(reply):
                """ This function is called when a xlib event is fired """
                data = reply.data
                while len(data):
                    event, data = rq.EventField(None).parse_binary_value(data, disp.display, None, None)
                    # KEYCODE IS FOUND USERING event.detail
                    global ButtonClicked
                    ButtonClicked = int(event.detail)
                    if event.type == X.KeyPress:
                        if (event.detail == 66) or (event.detail == 77) :
                            self.eventCapture.emit()
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
# Initial Code
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = windows()
    window.setWindowTitle("CapsNumLockIndicator")
    sys.exit(app.exec_())



