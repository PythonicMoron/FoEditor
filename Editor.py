"""
Save editor for Fall of Eden.

Currently, it isn't much more than a basic character editor, but overtime it will gain other features.

In order to run this python script, PyQt5 needs to be installed.
Also requires the package dpath, which can be obtained from PyPI.

Written and tested using Python 3.5.0 and PyQt 5.6.0.
"""

from sys import exit, argv
from FoEditor.main import Main, log
from PyQt5.QtWidgets import QMainWindow, QApplication

ADVANCED_LOGGING = False


class MainApp(QMainWindow, Main):  # Main window class sets up ui.

    # All function definitions can be found in FoEditor.Main.

    def __init__(self):  # initialize
        # Configure logger
        if ADVANCED_LOGGING:
            fmt = '%(levelname)s (%(module)s.%(funcName)s): %(message)s'
        else:
            fmt = '%(levelname)s: %(message)s'
        log.basicConfig(filename='Editor.log', filemode='w+', format=fmt, level=log.DEBUG)

        log.info("Logging started. Advanced mode = " + str(ADVANCED_LOGGING))
        log.info("Initializing...")

        QMainWindow.__init__(self)
        log.info("QMainWindow initialized.")

        self.setupUi(self)  # initializes generated ui file (UI_MainWindow)
        log.debug("Executed generated ui class.")

        self.initUI(ADVANCED_LOGGING)  # Large class found in main.Main.
        log.info("UI setup.")
        log.info("Initialized.")

if 'alog' in argv:
    ADVANCED_LOGGING = True

app = QApplication(argv)
window = MainApp()
window.show()
exit(app.exec_())
