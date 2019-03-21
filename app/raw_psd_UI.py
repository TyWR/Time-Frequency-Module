# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'raw_psd-ui.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RawPSDWindow(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(792, 605)
        Dialog.setMinimumSize(QtCore.QSize(400, 300))
        Dialog.setMaximumSize(QtCore.QSize(1080, 1720))
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.figureLayout = QtWidgets.QVBoxLayout()
        self.figureLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.figureLayout.setObjectName("figureLayout")
        self.verticalLayout_3.addLayout(self.figureLayout)
        self.line_2 = QtWidgets.QFrame(Dialog)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_3.addWidget(self.line_2)
        self.lowerWindowLayout = QtWidgets.QVBoxLayout()
        self.lowerWindowLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.lowerWindowLayout.setObjectName("lowerWindowLayout")
        self.selectPlotLayout = QtWidgets.QVBoxLayout()
        self.selectPlotLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.selectPlotLayout.setObjectName("selectPlotLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.selectPlotLabel = QtWidgets.QLabel(Dialog)
        self.selectPlotLabel.setObjectName("selectPlotLabel")
        self.horizontalLayout.addWidget(self.selectPlotLabel)
        self.selectPlotType = QtWidgets.QComboBox(Dialog)
        self.selectPlotType.setObjectName("selectPlotType")
        self.horizontalLayout.addWidget(self.selectPlotType)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)
        self.selectPlotLayout.addLayout(self.horizontalLayout)
        self.lowerWindowLayout.addLayout(self.selectPlotLayout)
        self.Separator = QtWidgets.QFrame(Dialog)
        self.Separator.setFrameShape(QtWidgets.QFrame.HLine)
        self.Separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Separator.setObjectName("Separator")
        self.lowerWindowLayout.addWidget(self.Separator)
        self.ParametersLayout = QtWidgets.QHBoxLayout()
        self.ParametersLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.ParametersLayout.setObjectName("ParametersLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frequencyLabel = QtWidgets.QLabel(Dialog)
        self.frequencyLabel.setObjectName("frequencyLabel")
        self.horizontalLayout_2.addWidget(self.frequencyLabel)
        self.fmin = QtWidgets.QLineEdit(Dialog)
        self.fmin.setObjectName("fmin")
        self.horizontalLayout_2.addWidget(self.fmin)
        self.fmax = QtWidgets.QLineEdit(Dialog)
        self.fmax.setObjectName("fmax")
        self.horizontalLayout_2.addWidget(self.fmax)
        self.horizontalLayout_2.setStretch(0, 2)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.vmaxLabel = QtWidgets.QLabel(Dialog)
        self.vmaxLabel.setObjectName("vmaxLabel")
        self.horizontalLayout_3.addWidget(self.vmaxLabel)
        self.vmax = QtWidgets.QLineEdit(Dialog)
        self.vmax.setObjectName("vmax")
        self.horizontalLayout_3.addWidget(self.vmax)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.ParametersLayout.addLayout(self.verticalLayout)
        self.ParametersLayout.setStretch(0, 1)
        self.lowerWindowLayout.addLayout(self.ParametersLayout)
        self.lowerWindowLayout.setStretch(0, 1)
        self.lowerWindowLayout.setStretch(1, 1)
        self.lowerWindowLayout.setStretch(2, 2)
        self.verticalLayout_3.addLayout(self.lowerWindowLayout)
        self.line_3 = QtWidgets.QFrame(Dialog)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_3.addWidget(self.line_3)
        self.recapLabel = QtWidgets.QLabel(Dialog)
        self.recapLabel.setMinimumSize(QtCore.QSize(300, 25))
        self.recapLabel.setMaximumSize(QtCore.QSize(16777215, 25))
        self.recapLabel.setText("")
        self.recapLabel.setObjectName("recapLabel")
        self.verticalLayout_3.addWidget(self.recapLabel)
        self.verticalLayout_3.setStretch(0, 15)
        self.verticalLayout_3.setStretch(1, 1)
        self.verticalLayout_3.setStretch(2, 1)
        self.verticalLayout_3.setStretch(3, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "PSD Visualizer"))
        self.selectPlotLabel.setText(_translate("Dialog", "Select Plot Type  "))
        self.frequencyLabel.setText(_translate("Dialog", "Frequency Range Display (min - max)"))
        self.vmaxLabel.setText(_translate("Dialog", "Scaling "))