from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtGui import QIcon
import sys
import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
print('CURRENT DIRECTORY FOLDER : ', os.getcwd())

from app.menu import MenuWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MenuWindow()
    main.setWindowIcon(QIcon('media/main.png'))
    main.show()
    sys.exit(app.exec_())
