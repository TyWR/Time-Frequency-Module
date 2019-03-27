# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'avg_epochs_tfr.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AvgTFRWindow(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1192, 762)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.matplotlibLayout = QtWidgets.QVBoxLayout()
        self.matplotlibLayout.setObjectName("matplotlibLayout")
        self.verticalLayout_2.addLayout(self.matplotlibLayout)
        self.bottomLayout = QtWidgets.QVBoxLayout()
        self.bottomLayout.setObjectName("bottomLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(15)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.Display = QtWidgets.QLabel(Dialog)
        self.Display.setMinimumSize(QtCore.QSize(130, 25))
        self.Display.setMaximumSize(QtCore.QSize(130, 25))
        self.Display.setObjectName("Display")
        self.horizontalLayout_3.addWidget(self.Display)
        self.displayBox = QtWidgets.QComboBox(Dialog)
        self.displayBox.setMinimumSize(QtCore.QSize(0, 25))
        self.displayBox.setMaximumSize(QtCore.QSize(16777215, 25))
        self.displayBox.setObjectName("displayBox")
        self.horizontalLayout_3.addWidget(self.displayBox)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setMinimumSize(QtCore.QSize(130, 25))
        self.label.setMaximumSize(QtCore.QSize(130, 25))
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_3.addWidget(self.lineEdit)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 2)
        self.horizontalLayout_3.setStretch(2, 1)
        self.horizontalLayout_3.setStretch(3, 2)
        self.bottomLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mainLabel = QtWidgets.QLabel(Dialog)
        self.mainLabel.setMinimumSize(QtCore.QSize(130, 25))
        self.mainLabel.setMaximumSize(QtCore.QSize(130, 25))
        self.mainLabel.setText("")
        self.mainLabel.setObjectName("mainLabel")
        self.horizontalLayout.addWidget(self.mainLabel)
        self.mainSlider = QtWidgets.QSlider(Dialog)
        self.mainSlider.setMinimumSize(QtCore.QSize(0, 25))
        self.mainSlider.setMaximumSize(QtCore.QSize(16777215, 25))
        self.mainSlider.setOrientation(QtCore.Qt.Horizontal)
        self.mainSlider.setObjectName("mainSlider")
        self.horizontalLayout.addWidget(self.mainSlider)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)
        self.bottomLayout.addLayout(self.horizontalLayout)
        self.bottomLayout.setStretch(0, 1)
        self.bottomLayout.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.bottomLayout)
        self.verticalLayout_2.setStretch(0, 5)
        self.verticalLayout_2.setStretch(1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.Display.setText(_translate("Dialog", "Display"))
        self.label.setText(_translate("Dialog", "Scaling"))
