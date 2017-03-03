# -*- coding: utf-8 -*-
'''
批次命名分割出來的小驗證碼並存檔
'''
from PyQt4 import QtCore, QtGui
from PIL import Image as pilIm
import sys,random,os,requests
from StringIO import StringIO
from Image import Image
import cv2



class RenameWindow(QtGui.QDialog):
    def __init__(self, parent=None):
        super(RenameWindow, self).__init__(parent)
        self.setWindowTitle(u'重新命名驗證碼')
        self.grid = QtGui.QGridLayout(self)

        self.captchaPic = smallPicBox(203,62)
        self.grid.addWidget(self.captchaPic,0,0,3,2)
        self.changePicBtn = QtGui.QPushButton(u'換圖')
        self.changePicBtn.clicked.connect(self.GetImage)
        self.grid.addWidget(self.changePicBtn,0,2,3,3)
        # 加入分割後驗證碼圖片的pictureBox
        width,height = 60,60
        self.pic1 = smallPicBox(width,height)
        self.grid.addWidget(self.pic1,4,0,3,2)
        self.input1 = QtGui.QLineEdit()
        self.input1.returnPressed.connect(self.saveImg)
        self.grid.addWidget(self.input1,4,1,3,2)

        self.pic2 = smallPicBox(width,height)
        self.grid.addWidget(self.pic2,7,0,3,2)
        self.input2 = QtGui.QLineEdit()
        self.input2.returnPressed.connect(self.saveImg)
        self.grid.addWidget(self.input2,7,1,3,2)

        self.pic3 = smallPicBox(width,height)
        self.grid.addWidget(self.pic3,10,0,3,2)
        self.input3 = QtGui.QLineEdit()
        self.input3.returnPressed.connect(self.saveImg)
        self.grid.addWidget(self.input3,10,1,3,2)

        self.pic4 = smallPicBox(width,height)
        self.grid.addWidget(self.pic4,13,0,3,2)
        self.input4 = QtGui.QLineEdit()
        self.input4.returnPressed.connect(self.saveImg)
        self.grid.addWidget(self.input4,13,1,3,2)

        self.pic5 = smallPicBox(width,height)
        self.grid.addWidget(self.pic5,16,0,3,2)
        self.input5 = QtGui.QLineEdit()
        self.input5.returnPressed.connect(self.saveImg)
        self.grid.addWidget(self.input5,16,1,3,2)

        self.pic6 = smallPicBox(width,height)
        self.grid.addWidget(self.pic6,19,0,3,2)
        self.input6 = QtGui.QLineEdit()
        self.input6.returnPressed.connect(self.saveImg)
        self.grid.addWidget(self.input6,19,1,3,2)

        self.setTabOrder(self.pic1, self.pic2)
        self.setTabOrder(self.pic2, self.pic3)
        self.setTabOrder(self.pic3, self.pic4)
        self.setTabOrder(self.pic4, self.pic5)
        self.setTabOrder(self.pic5, self.pic6)

        self.pixBoxs = [self.pic1, self.pic2, self.pic3, self.pic4, self.pic5, self.pic6]
        self.inputBoxs = [self.input1,self.input2,self.input3,self.input4,self.input5,self.input6]

        # 取得驗證碼
        self.GetImage()


    def GetImage(self):
        # 取得驗證碼stream
        s = requests.Session()
        req = s.get('http://railway.hinet.net/ImageOut.jsp')

        im = pilIm.open(StringIO(req.content)).convert('RGB')
        io = StringIO()
        im.save(io, format='png')
        qimg = QtGui.QImage.fromData(io.getvalue())
        self.captchaPic.setPixmap(QtGui.QPixmap(qimg))

        Img = Image(req.content)
        # 取得處理完後的圖片
        imgarr = Img.StartProcess()

        for index,img in enumerate(imgarr):
            try:
                height, width,channel = img.shape
                bytes = 3*width
                self.pixBoxs[index].setPixmap(QtGui.QPixmap(QtGui.QImage(img.data, width, height,bytes, QtGui.QImage.Format_RGB888)))
            except:
                pass

    def saveImg(self):
        print('存檔')
        # 取得圖片
        self.GetImage()
        # 清空輸入框
        for i,obj in enumerate(self.inputBoxs):
            obj.clear()

        self.input1.setFocus(True)



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