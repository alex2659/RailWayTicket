# encoding: utf-8
from VPN import VPN
from Image import Image
import os, random
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

__CaptchaPath__ = r"D:\RailWayCapcha"
# 取得VPN
# a = VPN()
#
# b= a.ConnectVPN()

for i in range(10):
    #  取得驗證碼資料夾裡 隨機一個驗證碼的路徑
    x = Image(__CaptchaPath__, random.choice(os.listdir(__CaptchaPath__)))
    x.threshold()
    x.removeNoise()
    x.splitImg()
    x.positiveImg()