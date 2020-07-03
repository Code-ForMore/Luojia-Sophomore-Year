import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow
import calibration
from caliUIv4 import *


if __name__ == '__main__':
    '''
    主函数,由此打开UI
    '''

    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()

    sys.exit(app.exec_())
    # 为什么有时会读取照片失败？OpenCV的imread只能读取英文路径下的文件，不能出现中文。
