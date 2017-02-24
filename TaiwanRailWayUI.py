# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TaiwanRailWay.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import datetime,json,sys,io

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(628, 401)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        #  身份證字號
        self.lbID = QtGui.QLabel(self.centralwidget)
        self.lbID.setGeometry(QtCore.QRect(10, 20, 81, 31))
        self.lbID.setObjectName(_fromUtf8("lbID"))

        self.textID = QtGui.QTextEdit(self.centralwidget)
        self.textID.setGeometry(QtCore.QRect(100, 20, 111, 21))
        self.textID.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textID.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textID.setObjectName(_fromUtf8("textID"))

        self.groupBoxGo = QtGui.QGroupBox(self.centralwidget)
        self.groupBoxGo.setGeometry(QtCore.QRect(0, 70, 231, 301))
        self.groupBoxGo.setObjectName(_fromUtf8("groupBoxGo"))

        #  ===============================================
        #                            去程
        # ================================================
        #  起站
        self.lb_Go_StartStation = QtGui.QLabel(self.groupBoxGo)
        self.lb_Go_StartStation.setGeometry(QtCore.QRect(20, 20, 71, 21))
        self.lb_Go_StartStation.setObjectName(_fromUtf8("lb_Go_StartStation"))
        self.cb_Go_StartStation = QtGui.QComboBox(self.groupBoxGo)
        self.cb_Go_StartStation.setGeometry(QtCore.QRect(90, 20, 111, 20))
        self.cb_Go_StartStation.setObjectName(_fromUtf8("cb_Go_StartStation"))
        self.cbStationAddItem(self.cb_Go_StartStation)

        # 終點站
        self.lb_Go_EndStation = QtGui.QLabel(self.groupBoxGo)
        self.lb_Go_EndStation.setGeometry(QtCore.QRect(20, 70, 47, 16))
        self.lb_Go_EndStation.setObjectName(_fromUtf8("lb_Go_EndStation"))
        self.cb_Go_EndStation = QtGui.QComboBox(self.groupBoxGo)
        self.cb_Go_EndStation.setGeometry(QtCore.QRect(90, 70, 111, 20))
        self.cb_Go_EndStation.setObjectName(_fromUtf8("cb_Go_EndStation"))
        self.cbStationAddItem(self.cb_Go_EndStation)
        #  日期
        self.lb_Go_Date = QtGui.QLabel(self.groupBoxGo)
        self.lb_Go_Date.setGeometry(QtCore.QRect(20, 110, 47, 12))
        self.lb_Go_Date.setObjectName(_fromUtf8("lb_Go_Date"))
        self.cb_Go_Date = QtGui.QComboBox(self.groupBoxGo)
        self.cb_Go_Date.setGeometry(QtCore.QRect(90, 110, 110, 20))
        self.cb_Go_Date.setObjectName(_fromUtf8("cb_Go_Date"))
        self.cbDateAddItem(self.cb_Go_Date)
        # 開始時間
        self.lb_Go_StartTime = QtGui.QLabel(self.groupBoxGo)
        self.lb_Go_StartTime.setGeometry(QtCore.QRect(20, 150, 61, 16))
        self.lb_Go_StartTime.setObjectName(_fromUtf8("lb_Go_StartTime"))
        self.cb_Go_StartTime = QtGui.QComboBox(self.groupBoxGo)
        self.cb_Go_StartTime.setGeometry(QtCore.QRect(90, 150, 96, 20))
        self.cb_Go_StartTime.setObjectName(_fromUtf8("cb_Go_StartTime"))
        self.cbTimeAddItem(self.cb_Go_StartTime)
        # 截止時間
        self.lb_Go_EndTime = QtGui.QLabel(self.groupBoxGo)
        self.lb_Go_EndTime.setGeometry(QtCore.QRect(20, 180, 61, 16))
        self.lb_Go_EndTime.setObjectName(_fromUtf8("lb_Go_EndTime"))
        self.cb_Go_EndTime = QtGui.QComboBox(self.groupBoxGo)
        self.cb_Go_EndTime.setGeometry(QtCore.QRect(90, 180, 96, 20))
        self.cb_Go_EndTime.setObjectName(_fromUtf8("cb_Go_EndTime"))
        self.cbTimeAddItem(self.cb_Go_EndTime)
        #  車種
        self.lb_Go_Kind = QtGui.QLabel(self.groupBoxGo)
        self.lb_Go_Kind.setGeometry(QtCore.QRect(20, 220, 47, 12))
        self.lb_Go_Kind.setObjectName(_fromUtf8("lb_Go_Kind"))
        self.cb_Go_Kind = QtGui.QComboBox(self.groupBoxGo)
        self.cb_Go_Kind.setGeometry(QtCore.QRect(90, 220, 70, 20))
        self.cb_Go_Kind.setObjectName(_fromUtf8("cb_Go_Kind"))
        self.cbKindAddItem(self.cb_Go_Kind)
        #  訂票張數
        self.lb_Go_Num = QtGui.QLabel(self.groupBoxGo)
        self.lb_Go_Num.setGeometry(QtCore.QRect(20, 260, 61, 16))
        self.lb_Go_Num.setObjectName(_fromUtf8("lb_Go_Num"))
        self.cb_Go_Num = QtGui.QComboBox(self.groupBoxGo)
        self.cb_Go_Num.setGeometry(QtCore.QRect(90, 260, 33, 20))
        self.cb_Go_Num.setObjectName(_fromUtf8("cb_Go_Num"))
        self.cbNumAddItem(self.cb_Go_Num)

        # ======================================================
        #                          回程
        # ======================================================

        self.groupBoxBack = QtGui.QGroupBox(self.centralwidget)
        self.groupBoxBack.setGeometry(QtCore.QRect(240, 70, 221, 301))
        self.groupBoxBack.setObjectName(_fromUtf8("groupBoxBack"))


        # 回程日期
        self.lb_Back_Date = QtGui.QLabel(self.groupBoxBack)
        self.lb_Back_Date.setGeometry(QtCore.QRect(20, 120, 47, 12))
        self.lb_Back_Date.setObjectName(_fromUtf8("lb_Back_Date"))
        self.cb_Back_Date = QtGui.QComboBox(self.groupBoxBack)
        self.cb_Back_Date.setGeometry(QtCore.QRect(90, 110, 110, 20))
        self.cb_Back_Date.setObjectName(_fromUtf8("cb_Back_Date"))
        self.cbDateAddItem(self.cb_Back_Date)
        # 回程起站
        self.lb_Back_StartStation = QtGui.QLabel(self.groupBoxBack)
        self.lb_Back_StartStation.setGeometry(QtCore.QRect(20, 20, 71, 21))
        self.lb_Back_StartStation.setObjectName(_fromUtf8("lb_Back_StartStation"))
        self.cb_Back_StartStation = QtGui.QComboBox(self.groupBoxBack)
        self.cb_Back_StartStation.setGeometry(QtCore.QRect(90, 20, 111, 20))
        self.cb_Back_StartStation.setObjectName(_fromUtf8("cb_Back_StartStation"))
        self.cbStationAddItem(self.cb_Back_StartStation)
        # 回程終點站
        self.lb_Back_EndStation = QtGui.QLabel(self.groupBoxBack)
        self.lb_Back_EndStation.setGeometry(QtCore.QRect(20, 70, 47, 16))
        self.lb_Back_EndStation.setObjectName(_fromUtf8("lb_Back_EndStation"))
        self.cb_Back_EndStation = QtGui.QComboBox(self.groupBoxBack)
        self.cb_Back_EndStation.setGeometry(QtCore.QRect(90, 70, 111, 20))
        self.cb_Back_EndStation.setObjectName(_fromUtf8("cb_Back_EndStation"))
        self.cbStationAddItem(self.cb_Back_EndStation)

        # 回程開始時間
        self.lb_Back_StartTime = QtGui.QLabel(self.groupBoxBack)
        self.lb_Back_StartTime.setGeometry(QtCore.QRect(20, 150, 61, 16))
        self.lb_Back_StartTime.setObjectName(_fromUtf8("lb_Back_StartTime"))
        self.cb_Back_StartTime = QtGui.QComboBox(self.groupBoxBack)
        self.cb_Back_StartTime.setGeometry(QtCore.QRect(90, 150, 96, 20))
        self.cb_Back_StartTime.setObjectName(_fromUtf8("cb_Back_StartTime"))
        self.cbTimeAddItem(self.cb_Back_StartTime)
        # 車種
        self.lb_Back_Kind = QtGui.QLabel(self.groupBoxBack)
        self.lb_Back_Kind.setGeometry(QtCore.QRect(20, 230, 47, 12))
        self.lb_Back_Kind.setObjectName(_fromUtf8("lb_Back_Kind"))
        self.cb_Back_Kind = QtGui.QComboBox(self.groupBoxBack)
        self.cb_Back_Kind.setGeometry(QtCore.QRect(90, 220, 70, 20))
        self.cb_Back_Kind.setObjectName(_fromUtf8("cb_Back_Kind"))
        self.cbKindAddItem(self.cb_Back_Kind)
        # 回程終止時間
        self.lb_Back_EndTime = QtGui.QLabel(self.groupBoxBack)
        self.lb_Back_EndTime.setGeometry(QtCore.QRect(20, 190, 61, 16))
        self.lb_Back_EndTime.setObjectName(_fromUtf8("lb_Back_EndTime"))
        self.cb_Back_EndTime = QtGui.QComboBox(self.groupBoxBack)
        self.cb_Back_EndTime.setGeometry(QtCore.QRect(90, 190, 96, 20))
        self.cb_Back_EndTime.setObjectName(_fromUtf8("cb_Back_EndTime"))
        self.cbTimeAddItem(self.cb_Back_EndTime)
        # 回程訂票張數
        self.lb_Back_Num = QtGui.QLabel(self.groupBoxBack)
        self.lb_Back_Num.setGeometry(QtCore.QRect(20, 260, 61, 16))
        self.lb_Back_Num.setObjectName(_fromUtf8("lb_Back_Num"))
        self.cb_Back_Num = QtGui.QComboBox(self.groupBoxBack)
        self.cb_Back_Num.setGeometry(QtCore.QRect(90, 260, 33, 20))
        self.cb_Back_Num.setObjectName(_fromUtf8("cb_Back_Num"))
        self.cbNumAddItem(self.cb_Back_Num)

        # 開始訂票按鈕
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(380, 10, 81, 51))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        # 是否為來回票checkbox
        self.ckIsTwoWay = QtGui.QCheckBox(self.centralwidget)
        self.ckIsTwoWay.setGeometry(QtCore.QRect(250, 20, 101, 16))
        self.ckIsTwoWay.setObjectName(_fromUtf8("ckIsTwoWay"))

        # ======================================================
        #                           結果
        # ======================================================

        self.GroupBoxMessage = QtGui.QGroupBox(self.centralwidget)
        self.GroupBoxMessage.setGeometry(QtCore.QRect(470, 70, 141, 291))
        self.GroupBoxMessage.setObjectName(_fromUtf8("GroupBoxMessage"))
        # 進度條
        self.progressBar = QtGui.QProgressBar(self.GroupBoxMessage)
        self.progressBar.setGeometry(QtCore.QRect(10, 40, 121, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.lbProgressBar = QtGui.QLabel(self.GroupBoxMessage)
        self.lbProgressBar.setGeometry(QtCore.QRect(10, 20, 61, 16))
        self.lbProgressBar.setObjectName(_fromUtf8("lbProgressBar"))
        # 回傳訊息
        self.lbMessage = QtGui.QLabel(self.GroupBoxMessage)
        self.lbMessage.setGeometry(QtCore.QRect(10, 80, 61, 16))
        self.lbMessage.setObjectName(_fromUtf8("lbMessage"))

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 628, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName(_fromUtf8("menu"))
        MainWindow.setMenuBar(self.menubar)
        self.action = QtGui.QAction(MainWindow)
        self.action.setObjectName(_fromUtf8("action"))
        self.action_2 = QtGui.QAction(MainWindow)
        self.action_2.setObjectName(_fromUtf8("action_2"))
        self.menu.addAction(self.action)
        self.menu.addAction(self.action_2)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.cb_Go_StartStation, self.cb_Go_EndStation)
        MainWindow.setTabOrder(self.cb_Go_EndStation, self.cb_Go_Date)
        MainWindow.setTabOrder(self.cb_Go_Date, self.cb_Go_StartTime)
        MainWindow.setTabOrder(self.cb_Go_StartTime, self.cb_Go_EndTime)
        MainWindow.setTabOrder(self.cb_Go_EndTime, self.cb_Go_Kind)
        MainWindow.setTabOrder(self.cb_Go_Kind, self.cb_Go_Num)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.lbID.setText(_translate("MainWindow", "身份證字號：", None))
        self.groupBoxGo.setTitle(_translate("MainWindow", "【出發／單程】", None))
        self.lb_Go_StartStation.setText(_translate("MainWindow", "起站：", None))
        self.lb_Go_EndStation.setText(_translate("MainWindow", "到站：", None))
        self.lb_Go_Date.setText(_translate("MainWindow", "日期：", None))
        self.lb_Go_StartTime.setText(_translate("MainWindow", "起始時間：", None))
        self.lb_Go_EndTime.setText(_translate("MainWindow", "截止時間：", None))
        self.lb_Go_Kind.setText(_translate("MainWindow", "車種：", None))
        self.lb_Go_Num.setText(_translate("MainWindow", "訂票張數：", None))
        self.groupBoxBack.setTitle(_translate("MainWindow", "【回程】", None))
        self.lb_Back_Date.setText(_translate("MainWindow", "日期：", None))
        self.lb_Back_EndStation.setText(_translate("MainWindow", "到站：", None))
        self.lb_Back_StartStation.setText(_translate("MainWindow", "起站：", None))
        self.lb_Back_Kind.setText(_translate("MainWindow", "車種：", None))
        self.lb_Back_EndTime.setText(_translate("MainWindow", "截止時間：", None))
        self.lb_Back_Num.setText(_translate("MainWindow", "訂票張數：", None))
        self.lb_Back_StartTime.setText(_translate("MainWindow", "起始時間：", None))
        self.pushButton.setText(_translate("MainWindow", "開始訂票", None))
        self.ckIsTwoWay.setText(_translate("MainWindow", "是否為來回票", None))
        self.GroupBoxMessage.setTitle(_translate("MainWindow", "【結果】", None))
        self.lbProgressBar.setText(_translate("MainWindow", "訂票進度：", None))
        self.lbMessage.setText(_translate("MainWindow", "訊息：", None))
        self.menu.setTitle(_translate("MainWindow", "說明", None))
        self.action.setText(_translate("MainWindow", "使用方法", None))
        self.action_2.setText(_translate("MainWindow", "免責聲明", None))

    # 為訂票張數的combobox add item
    def cbNumAddItem(self,cb):
        cb.addItems([str(i) for i in range(1, 7)])
    # 為時間下拉選單產生時段
    def cbTimeAddItem(self,cb):
        cb.addItems([str(i).zfill(2)+':00' for i in range(24)])
        cb.addItem('23:59')
    #  為車種下拉選單產生data
    def cbKindAddItem(self, cb):
        cb.addItem(self.translate('全部車種'),'*4')
        cb.addItem(self.translate('自強號'),'*1')
        cb.addItem(self.translate('莒光號'),'*2')
        cb.addItem(self.translate('復興號'),'*3')
    # 為日期下拉選單產生資料
    def cbDateAddItem(self,cb):
        date = datetime.datetime.now()
        dateOfWeek =['一','二','三','四','五','六','日']
        cb.addItem(date.date().strftime('%Y/%m/%d')+' ('+self.translate(dateOfWeek[date.date().weekday()])+')')
        for i in range(16):
            date += datetime.timedelta(days=1)
            cb.addItem(date.date().strftime('%Y/%m/%d')+' ('+self.translate(dateOfWeek[date.date().weekday()])+')')

    # 產生車站下拉選單的資料
    def cbStationAddItem(self,cb):
        try:
            with io.open('station.json', 'r', encoding='utf8') as f:
                sdata = json.loads(f.read())
                # Sort it by station numbers
                sdata_sorted = sorted(
                    sdata, key=lambda s: s['ID']
                )
                for ii in range(len(sdata_sorted)):

                    cb.addItem(sdata_sorted[ii]['Station'],int(sdata_sorted[ii]['ID']))

        except IOError as ioerr:
            print('File Error: ' + str(ioerr))






    #  將字串翻成中文 避免亂碼
    def translate(self,str):
        return _translate("MainWindow", str, None)

