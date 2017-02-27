# encoding: utf-8
import requests
from PIL import Image
from PyQt4 import QtCore, QtGui
from StringIO import StringIO
import re

class BuyTicket:
    def __init__(self, mainWindow):

        self.mainWindow = mainWindow
        # 身份證字號
        self.ID = str(mainWindow.textID.text())
        # 是否為來回票
        self.IsTwoWay = mainWindow.BackLayout.isChecked()
        # 去程開始車站
        self.sStation = self.GetComboboxValue(mainWindow.cb_StartStation).zfill(3)
        #去程終點車站
        self.eStation = self.GetComboboxValue(mainWindow.cb_EndStation).zfill(3)

        # 去程日期
        self.Go_Date = self.GetComboboxValue(mainWindow.cb_Go_Date)
        # 去程開始時間
        self.Go_sTime = unicode(mainWindow.cb_Go_StartTime.currentText())
        #去程結束時間
        self.Go_eTime = unicode(mainWindow.cb_Go_EndTime.currentText())

        # 去程車種
        self.Go_Kind = self.GetComboboxValue(mainWindow.cb_Go_Kind)
        # 去程票數
        self.Go_Num = unicode(mainWindow.cb_Go_Num.currentText())

        # 回程日期
        self.Back_Date = self.GetComboboxValue(mainWindow.cb_Back_Date)
        # 回程開始時間
        self.Back_sTime = unicode(mainWindow.cb_Back_StartTime.currentText())
        # 回程結束時間
        self.Back_eTime = unicode(mainWindow.cb_Back_EndTime.currentText())
        # 回程車種
        self.Back_Kind = self.GetComboboxValue(mainWindow.cb_Back_Kind)
        # 回程票數
        self.Back_Num = unicode(mainWindow.cb_Back_Num.currentText())


    def Start(self):
        # self.PrintAllVariable()
        # ==================
        # 輸入基本資料頁
        # ==================
        url = 'http://railway.hinet.net/check_ctkind2.jsp'
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'Referer': 'http://railway.hinet.net/ctkind2.htm'
                  }
        # # 取得post的參數
        data = self.GetQueryData()
        s = requests.Session()
        result = s.post(url,data=data, headers=headers)
        result.encoding = 'big5'
        # print(result.text)

        # =====================
        # 填寫驗證碼頁面
        # =====================
        # 取得驗證碼圖片
        req = s.get('http://railway.hinet.net/ImageOut.jsp')

        im = Image.open(StringIO(req.content)).convert('RGB')
        io = StringIO()
        im.save(io, format='png')
        qimg = QtGui.QImage.fromData(io.getvalue())
        self.mainWindow.captchaPic.setPixmap(QtGui.QPixmap(qimg))
        QtGui.QApplication.processEvents()

        num, ok = QtGui.QInputDialog.getText(self.mainWindow, u"驗證碼", u"請輸入驗證碼")
        self.mainWindow.logMsg('驗證碼:'+num)
        if ok:
            # ===============================
            # 來回票訂票結果
            # ===============================

            url = 'http://railway.hinet.net/order_kind1.jsp'
            # 去程訂票結果
            data = self.GetQueryData(type=2, returnTicket=1, randInput=num)
            # print(data)
            result = s.get(url, params= data, headers=headers)
            result.encoding = 'big5-hkscs'
            #  過濾出結果頁的html訊息
            GoreturnMsg = self.htmlRegexMatchResult(result.text)
            self.mainWindow.Go_resultMsg.setText(unicode(GoreturnMsg,"utf-8"))
            self.mainWindow.logMsg(result.text)
            self.mainWindow.logMsg('====================================\n')
            #  回程訂票結果
            data2 = self.GetQueryData(type=2, returnTicket=2, randInput=num)
            result = s.get(url, params=data2, headers=headers)
            result.encoding = 'big5-hkscs'
            self.mainWindow.logMsg(result.text)
            #  過濾出結果頁的html訊息
            BackreturnMsg = self.htmlRegexMatchResult(result.text)
            self.mainWindow.Back_resultMsg.setText(unicode(BackreturnMsg,"utf-8"))


    # 印出所有參數 Debug用
    def PrintAllVariable(self):
        attrs = vars(self)
        self.mainWindow.logMsg(', \n'.join("%s: %s" % item for item in attrs.items()))

    # 取得combobox的value
    def GetComboboxValue(self, cb):
        return str(cb.itemData(cb.currentIndex()).toPyObject())

    # 傳回post或get需要的參數
    # type 1:訂來回票 包括去回程的參數 第一個頁面用的
    #      2:result頁裡的iframe用的 依據returnTicket判斷是單程、回程、去程  1:去程 2:回程 0:單程
    def GetQueryData(self,type=1,returnTicket=0,randInput=None):
        data = {}
        if type == 1:
            data = {"person_id": self.ID,#身份證字號
                    "from_station": self.sStation,#起站
                    "to_station":self.eStation,#迄站
                    "getin_date":self.Go_Date, #去程乘車日期
                    "getin_date2":self.Back_Date,#回程乘車日期
                    "order_qty_str":self.Go_Num,#去程訂票張數
                    "order_qty_str2":self.Back_Num,#回程訂票張數
                    "train_type":self.Go_Kind,#去程車種
                    "train_type2":self.Back_Kind,#回程車種
                    "getin_start_dtime":self.Go_sTime,#去程起始時間
                    "getin_start_dtime2":self.Back_sTime,#回程起始時間
                    "getin_end_dtime":self.Go_eTime,#去程截止時間
                    "getin_end_dtime2":self.Back_eTime,#回程截止時間
                    "returnTicket": returnTicket
                   }
        elif type == 2:
            data = {"person_id": self.ID,  # 身份證字號
                    "from_station": self.sStation,  # 起站
                    "to_station": self.eStation,  # 迄站
                    "getin_date": self.Go_Date if returnTicket is not 2 else self.Back_Date,  # 去程乘車日期
                    "order_qty_str": self.Go_Num if returnTicket is not 2 else self.Back_Num,  # 去程訂票張數
                    "train_type": self.Go_Kind if returnTicket is not 2 else self.Back_Kind,  # 去程車種
                    "getin_start_dtime": self.Go_sTime if returnTicket is not 2 else self.Back_sTime,  # 去程起始時間
                    "getin_end_dtime": self.Go_eTime if returnTicket is not 2 else self.Back_eTime,  # 去程截止時間
                    "returnTicket": returnTicket,
                    "randInput": randInput
                    }
        # 避免request在get時會將網址encode
        strdata = "&".join("%s=%s" % (k, v) for k, v in data.items())
        return strdata
    # 輸入結果頁面的html 回傳result message
    def htmlRegexMatchResult(self,html):
        if html.find(u"亂數號碼錯誤") > -1:
            result = "驗證碼錯誤"
        elif html.find(u"身分證字號錯誤") > -1:
            result = "身份證字號錯誤"
        elif html.find(u"此期間訂票額滿") > -1:
            result = "此期間訂票額滿，\n或無指定條件之車次"
        elif html.find(u"該車種已訂票額滿") > -1:
            result = "【該時段、該車種已訂票額滿】\n─ 請改訂其他時段、車種乘車票"
        elif html.find(u'訂票日期錯誤或內容格式錯誤') > -1:
            result = "訂票日期錯誤或內容格式錯誤"
        elif html.find(u"您的車票已訂到") > -1:
            regex = r"<span id='spanOrderCode'[^>]*>(?P<code>\d*).*車次：</span> <span class='hv1 blue01 bold01'>(?P<trainNumber>\d*).*車種：</span> <span class='hv1 blue01 bold01'>(?P<kind>[自強|莒光|復興]*)"
            # p = re.compile(regex)
            try:
                html = html.decode('utf-8')
            except:
                pass
            m = re.search(regex.decode('utf-8'), html)
            result = str.format("您的車票已訂到\n電腦代碼:{} \n車次:{}  車種:{}",
                                m.group('code').encode('utf-8'), m.group('trainNumber').encode('utf-8'),
                                m.group('kind').encode('utf-8'))
        else:
            result = "查無回傳資料"

        return result
