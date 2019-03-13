from PyQt5.QtWidgets import QDialog, QApplication
import sys

from app.PSDWindow import PSDWindow
from backend.psd import EpochsPSD
from data.example_1 import get_example1

epochs = get_example1()
epochsPSD = EpochsPSD(epochs, fmin = 0, fmax = 75, tmin = 0, tmax = 0.5, method = 'welch', n_fft = 512, n_per_seg = 30, n_overlap = 15)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = PSDWindow(epochsPSD, fmin = 0, fmax = 75, tmin = 0, tmax = 0.5, method = 'welch', n_fft = 512, n_per_seg = 30, n_overlap = 15)
    main.show()

    sys.exit(app.exec_())
