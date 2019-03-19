from PyQt5.QtWidgets import QDialog, QApplication
import sys
import os
print('CURRENT DIRECTORY FOLDER : ', os.getcwd())

from app.menu import MenuWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MenuWindow()
    main.show()
    sys.exit(app.exec_())
