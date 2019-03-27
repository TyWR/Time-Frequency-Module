# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'menu-ui.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MenuWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(542, 430)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.mainLayout.setObjectName("mainLayout")
        self.choosePathLayout = QtWidgets.QHBoxLayout()
        self.choosePathLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.choosePathLayout.setObjectName("choosePathLayout")
        self.pathButton = QtWidgets.QPushButton(self.centralwidget)
        self.pathButton.setMinimumSize(QtCore.QSize(130, 25))
        self.pathButton.setMaximumSize(QtCore.QSize(130, 25))
        self.pathButton.setObjectName("pathButton")
        self.choosePathLayout.addWidget(self.pathButton)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setMinimumSize(QtCore.QSize(300, 25))
        self.lineEdit.setMaximumSize(QtCore.QSize(16777215, 25))
        self.lineEdit.setObjectName("lineEdit")
        self.choosePathLayout.addWidget(self.lineEdit)
        self.chooseFileType = QtWidgets.QComboBox(self.centralwidget)
        self.chooseFileType.setMinimumSize(QtCore.QSize(80, 25))
        self.chooseFileType.setMaximumSize(QtCore.QSize(80, 25))
        self.chooseFileType.setObjectName("chooseFileType")
        self.choosePathLayout.addWidget(self.chooseFileType)
        self.choosePathLayout.setStretch(0, 1)
        self.mainLayout.addLayout(self.choosePathLayout)
        self.dataLayout = QtWidgets.QHBoxLayout()
        self.dataLayout.setObjectName("dataLayout")
        self.displayDataButton = QtWidgets.QPushButton(self.centralwidget)
        self.displayDataButton.setObjectName("displayDataButton")
        self.dataLayout.addWidget(self.displayDataButton)
        self.plotData = QtWidgets.QPushButton(self.centralwidget)
        self.plotData.setObjectName("plotData")
        self.dataLayout.addWidget(self.plotData)
        self.epochingButton = QtWidgets.QPushButton(self.centralwidget)
        self.epochingButton.setObjectName("epochingButton")
        self.dataLayout.addWidget(self.epochingButton)
        self.mainLayout.addLayout(self.dataLayout)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.mainLayout.addWidget(self.line)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setMinimumSize(QtCore.QSize(0, 25))
        self.label_4.setMaximumSize(QtCore.QSize(1000, 25))
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_6.addWidget(self.label_4)
        self.xyzPath = QtWidgets.QLineEdit(self.centralwidget)
        self.xyzPath.setObjectName("xyzPath")
        self.horizontalLayout_6.addWidget(self.xyzPath)
        self.electrodeMontage = QtWidgets.QComboBox(self.centralwidget)
        self.electrodeMontage.setMinimumSize(QtCore.QSize(130, 25))
        self.electrodeMontage.setMaximumSize(QtCore.QSize(130, 25))
        self.electrodeMontage.setFrame(False)
        self.electrodeMontage.setObjectName("electrodeMontage")
        self.horizontalLayout_6.addWidget(self.electrodeMontage)
        self.mainLayout.addLayout(self.horizontalLayout_6)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.mainLayout.addWidget(self.line_2)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.psdTab = QtWidgets.QWidget()
        self.psdTab.setObjectName("psdTab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.psdTab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.methodLabel = QtWidgets.QLabel(self.psdTab)
        self.methodLabel.setMinimumSize(QtCore.QSize(130, 25))
        self.methodLabel.setMaximumSize(QtCore.QSize(130, 25))
        self.methodLabel.setObjectName("methodLabel")
        self.horizontalLayout.addWidget(self.methodLabel)
        self.psdMethod = QtWidgets.QComboBox(self.psdTab)
        self.psdMethod.setMinimumSize(QtCore.QSize(300, 25))
        self.psdMethod.setMaximumSize(QtCore.QSize(16777215, 25))
        self.psdMethod.setAccessibleName("")
        self.psdMethod.setCurrentText("")
        self.psdMethod.setObjectName("psdMethod")
        self.horizontalLayout.addWidget(self.psdMethod)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.label_2 = QtWidgets.QLabel(self.psdTab)
        self.label_2.setMinimumSize(QtCore.QSize(0, 25))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 25))
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.psdParametersButton = QtWidgets.QPushButton(self.psdTab)
        self.psdParametersButton.setMinimumSize(QtCore.QSize(130, 25))
        self.psdParametersButton.setMaximumSize(QtCore.QSize(130, 25))
        self.psdParametersButton.setObjectName("psdParametersButton")
        self.horizontalLayout_2.addWidget(self.psdParametersButton)
        self.psdParametersLine = QtWidgets.QLineEdit(self.psdTab)
        self.psdParametersLine.setMinimumSize(QtCore.QSize(300, 25))
        self.psdParametersLine.setMaximumSize(QtCore.QSize(16777215, 25))
        self.psdParametersLine.setObjectName("psdParametersLine")
        self.horizontalLayout_2.addWidget(self.psdParametersLine)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.psdParametersText = QtWidgets.QTextEdit(self.psdTab)
        self.psdParametersText.setObjectName("psdParametersText")
        self.verticalLayout_3.addWidget(self.psdParametersText)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.psdButton = QtWidgets.QPushButton(self.psdTab)
        self.psdButton.setObjectName("psdButton")
        self.horizontalLayout_5.addWidget(self.psdButton)
        self.savePsdButton = QtWidgets.QPushButton(self.psdTab)
        self.savePsdButton.setObjectName("savePsdButton")
        self.horizontalLayout_5.addWidget(self.savePsdButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(2, 1)
        self.verticalLayout_3.setStretch(3, 5)
        self.verticalLayout_3.setStretch(4, 1)
        self.tabWidget.addTab(self.psdTab, "")
        self.tfrTab = QtWidgets.QWidget()
        self.tfrTab.setObjectName("tfrTab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tfrTab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.methodLabel_3 = QtWidgets.QLabel(self.tfrTab)
        self.methodLabel_3.setMinimumSize(QtCore.QSize(130, 25))
        self.methodLabel_3.setMaximumSize(QtCore.QSize(130, 25))
        self.methodLabel_3.setObjectName("methodLabel_3")
        self.horizontalLayout_3.addWidget(self.methodLabel_3)
        self.tfrMethodBox = QtWidgets.QComboBox(self.tfrTab)
        self.tfrMethodBox.setMinimumSize(QtCore.QSize(300, 25))
        self.tfrMethodBox.setMaximumSize(QtCore.QSize(16777215, 25))
        self.tfrMethodBox.setAccessibleName("")
        self.tfrMethodBox.setCurrentText("")
        self.tfrMethodBox.setObjectName("tfrMethodBox")
        self.horizontalLayout_3.addWidget(self.tfrMethodBox)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.label = QtWidgets.QLabel(self.tfrTab)
        self.label.setMinimumSize(QtCore.QSize(0, 25))
        self.label.setMaximumSize(QtCore.QSize(16777215, 25))
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.tfrParametersButton = QtWidgets.QPushButton(self.tfrTab)
        self.tfrParametersButton.setMinimumSize(QtCore.QSize(130, 25))
        self.tfrParametersButton.setMaximumSize(QtCore.QSize(130, 25))
        self.tfrParametersButton.setObjectName("tfrParametersButton")
        self.horizontalLayout_4.addWidget(self.tfrParametersButton)
        self.tfrParametersLine = QtWidgets.QLineEdit(self.tfrTab)
        self.tfrParametersLine.setMinimumSize(QtCore.QSize(300, 25))
        self.tfrParametersLine.setMaximumSize(QtCore.QSize(16777215, 25))
        self.tfrParametersLine.setObjectName("tfrParametersLine")
        self.horizontalLayout_4.addWidget(self.tfrParametersLine)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tfrParametersText = QtWidgets.QTextEdit(self.tfrTab)
        self.tfrParametersText.setObjectName("tfrParametersText")
        self.verticalLayout_2.addWidget(self.tfrParametersText)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.tfrButton = QtWidgets.QPushButton(self.tfrTab)
        self.tfrButton.setObjectName("tfrButton")
        self.verticalLayout.addWidget(self.tfrButton)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 5)
        self.tabWidget.addTab(self.tfrTab, "")
        self.mainLayout.addWidget(self.tabWidget)
        self.mainLayout.setStretch(0, 1)
        self.mainLayout.setStretch(1, 1)
        self.mainLayout.setStretch(2, 1)
        self.mainLayout.setStretch(3, 1)
        self.mainLayout.setStretch(5, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 542, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pathButton.setText(_translate("MainWindow", "Choose Path"))
        self.displayDataButton.setText(_translate("MainWindow", "Display Data Informations"))
        self.plotData.setText(_translate("MainWindow", "Visualize Data"))
        self.epochingButton.setText(_translate("MainWindow", "Cut into Epochs"))
        self.label_4.setText(_translate("MainWindow", "Electrode Labeling"))
        self.methodLabel.setText(_translate("MainWindow", "Method"))
        self.label_2.setText(_translate("MainWindow", "Parameters"))
        self.psdParametersButton.setText(_translate("MainWindow", "Import "))
        self.psdButton.setText(_translate("MainWindow", "Visualize PSD"))
        self.savePsdButton.setText(_translate("MainWindow", "Save PSD"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.psdTab), _translate("MainWindow", "PSD "))
        self.methodLabel_3.setText(_translate("MainWindow", "Method"))
        self.label.setText(_translate("MainWindow", "Parameters"))
        self.tfrParametersButton.setText(_translate("MainWindow", "Import"))
        self.tfrButton.setText(_translate("MainWindow", "Visualize TFR"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tfrTab), _translate("MainWindow", "TFR"))
