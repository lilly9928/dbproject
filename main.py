import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import uic

## python실행파일 디렉토리
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
from_class = uic.loadUiType(BASE_DIR + r'\main_page.ui')[0]


# MainWindow Class 선언
class WindowClass(QWidget, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


# 실행
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()