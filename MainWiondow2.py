# -*- coding: utf-8 -*-
# 直接調用pyqt 不用designer

from PyQt4 import QtCore, QtGui
import datetime,json,sys,io
from BuyTicket import BuyTicket

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle(u'台鐵訂票助手')
        self.form_widget = FormWidget(self)

        # 加入form_widget 表單主體
        self.setCentralWidget(self.form_widget)

        # 加入menu bar 幫助
        AboutAction = QtGui.QAction(u'關於', self)
        AboutAction.triggered.connect(self.form_widget.showAbout)
        menubar = self.menuBar()
        AboutMenu = menubar.addMenu(u'幫助')
        AboutMenu.addAction(AboutAction)




class FormWidget(QtGui.QWidget):

    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)
        self.layout = QtGui.QVBoxLayout(self)

        self.button1 = QtGui.QPushButton("Button 1")
        self.button1.clicked.connect(lambda: self.showAbout())
        self.layout.addWidget(self.button1)

        self.button2 = QtGui.QPushButton("Button 2")
        self.layout.addWidget(self.button2)

        self.setLayout(self.layout)

    # 為訂票張數的combobox add item
    def cbNumAddItem(self, cb):
        cb.addItems([str(i) for i in range(1, 7)])


    # 為時間下拉選單產生時段
    def cbTimeAddItem(self, cb):
        cb.addItems([str(i).zfill(2) + ':00' for i in range(24)])
        cb.addItem('23:59')


    #  為車種下拉選單產生data
    def cbKindAddItem(self, cb):
        cb.addItem(self.translate('全部車種'), '*4')
        cb.addItem(self.translate('自強號'), '*1')
        cb.addItem(self.translate('莒光號'), '*2')
        cb.addItem(self.translate('復興號'), '*3')


    # 為日期下拉選單產生資料
    def cbDateAddItem(self, cb):
        date = datetime.datetime.now()
        strDate = date.date().strftime('%Y/%m/%d')
        dateOfWeek = ['一', '二', '三', '四', '五', '六', '日']
        cb.addItem(strDate + ' (' + self.translate(dateOfWeek[date.date().weekday()]) + ')', strDate + '-00')
        for i in range(16):
            date += datetime.timedelta(days=1)
            strDate = date.date().strftime('%Y/%m/%d')
            cb.addItem(strDate + ' (' + self.translate(dateOfWeek[date.date().weekday()]) + ')',
                       strDate + '-' + str(i + 1).zfill(2))


    # 產生車站下拉選單的資料
    def cbStationAddItem(self, cb):
        try:
            with io.open('station.json', 'r', encoding='utf8') as f:
                sdata = json.loads(f.read())
                # Sort it by station numbers
                sdata_sorted = sorted(
                    sdata, key=lambda s: s['ID']
                )
                for ii in range(len(sdata_sorted)):
                    cb.addItem(sdata_sorted[ii]['Station'], int(sdata_sorted[ii]['ID']))

        except IOError as ioerr:
            print('File Error: ' + str(ioerr))

    # 顯示出對話視窗 要在connect裡傳參數可使用 lambda: self.showMessage(u'text you want to display')
    def showMessage(self,message=None):
        QtGui.QMessageBox.information(self, u"提示", message if message != None else u'發生錯誤!!')

    def showAbout(self):
        QtGui.QMessageBox.about(self,u"說明",
                                u"""
        <b>台鐵訂票程式</b>
        <p>Copyright © 2017 Lin Yich - All rights reserved.</p>
        <p>這程式能實現台鐵自動化訂票</p>
        <p>僅供學術交流用途，請勿從事非法活動</p>
        <p>需求環境：請參閱Readme.md</p>
                                """)


if __name__ == '__main__':
    app =QtGui.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.resize(300, 60)
    MainWindow.show()
    app.exec_()
