import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QAction
from Xlib.display import Display
from Xlib import X
from Xlib.ext import record
from Xlib.protocol import rq
import LockStatus

#Variables for Global Shortcut events
disp = None
disp = Display()
root = disp.screen().root

#Gets present lock status from LockStatus module
caps = LockStatus.getCapsLockStaus()
num = LockStatus.getNumLockStaus()
ButtonClicked = 60


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
        aboutAction.triggered.connect(self.about)
        self.setContextMenu(menu)

    def about(self):
        self.aboutWindow = QtWidgets.QWidget()

        self.aboutWindow.show()

class windows(QtWidgets.QWidget):
    def __init__(self):
        super(windows, self).__init__()
        self.gsThread = GlobalShortCutThread()
        self.gsThread.start()
        self.gsThread.eventCapture.connect(self.changeIcon)

        if caps == "on":
            self.capIcon = SystemTrayIcon(QtGui.QIcon('images/capsOn.png'),self)
            self.capIcon.show()
            self.capsCount = 1
            self.capIcon.setToolTip("Caps Lock On")
        elif caps == "off":
            self.capIcon = SystemTrayIcon(QtGui.QIcon('images/capsOff.png'), self)
            self.capIcon.show()
            self.capsCount = 2
            self.capIcon.setToolTip("Caps Lock Off")

        if num == "on":
            self.numIcon = SystemTrayIcon(QtGui.QIcon('images/numOn.png'),self)
            self.numIcon.show()
            self.numCount = 1
            self.numIcon.setToolTip("num Lock On")

        elif num == "off":
            self.numIcon = SystemTrayIcon(QtGui.QIcon('images/numOff.png'), self)
            self.numIcon.show()
            self.numCount = 2
            self.numIcon.setToolTip("num Lock Off")

    def changeIcon(self):
        if ButtonClicked == 66:
            self.capsCount += 1
            if self.capsCount%2 == 0:
                self.capIcon.setIcon(QtGui.QIcon('images/capsOff.png'))
                self.capIcon.setToolTip("Caps Lock Off")

            else:
                self.capIcon.setIcon(QtGui.QIcon('images/capsOn.png'))
                self.capIcon.setToolTip("Caps Lock On")

        elif ButtonClicked == 77:
            self.numCount += 1
            if self.numCount%2 == 0:
                self.numIcon.setIcon(QtGui.QIcon('images/numOff.png'))
                self.numIcon.setToolTip("num Lock Off")
            else:
                self.numIcon.setIcon(QtGui.QIcon('images/numOn.png'))
                self.numIcon.setToolTip("num Lock On")


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

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = windows()
    window.setWindowTitle("CapsNumLockIndicator")
    sys.exit(app.exec_())



