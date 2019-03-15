# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'psd-ui.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PSDWindow(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1318, 764)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 1301, 571))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

        self.figureLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.figureLayout.setContentsMargins(0, 0, 0, 0)
        self.figureLayout.setObjectName("figureLayout")

        self.selectPlotLabel = QtWidgets.QLabel(Dialog)
        self.selectPlotLabel.setGeometry(QtCore.QRect(10, 590, 271, 51))
        self.selectPlotLabel.setObjectName("selectPlotLabel")

        self.selectPlotType = QtWidgets.QComboBox(Dialog)
        self.selectPlotType.setGeometry(QtCore.QRect(310, 600, 1001, 25))
        self.selectPlotType.setObjectName("selectPlotType")
        self.selectPlotType.addItem("PSD Matrix")
        self.selectPlotType.addItem("Topomap")


        self.line = QtWidgets.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(0, 640, 1331, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.frequencyLabel = QtWidgets.QLabel(Dialog)
        self.frequencyLabel.setGeometry(QtCore.QRect(10, 660, 261, 51))
        self.frequencyLabel.setObjectName("frequencyLabel")

        self.fmin = QtWidgets.QLineEdit(Dialog)
        self.fmin.setGeometry(QtCore.QRect(310, 670, 121, 25))
        self.fmin.setObjectName("fmin")
        self.fmin.setValidator(QtGui.QDoubleValidator())
        self.fmin.setMaxLength(4)


        self.fmax = QtWidgets.QLineEdit(Dialog)
        self.fmax.setGeometry(QtCore.QRect(450, 670, 121, 25))
        self.fmax.setObjectName("fmax")
        self.fmax.setValidator(QtGui.QDoubleValidator())
        self.fmax.setMaxLength(4)


        self.vmaxLabel = QtWidgets.QLabel(Dialog)
        self.vmaxLabel.setGeometry(QtCore.QRect(10, 710, 261, 51))
        self.vmaxLabel.setObjectName("vmaxLabel")

        self.vmax = QtWidgets.QLineEdit(Dialog)
        self.vmax.setGeometry(QtCore.QRect(310, 720, 261, 25))
        self.vmax.setObjectName("vmax")
        self.vmax.setValidator(QtGui.QDoubleValidator())
        self.vmax.setMaxLength(15)
        self.vmax.setText("3e-12")

        self.line_2 = QtWidgets.QFrame(Dialog)
        self.line_2.setGeometry(QtCore.QRect(643, 650, 20, 131))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")

        self.displayLabel = QtWidgets.QLabel(Dialog)
        self.displayLabel.setGeometry(QtCore.QRect(660, 660, 101, 51))
        self.displayLabel.setObjectName("displayLabel")
        self.epochsLabel = QtWidgets.QLabel(Dialog)
        self.epochsLabel.setGeometry(QtCore.QRect(660, 710, 101, 51))
        self.epochsLabel.setObjectName("epochsLabel")

        self.epochsSlider = QtWidgets.QSlider(Dialog)
        self.epochsSlider.setGeometry(QtCore.QRect(740, 710, 571, 51))
        self.epochsSlider.setOrientation(QtCore.Qt.Horizontal)
        self.epochsSlider.setObjectName("epochsSlider")
        self.epochsSlider.setMinimum(0)
        self.epochsSlider.setValue(0)
        self.epochsSlider.setTickInterval(1)

        self.showSingleEpoch = QtWidgets.QCheckBox(Dialog)
        self.showSingleEpoch.setGeometry(QtCore.QRect(740, 660, 161, 51))
        self.showSingleEpoch.setObjectName("showSingleEpoch")

        self.showMean = QtWidgets.QCheckBox(Dialog)
        self.showMean.setGeometry(QtCore.QRect(910, 660, 161, 51))
        self.showMean.setObjectName("showMean")
        self.showMean.setCheckState(2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.selectPlotLabel.setText(_translate("Dialog", "Select Plot Type  "))
        self.frequencyLabel.setText(_translate("Dialog", "Frequency Range Display (min - max)"))
        self.vmaxLabel.setText(_translate("Dialog", "Scaling "))
        self.displayLabel.setText(_translate("Dialog", "Display"))
        self.epochsLabel.setText(_translate("Dialog", "Epoch"))
        self.showSingleEpoch.setText(_translate("Dialog", "Single Epoch"))
        self.showMean.setText(_translate("Dialog", "Average over Epochs"))
