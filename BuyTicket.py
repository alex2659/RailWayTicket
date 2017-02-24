# encoding: utf-8

class BuyTicket:
    def __init__(self, mainWindow):
        # 身份證字號
        self.ID = mainWindow.textID.toPlainText()
        # 是否為來回票
        self.IsTwoWay = mainWindow.ckIsTwoWay.isChecked()

        # 去程日期
        self.Go_Date = unicode(mainWindow.cb_Go_Date.currentText())
        # 去程開始時間
        self.Go_sTime = unicode(mainWindow.cb_Go_StartTime.currentText())
        #去程結束時間
        self.Go_eTime = unicode(mainWindow.cb_Go_EndTime.currentText())
        # 去程開始車站
        self.Go_sStation = unicode(mainWindow.cb_Go_StartStation.currentText())
        #去程終點車站
        self.Go_eStation = unicode(mainWindow.cb_Go_EndStation.currentText())
        # 去程車種
        self.Go_Kind = unicode(mainWindow.cb_Go_Kind.currentText())
        # 去程票數
        self.Go_Num = unicode(mainWindow.cb_Go_Num.currentText())

        # 回程日期
        self.Back_Date = unicode(mainWindow.cb_Back_Date.currentText())
        # 回程開始時間
        self.Back_sTime = unicode(mainWindow.cb_Back_StartTime.currentText())
        # 回程結束時間
        self.Back_eTime = unicode(mainWindow.cb_Back_EndTime.currentText())
        # 回程開始車站
        self.Back_sStation = unicode(mainWindow.cb_Back_StartStation.currentText())
        # 回程終點車站
        self.Back_eStation = unicode(mainWindow.cb_Back_EndStation.currentText())
        # 回程車種
        self.Back_Kind = unicode(mainWindow.cb_Back_Kind.currentText())
        # 回程票數
        self.Back_Num = unicode(mainWindow.cb_Back_Num.currentText())


    def Start(self):
        pass

    # 印出所有參數 Debug用
    def PrintAllVariable(self):
        attrs = vars(self)
        print ', \n'.join("%s: %s" % item for item in attrs.items())
