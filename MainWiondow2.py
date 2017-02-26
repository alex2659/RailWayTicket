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



        # ====================設定左邊layout 用來呈現訂票介面 裡面包含ticketInfo Layout====================
        self.leftLayout = QtGui.QGridLayout()


        # =============設定left layout的上方控件
        self.lbID = QtGui.QLabel( u"身份證字號：")
        self.lbID.setObjectName(u"lbID")
        self.leftLayout.addWidget(self.lbID,0,0)
        self.textID = QtGui.QLineEdit()
        self.textID.setObjectName(u"textID")
        self.leftLayout.addWidget(self.textID,0,1)

        self.submitBtn = QtGui.QPushButton(u'開始訂票')
        self.submitBtn.setFixedSize(70,70)
        self.leftLayout.addWidget(self.submitBtn,0,3,2,2)

        self.lb_StartStation = QtGui.QLabel(u'起站代碼')
        self.leftLayout.addWidget(self.lb_StartStation,1,0,1,1)
        self.cb_StartStation = QtGui.QComboBox()
        self.cbStationAddItem(self.cb_StartStation)
        self.leftLayout.addWidget(self.cb_StartStation,1,1,1,1)

        self.lb_EndStation = QtGui.QLabel(u'到站代碼')
        self.leftLayout.addWidget(self.lb_EndStation,2,0,1,1)
        self.cb_EndStation = QtGui.QComboBox()
        self.cbStationAddItem(self.cb_EndStation)
        self.leftLayout.addWidget(self.cb_EndStation,2,1,1,1)

        # self.isTwoWay = QtGui.QCheckBox(u'是否為來回票')
        # self.isTwoWay.setChecked(True)
        # self.leftLayout.addWidget(self.isTwoWay,3,3,1,3)

        # =============ticketInfo Layout 用來放置去回程的控件
        self.TicketInfolayout = QtGui.QGridLayout()
        self.leftLayout.addLayout(self.TicketInfolayout,4,0,10,5)

        # =============設定位在ticketInfo裡的出發layout
        self.GoLayout = QtGui.QGroupBox()
        self.GoLayout.setTitle(u'【出發／單程】')
        vbox = QtGui.QGridLayout()

        self.lb_Go_Date = QtGui.QLabel(u'乘車日期')
        vbox.addWidget(self.lb_Go_Date,0,0,1,2)
        self.cb_Go_Date = QtGui.QComboBox()
        self.cbDateAddItem(self.cb_Go_Date)
        vbox.addWidget(self.cb_Go_Date,0,3,1,2)

        self.lb_Go_Num = QtGui.QLabel(u'訂票張數')
        vbox.addWidget(self.lb_Go_Num,1,0,1,2)
        self.cb_Go_Num = QtGui.QComboBox()
        self.cbNumAddItem(self.cb_Go_Num)
        vbox.addWidget(self.cb_Go_Num,1,3,1,1)

        self.lb_Go_Kind = QtGui.QLabel(u'車種')
        vbox.addWidget(self.lb_Go_Kind,2,0,1,2)
        self.cb_Go_Kind = QtGui.QComboBox()
        self.cbKindAddItem(self.cb_Go_Kind)
        vbox.addWidget(self.cb_Go_Kind,2,3,1,2)

        self.lb_Go_StartTime = QtGui.QLabel(u'起始時間')
        vbox.addWidget(self.lb_Go_StartTime, 3, 0, 1, 2)
        self.cb_Go_StartTime = QtGui.QComboBox()
        self.cbTimeAddItem(self.cb_Go_StartTime)
        vbox.addWidget(self.cb_Go_StartTime, 3, 3, 1, 1)

        self.lb_Go_EndTime = QtGui.QLabel(u'截止時間')
        vbox.addWidget(self.lb_Go_EndTime, 4, 0, 1, 2)
        self.cb_Go_EndTime = QtGui.QComboBox()
        self.cbTimeAddItem(self.cb_Go_EndTime)
        vbox.addWidget(self.cb_Go_EndTime, 4, 3, 1, 1)

        self.GoLayout.setLayout(vbox)
        self.TicketInfolayout.addWidget(self.GoLayout,0,0,1,3)

        # =============設定位在ticketInfo裡的回程layout
        self.BackLayout = QtGui.QGroupBox()
        self.BackLayout.setTitle(u'【回程】')
        self.BackLayout.setCheckable(True)
        backBox = QtGui.QGridLayout()

        self.lb_Back_Date = QtGui.QLabel(u'乘車日期')
        backBox.addWidget(self.lb_Back_Date,0,0,1,2)
        self.cb_Back_Date = QtGui.QComboBox()
        self.cbDateAddItem(self.cb_Back_Date)
        backBox.addWidget(self.cb_Back_Date,0,3,1,2)

        self.lb_Back_Num = QtGui.QLabel(u'訂票張數')
        backBox.addWidget(self.lb_Back_Num,1,0,1,2)
        self.cb_Back_Num = QtGui.QComboBox()
        self.cbNumAddItem(self.cb_Back_Num)
        backBox.addWidget(self.cb_Back_Num,1,3,1,1)

        self.lb_Back_Kind = QtGui.QLabel(u'車種')
        backBox.addWidget(self.lb_Back_Kind,2,0,1,2)
        self.cb_Back_Kind = QtGui.QComboBox()
        self.cbKindAddItem(self.cb_Back_Kind)
        backBox.addWidget(self.cb_Back_Kind,2,3,1,2)

        self.lb_Back_StartTime = QtGui.QLabel(u'起始時間')
        backBox.addWidget(self.lb_Back_StartTime, 3, 0, 1, 2)
        self.cb_Back_StartTime = QtGui.QComboBox()
        self.cbTimeAddItem(self.cb_Back_StartTime)
        backBox.addWidget(self.cb_Back_StartTime, 3, 3, 1, 1)

        self.lb_Back_EndTime = QtGui.QLabel(u'截止時間')
        backBox.addWidget(self.lb_Back_EndTime, 4, 0, 1, 2)
        self.cb_Back_EndTime = QtGui.QComboBox()
        self.cbTimeAddItem(self.cb_Back_EndTime)
        backBox.addWidget(self.cb_Back_EndTime, 4, 3, 1, 1)

        self.BackLayout.setLayout(backBox)
        self.TicketInfolayout.addWidget(self.BackLayout,0,3,1,3)





        # ====================設定右方layout====================
        self.rightLayout = QtGui.QVBoxLayout()
        self.groupBox=QtGui.QGroupBox()
        self.rightLayout.addWidget(self.groupBox)




        # ====================主要layout======================
        self.mainLayout = QtGui.QHBoxLayout()
        self.mainLayout.addLayout(self.leftLayout)
        # 分隔線
        line = QtGui.QFrame()
        line.setFrameStyle(QtGui.QFrame.VLine| QtGui.QFrame.Sunken)
        self.mainLayout.addWidget(line)
        self.mainLayout.addLayout(self.rightLayout)
        self.setLayout(self.mainLayout)

    # 為訂票張數的combobox add item
    def cbNumAddItem(self, cb):
        cb.addItems([str(i) for i in range(1, 7)])


    # 為時間下拉選單產生時段
    def cbTimeAddItem(self, cb):
        cb.addItems([str(i).zfill(2) + ':00' for i in range(24)])
        cb.addItem('23:59')


    #  為車種下拉選單產生data
    def cbKindAddItem(self, cb):
        cb.addItem(u'全部車種', '*4')
        cb.addItem(u'自強號', '*1')
        cb.addItem(u'莒光號', '*2')
        cb.addItem(u'復興號', '*3')


    # 為日期下拉選單產生資料
    def cbDateAddItem(self, cb):
        date = datetime.datetime.now()
        strDate = date.date().strftime('%Y/%m/%d')
        dateOfWeek = ['一', '二', '三', '四', '五', '六', '日']
        cb.addItem(strDate + ' (' + unicode(dateOfWeek[date.date().weekday()],"utf-8") + ')', strDate + '-00')
        for i in range(16):
            date += datetime.timedelta(days=1)
            strDate = date.date().strftime('%Y/%m/%d')
            cb.addItem(strDate + ' (' + unicode(dateOfWeek[date.date().weekday()],"utf-8") + ')',
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
    # MainWindow.resize(600, 400)
    MainWindow.show()
    app.exec_()
