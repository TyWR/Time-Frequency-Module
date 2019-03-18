from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
from app.psd import PSDWindow
from app.menu_UI import Ui_MenuWindow

"""
File containing the main window class, ie the window for selectionning
the path of the dataset, choose the parameters for computing the PSD etc.
"""
class MenuWindow(QMainWindow) :

    def __init__(self, epochsPSD) :
        super(MenuWindow, self).__init__(parent = None)
        self.psd = epochsPSD
        self.setWindowTitle("Open PSD Visualize")
        self.ui = Ui_MenuWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.setup_ui()

    def setup_ui(self) :
        """Setup the ui with initial values and bindings"""
        self.set_sliders()
        self.set_bindings()

    def set_bindings(self) :
        """Set all the bindings"""
        self.ui.psdButton.clicked.connect(self.open_psd_visualizer)
        self.ui.pathButton.clicked.connect(self.choose_path)
        self.ui.lineEdit.editingFinished.connect(self.path_change)

    def set_sliders(self) :
        """Set slider for extensions"""
        self.ui.chooseFileType.addItem(".ep")
        self.ui.chooseFileType.addItem(".eph")
        self.ui.chooseFileType.addItem(".sef")

        self.ui.psdMethod.addItem('Welch')
        self.ui.psdMethod.addItem('Multitaper')

    def plot_raw_data(self) :
        """Plot the raw data"""
        return 0

    def set_data(self) :
        """Set-up the data in mne class"""
        return 0

    def open_psd_visualizer(self) :
        """Redirect to PSD Visualize app"""
        psdVisualizer = PSDWindow(self.psd)
        psdVisualizer.show()

    #=====================================================================
    # Choosing path
    def choose_path(self) :
        self.filePath, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "Python Files (*.py)")
        self.ui.lineEdit.setText(self.filePath)

    #---------------------------------------------------------------------
    def path_change(self) :
        self.filePath = self.ui.lineEdit.text()
