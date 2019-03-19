from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from app.cut_UI import Ui_CutWindow

class CutWindow(QDialog) :
    def __init__(self, parent = None) :
        super(CutWindow, self).__init__(parent)
        self.ui = Ui_CutWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
