# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'caliUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import calibration


class Ui_MainWindow(object):
    def slota(self, MainWindow):#calibrate

        self.textBrowser.append("loading...")
        mtx, dist, rvecs, tvecs, rms, path2 = calibration.calibrate()
        self.textBrowser.append("内参矩阵：")
        self.textBrowser.append(str(mtx))
        self.textBrowser.append("畸变系数：")
        self.textBrowser.append(str(dist))
        self.textBrowser.append("旋转向量：")
        self.textBrowser.append(str(rvecs))
        self.textBrowser.append("平移向量：")
        self.textBrowser.append(str(tvecs))
        self.textBrowser.append("reprojection error：")
        self.textBrowser.append(str(rms))
        self.textBrowser.append("结果存储路径：")
        self.textBrowser.append(path2)
        self.textBrowser.append("Calibrate Done\n")

    def slotb(self, MainWindow):#draw

        self.textBrowser.append("loading...")
        num, path2 = calibration.AxisAndBox()
        self.textBrowser.append("已处理"+str(num)+"张图像")
        self.textBrowser.append("结果存储路径：")
        self.textBrowser.append(path2)
        self.textBrowser.append("Draw Done\n")

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 400)
        font = QtGui.QFont()
        font.setFamily("Adobe 黑体 Std R")
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(320, 120, 111, 41))
        self.pushButton.setObjectName("pushButton")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(20, 50, 271, 261))
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(320, 250, 111, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(300, 165, 400, 80))
        font = QtGui.QFont()
        font.setFamily("Adobe 黑体 Std R")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(300, 30, 400, 81))
        font = QtGui.QFont()
        font.setFamily("Adobe 黑体 Std R")
        font.setPointSize(9)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 10, 300, 31))
        font = QtGui.QFont()
        font.setFamily("Adobe 黑体 Std R")
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 506, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.textBrowser.append("欢迎使用caliUI!")
        self.textBrowser.append("提示：若用于标定的照片数>20,为避免弹窗过多,窗口将不予展示")
        self.pushButton.clicked.connect(self.slota)
        self.pushButton_2.clicked.connect(self.slotb)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Calibrate"))
        self.pushButton_2.setText(_translate("MainWindow", "Draw"))
        self.label.setText(_translate("MainWindow", "说明：在运行Calibrate后，方能使用draw,Draw\n"
                                        "将在畸变矫正后的图片中画出3-D Box和坐标轴，\n"
                                        "并将结果存放于Calibrate结果存放的路径下"))
        self.label_2.setText(_translate("MainWindow", "说明：按下Calibrate按钮，在目录选择对话框中\n"
                                        "选择用于标定的照片所在文件夹、结果存放的文\n"
                                        "件夹"))
        self.label_3.setText(_translate("MainWindow", "信息输出"))
