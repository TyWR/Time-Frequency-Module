from PyQt5.QtWidgets import QDialog, QApplication
import sys

from app.psd import PSDWindow
from app.data import ImportDataWindow
from backend.psd import EpochsPSD
from data.example_1 import get_example1

epochs = get_example1()
epochsPSD = EpochsPSD(epochs, fmin = 0, fmax = 75, tmin = 0, tmax = 0.5, method = 'multitaper', bandwidth = 4)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = PSDWindow(epochsPSD)
    main.show()

    #main = ImportDataWindow()
    #main.show()
    sys.exit(app.exec_())
