# -*- coding: utf-8 -*-
'''
批次命名分割出來的小驗證碼並存檔
'''
from PyQt4 import QtCore, QtGui
import sys,random,os
from Image import Image


class RenameWindow(QtGui.QDialog):
    def __init__(self, parent=None):
        super(RenameWindow, self).__init__(parent)
        Img = Image(r"D:/RailWayCapcha", random.choice(os.listdir(r"D:/RailWayCapcha")))
        path = Img.Path
        imageName = Img.imageName
        # 取得處理完後的圖片
        imgarr = Img.StartProcess()

        self.setWindowTitle(u'重新命名驗證碼')
        self.grid = QtGui.QGridLayout(self)
        self.captchaPic = smallPicBox(203,62)
        print(path+'//'+imageName)
        self.grid.addWidget(self.captchaPic,0,0,3,2)
        self.captchaPic.setPixmap(QtGui.QPixmap(path+'//'+imageName))
        # 加入分割後驗證碼圖片的pictureBox
        width,height = 60,60
        self.pic1 = smallPicBox(width,height)
        self.grid.addWidget(self.pic1,4,0,3,2)
        self.input1 = QtGui.QLineEdit()
        self.grid.addWidget(self.input1,4,1,3,2)

        self.pic2 = smallPicBox(width,height)
        self.grid.addWidget(self.pic2,7,0,3,2)
        self.input2 = QtGui.QLineEdit()
        self.grid.addWidget(self.input2,7,1,3,2)

        self.pic3 = smallPicBox(width,height)
        self.grid.addWidget(self.pic3,10,0,3,2)
        self.input3 = QtGui.QLineEdit()
        self.grid.addWidget(self.input3,10,1,3,2)

        self.pic4 = smallPicBox(width,height)
        self.grid.addWidget(self.pic4,13,0,3,2)
        self.input4 = QtGui.QLineEdit()
        self.grid.addWidget(self.input4,13,1,3,2)

        self.pic5 = smallPicBox(width,height)
        self.grid.addWidget(self.pic5,16,0,3,2)
        self.input5 = QtGui.QLineEdit()
        self.grid.addWidget(self.input5,16,1,3,2)

        self.pic6 = smallPicBox(width,height)
        self.grid.addWidget(self.pic6,19,0,3,2)
        self.input6 = QtGui.QLineEdit()
        self.grid.addWidget(self.input6,19,1,3,2)



class smallPicBox(QtGui.QLabel):
    def __init__(self, width,height,parent=None):
        super(smallPicBox, self).__init__(parent)
        self.setFixedSize(width,height)
        self.setStyleSheet(
            'border:1px solid rgb(0, 0, 0)'
        )

if __name__ == '__main__':
    app =QtGui.QApplication(sys.argv)
    RenameWindow = RenameWindow()
    # MainWindow.resize(600, 400)
    RenameWindow.show()
    app.exec_()