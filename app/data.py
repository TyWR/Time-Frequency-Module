from PyQt5.QtWidgets import QDialog, QFileDialog, QVBoxLayout, QPushButton
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class ImportDataWindow(QDialog) :

    #---------------------------------------------------------------------
    def __init__(self, parent=None):
        super(ImportDataWindow, self).__init__(parent)

        # Pick path button
        self.pickPathButton = QPushButton("Choose path")
        self.pickPathButton.clicked.connect(self.pick_path)

        layout = QVBoxLayout()
        layout.addWidget(self.pickPathButton)
        self.setLayout(layout)

    #---------------------------------------------------------------------
    def pick_path(self) :
         self.fname = QFileDialog().getOpenFileName(self, 'Open file', 'c:\\', "EEG File (*sef)")
