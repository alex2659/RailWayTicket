import requests, os, sys, tempfile, subprocess, base64, time

"""
用來抓取速度最快的VPN
init:country參數 用來指定特定國家的VPN或不指定

members:
self.index:vpn gate CSV的國家全名或國家縮寫欄位的index
self.country:指定的國家
"""


class VPN:

    """
    初始化時 指派一個國家 可為縮寫或全名
    會依據縮寫或全名 指派index變數 用來指向array的全名或縮寫欄位
    日本 全:Japan  縮:Jp
    韓國 全:Korea Republic of  縮:KR
    墨西哥 全:Mexico  縮:MK
    美國   全:United States  縮:US
    中國   全:China  縮:CN
    .....etc
    """

    def __init__(self, country=''):

        self.country = country

        if len(country) == 0:
            self.index = -1  # 如果沒指派國家 index為-1
        elif len(country) == 2:
            self.index = 6  # 國家名稱縮寫
        elif len(country) > 2:
            self.index = 5  # 國家名稱全名
        else:
            print('請指定國家(全名或縮寫) 或不輸入，預設判斷全部資料')
            exit(1)

    #  取得最快速的VPN 回傳IP
    def getBestVPN(self):
        try:
            print("====Start to getting VPN====")
            vpn_data = requests.get('http://www.vpngate.net/api/iphone/').text.replace('\r','')
            servers = [line.split(',') for line in vpn_data.split('\n')]
            labels = servers[1]
            labels[0] = labels[0][1:]
            servers = [s for s in servers[2:] if len(s) > 1]
        except:
            print('Cannot get VPN servers data')
            exit(1)

        if self.index != -1:
            desired = [s for s in servers if self.country.lower() in s[self.index].lower()]
        else:
            desired = servers
        found = len(desired)
        print('Found ' + str(found) + ' servers for country ' + self.country
              if len(self.country) > 0
              else 'Found ' + str(found) + ' servers')
        if found == 0:
            exit(1)

        supported = [s for s in desired if len(s[-1]) > 0]
        print(str(len(supported)) + ' of these servers support OpenVPN')
        # 依照總分欄位 排序servers 取出最快的server
        winner = sorted(supported, key=lambda s: s[2], reverse=True)[0]

        print("\n== Best server ==")
        #  [:-1]是指不取最後一欄
        pairs = list(zip(labels, winner))[:-1]
        for (l, d) in pairs[:4]:
            print(l + ': ' + d)

        print(pairs[4][0] + ': ' + str(float(pairs[4][1]) / 10**6) + ' MBps')
        print("Country: " + pairs[5][1])

        print("\nLaunching VPN...")
        #  回傳IP
        return winner[1]
