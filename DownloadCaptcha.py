from urllib.request import urlretrieve
import os
import uuid
import time

# 抓取圖片張數
picNum = 1000
# 驗證碼的圖片路徑
url = "http://railway.hinet.net/ImageOut.jsp"
# 存檔路徑
save_path = "D:\\RailWayCapcha"
# 剩餘錯誤次數
remaining_download_tries = 30

for i in range(picNum):
    # 如果剩餘錯誤次數大於0 就抓取圖片
    if remaining_download_tries > 0:
        try:
            # 給定圖片存放名稱
            fileName = save_path + "\\Sample" + str(uuid.uuid4()) + ".jpg"
            # 文件名是否存在
            if not os.path.exists(fileName):
                urlretrieve(url, fileName)
                print("第" + str(i) + "張圖片己下載")
                # 設定延遲
                time.sleep(1)

        except Exception as e:
            remaining_download_tries = remaining_download_tries - 1
            print("連線錯誤 正重新連線 剩餘重試次數" + str(remaining_download_tries) + "錯誤訊息:"+str(e))
            time.sleep(5)
            continue
    else:
        print("錯誤次數己達上限 任務停止")

print("任務完成")









