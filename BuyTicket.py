# encoding: utf-8
import requests
from PIL import Image
from StringIO import StringIO
from PyQt4 import QtCore, QtGui

class BuyTicket:
    def __init__(self, mainWindow):
        # 身份證字號
        self.ID = mainWindow.textID.toPlainText()
        # 是否為來回票
        self.IsTwoWay = mainWindow.ckIsTwoWay.isChecked()

        # 去程日期
        self.Go_Date = self.GetComboboxValue(mainWindow.cb_Go_Date)
        # 去程開始時間
        self.Go_sTime = unicode(mainWindow.cb_Go_StartTime.currentText())
        #去程結束時間
        self.Go_eTime = unicode(mainWindow.cb_Go_EndTime.currentText())
        # 去程開始車站
        self.Go_sStation = self.GetComboboxValue(mainWindow.cb_Go_StartStation).zfill(3)
        #去程終點車站
        self.Go_eStation = self.GetComboboxValue(mainWindow.cb_Go_EndStation).zfill(3)
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
        # 回程開始車站
        self.Back_sStation = self.GetComboboxValue(mainWindow.cb_Back_StartStation).zfill(3)
        # 回程終點車站
        self.Back_eStation = self.GetComboboxValue(mainWindow.cb_Back_EndStation).zfill(3)
        # 回程車種
        self.Back_Kind = self.GetComboboxValue(mainWindow.cb_Back_Kind)
        # 回程票數
        self.Back_Num = unicode(mainWindow.cb_Back_Num.currentText())


    def Start(self):
        url = 'http://railway.hinet.net/check_ctkind2.jsp'
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'Referer': 'http://railway.hinet.net/ctkind2.htm'
                  }
        data = {"person_id": self.ID,#身份證字號
                "from_station": self.Go_sStation,#起站
                "to_station":self.Go_eStation,#迄站
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
                "returnTicket":"0" #似乎是CSRF token
               }
        s = requests.Session()
        result = s.post(url,data=data, headers=headers)
        result.encoding = 'big5'
        # print(result.text)
        # 取得驗證碼圖片
        req = s.get('http://railway.hinet.net/ImageOut.jsp')
        i = Image.open(StringIO(req.content))
        i.save(r'C:\Users\vi000\Desktop\123.jpg')
        var = raw_input("請輸入驗證碼: ")
        print('您輸入的驗證碼是'+ var)

        #=========================
        # 輸入驗證碼
        # ========================
        url = 'http://railway.hinet.net/ctkind2_result.jsp'
        # 將query string加上驗證碼
        data.update({'randInput':var})

        result = s.get(url, params= data, headers=headers)
        result.encoding = 'big5-hkscs'
        print(result.text)



    # 印出所有參數 Debug用
    def PrintAllVariable(self):
        attrs = vars(self)
        print ', \n'.join("%s: %s" % item for item in attrs.items())

    # 取得combobox的value
    def GetComboboxValue(self, cb):
        return str(cb.itemData(cb.currentIndex()).toPyObject())