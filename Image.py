# encoding: utf-8
from PIL import Image, ImageEnhance
import cv2
import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.font_manager import FontProperties
import collections
import os, random, sys
import numpy as np
from scipy import ndimage

reload(sys)
sys.setdefaultencoding("utf-8")

class Image:

    #  傳入圖片所在目錄和檔名
    def __init__(self, Path,ImgName):
        #  設置matplotlib中文字體
        self.font = FontProperties(fname=r"c:\windows\fonts\SimSun.ttc", size=14)
        #  儲存檔名
        self.imageName = ImgName
        #  儲存路徑
        self.Path = Path
        #  用來儲放分割後的圖片邊緣坐標(x,y,w,h)
        self.arr = []
        #  將每個階段做的圖存起來 用來debug
        self.dicImg = collections.OrderedDict()
        #  將圖片做灰階
        self.im = cv2.imread(Path + "\\" + ImgName)
        self.dicImg.update({"原始驗證碼": self.im.copy()})


    #  閾值化
    def threshold(self):
        # 115 是 threshold，越高濾掉越多
        # 255 是當你將 method 設為 THRESH_BINARY_INV 後，高於 threshold 要設定的顏色
        # 反轉黑白 以利輪廓識別
        gray_image = cv2.cvtColor(self.im, cv2.COLOR_BGR2GRAY)
        self.retval, self.im = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)
        # 存檔
        #cv2.imwrite("D:\\CaptchaRaw\\" + self.imageName + 'Threshold.png', self.im)
        self.dicImg.update({"閾值化": self.im.copy()})

    #  去噪
    def removeNoise(self):
        for i in xrange(len(self.im)):
            for j in xrange(len(self.im[i])):
                if self.CheckPixelIsBlack(self.im[i][j]):
                    count = 0
                    for k in range(-2, 3):
                        for l in range(-2, 3):
                            try:
                                if self.CheckPixelIsBlack(self.im[i + k][j + l]):
                                    count += 1
                            except IndexError:
                                pass
                    # 這裡 threshold 設 4，當週遭小於 4 個點的話視為雜點
                    if count <= 3:
                        self.im[i][j] = 0

        self.im = cv2.dilate(self.im, (2, 2), iterations=1)
        self.dicImg.update({"去噪": self.im.copy()})

    #  色調分離
    def posterization(self,levels=3):
        n = levels  # Number of levels of quantization

        indices = np.arange(0, 256)  # List of all colors

        divider = np.linspace(0, 255, n + 1)[1]  # we get a divider

        quantiz = np.int0(np.linspace(0, 255, n))  # we get quantization colors

        color_levels = np.clip(np.int0(indices / divider), 0, n - 1)  # color levels 0,1,2..

        palette = quantiz[color_levels]  # Creating the palette

        im2 = palette[self.im]  # Applying palette on image

        self.im = cv2.convertScaleAbs(im2)  # Converting image back to uint8
        #  存檔
        #cv2.imwrite("D:\\CaptchaRaw\\" + self.imageName + '.png', self.im)
        self.dicImg.update({"色調分離": self.im.copy()})

    #  干擾線檢測  (只檢查寬度為2pxiel的直線&橫線)
    def removeBlackLines(self):
        chop = 4  #  線段長度大於chop 才判斷為干擾線
        lineColor = 255  #  將線段設定為黑或白色 255:白 0:黑
        (height, width,_) = self.im.shape
        #  loop 每一個pixel
        for i in xrange(height):
            for j in xrange(width):
                #  如果是黑色點 開始計算線段長度
                if self.CheckPixelIsBlack(self.im[i][j]):
                    countWidth = 0
                    countWidth2= 0
                    #  移除橫線 在每個像素找尋橫向的像素 如果<threshold 就count+1
                    for c in range(j, width):
                        try:
                            if self.CheckPixelIsBlack(self.im[i][c]) and self.CheckPixelIsWhite(self.im[i+1][c]):
                                countWidth += 1
                            else:
                                break
                        # 檢查下方有沒有直線
                            if self.CheckPixelIsBlack(self.im[i-1][c]) and self.CheckPixelIsWhite(self.im[i-2][c]):
                                countWidth2+=1
                            else:
                                break
                        except:
                            pass

                    #  如果大於指定長度 代表是線段
                    if countWidth >= chop and countWidth >= chop:
                        for c in range(countWidth):
                            try:
                                #  如果此點的上下兩個點是白的 代表不在數字裡 可以移除
                                if self.CheckPixelIsWhite(self.im[i+1, j+c]) and self.CheckPixelIsWhite(self.im[i-2, j+c]):
                                    self.im[i, j + c] =lineColor
                                    self.im[i-1, j + c] = lineColor

                            except IndexError:
                                self.im[i, j + c] = lineColor
                                self.im[i - 1, j + c] = lineColor

                    j += countWidth
        #  loop 每一個pixel
        for j in xrange(width):
            for i in xrange(height):
                #  如果是黑色點 開始計算線段長度
                if self.CheckPixelIsBlack(self.im[i][j]):
                    countHeight = 0
                    countHeight2 = 0
                    #  移除直線
                    for c in range(i, height):
                        try:
                            if self.CheckPixelIsBlack(self.im[c][j]) and self.CheckPixelIsWhite(self.im[c][j-1]):
                                countHeight += 1
                            else:
                                break
                        # 檢查右方有沒有直線
                            if self.CheckPixelIsBlack(self.im[c][j+1]) and self.CheckPixelIsWhite(self.im[c][j+2]):
                                countHeight2 += 1
                            else:
                                break
                        except:
                            pass
                    if countHeight >= chop and countHeight2 >= chop:
                        for c in range(countHeight):
                            try:
                                if self.CheckPixelIsWhite(self.im[i + c, j + 2]) and self.CheckPixelIsWhite(self.im[i + c, j - 1]):
                                    self.im[i + c, j] =lineColor
                                    self.im[i + c, j+1] =lineColor
                            except IndexError:
                                    self.im[i + c, j] = lineColor
                                    self.im[i + c, j+1] = lineColor

                    i += countHeight
        # 存檔
        # cv2.imwrite("D:\\CaptchaRaw\\" + self.imageName + '.png', self.im)
        self.dicImg.update({"干擾線檢測": self.im.copy()})

    #  傳入RGB的pixel 判斷是否是黑點  (色調分離後 干擾線的RGB會變(127,127,127))
    def CheckPixelIsBlack(self, pixel, min= 127,max= 127):
        return self.CheckPixelColor(pixel,min,max)
    #  傳入RGB的pixel 判斷是否是白點
    def CheckPixelIsWhite(self, pixel, min= 160,max= 255):
        return self.CheckPixelColor(pixel, min, max)

    def CheckPixelColor(self,pixel, min ,max ):
        if  min<= pixel[0] <= max and min<= pixel[1] <= max and min <= pixel[2] <= max:
            return True
        else:
            return False

    def medianBlur(self):
        self.im = cv2.medianBlur(self.im, 3)
        self.dicImg.update({"中值模糊": self.im})

    # 閉運算
    def mop_close(self):
        # 定義結構元素
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

        # 閉運算
        self.im = cv2.morphologyEx(self.im, cv2.MORPH_CLOSE, kernel)

        # 顯示腐蝕後的圖像
        self.dicImg.update({"閉運算": self.im.copy()})
    # 垂直投影
    def horShadow(self):
        # 創建一個空白圖片(img.shape[0]為height,img.shape[1]為width)
        paintx = np.zeros(self.im.shape, np.uint8)
        # 將新圖像數組中的所有通道元素的值都設置為0
        cv2.cv.Zero(cv2.cv.fromarray(paintx))

        # 創建width長度都為0的數組 此陣列會存放每一column的黑點的個數
        num_of_valid_pix = [0] * self.im.shape[1]
        # 對每一行計算投影值
        for x in range(self.im.shape[1]):
            for y in range(self.im.shape[0]):
                t = cv2.cv.Get2D(cv2.cv.fromarray(self.im), y, x)
                if t[0] == 255: #  如果是黑色點就count+1
                    num_of_valid_pix[x] += 1

        # 繪製垂直投影圖
        for x in range(self.im.shape[1]):
            for y in range(num_of_valid_pix[x]):
                # 把為255的像素變成黑

                cv2.cv.Set2D(cv2.cv.fromarray(paintx), y, x, (255, 255, 255))
        self.dicImg.update({"投影": paintx})

        # ==============分割圖片=======================
        # letter_col_id = []  # @letter_col_id儲存每個數字所在的欄位的index
        # i = 0
        # # loop num_of_valid_pix陣列 如果黑色點數量>0 就將index加到letter_id 代表文字所在的index
        # while i in range(len(num_of_valid_pix)):
        #     letter_id = []  # @letter_id 儲存每個數字的欄位數
        #     # letter feature: there must be blank cols that contains no valid pixels in the column
        #     while num_of_valid_pix[i] != 0:
        #         letter_id.append(i)
        #         i += 1
        #     if letter_id:
        #         letter_col_id.append(letter_id)
        #     i += 1
        # # 確認每個字的寬度
        # numofLetters = len(letter_col_id)
        # # this part is dealing with the saparated
        # height = self.im.shape[0]
        # imgarr = []
        # print(numofLetters)
        # print('=============')
        # for j in range(numofLetters):
        #     colsForLetter = len(letter_col_id[j])
        #     print(len(letter_col_id[j]))
        #     if colsForLetter in range(5, 14):
        #         newimg = np.zeros((height,len(letter_col_id[j])), np.uint8)
        #         for y in range(height):
        #             # rowbuffer = []
        #             i = 0
        #             for x in letter_col_id[j]:
        #                 newimg.itemset((y, i), 0)
        #                 i += 1
        #                 imgarr.append(newimg)


        # cv2.line(self.im, (20, 0), (20, 60), (255, 255, 255))
        # self.im = self.im[:,:30] 切割圖片 讓圖片width減短

        # =====================================================

        # self.dicImg.update({"切割": imgarr})


    #  切割圖片
    def splitImg(self):
        # self.im = cv2.cvtColor(self.im , cv2.COLOR_BGR2GRAY)
        contours, hierarchy = cv2.findContours(self.im.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #  按照X軸位置對圖片進行排序 確保我們從左到右讀取數字
        cnts = sorted([(c, cv2.boundingRect(c)[0]) for c in contours], key=lambda x: x[1])
        # 畫出輪廓，-1,表示所有輪廓，畫筆顏色為(0, 255, 0)，即Green，粗細為3
        cv2.drawContours(self.im, contours, -1, (0, 100, 0), 1)
        self.dicImg.update({"找出輪廓": self.im})
        # for index, (c, _) in enumerate(cnts):
        #     (x, y, w, h) = cv2.boundingRect(c)
        #     self.arr.append((x, y, w, h))
            # try:
            #     # 只將寬高大於 8 視為數字留存
            #     if w > 8 and h > 8:
            #         add = True
            #         for i in range(0, len(self.arr)):
            #             # 這邊是要防止如 0、9 等，可能會偵測出兩個點，當兩點過於接近需忽略
            #             if abs(cnts[index][1] - self.arr[i][0]) <= 3:
            #                 add = False
            #                 break
            #         if add:
            #             self.arr.append((x, y, w, h))
            #
            # except IndexError:
            #     pass
        # Imgarr = [self.im[y: y + h, x: x + w] for x, y, w, h in self.arr]

        # self.showImgArray(Imgarr)


    #  圖片轉正
    def positiveImg(self):

        imgarr = []
        for index, (x, y, w, h) in enumerate(self.arr):
            roi = self.im[y: y + h, x: x + w]
            thresh = roi.copy()

            angle = 0
            smallest = 999
            row, col = thresh.shape

            for ang in range(-60, 61):
                M = cv2.getRotationMatrix2D((col / 2, row / 2), ang, 1)
                t = cv2.warpAffine(thresh.copy(), M, (col, row))

                r, c = t.shape
                right = 0
                left = 999

                for i in xrange(r):
                    for j in xrange(c):
                        if t[i][j] == 255 and left > j:
                            left = j
                        if t[i][j] == 255 and right < j:
                            right = j

                if abs(right - left) <= smallest:
                    smallest = abs(right - left)
                    angle = ang

            M = cv2.getRotationMatrix2D((col / 2, row / 2), angle, 1)
            thresh = cv2.warpAffine(thresh, M, (col, row))
            # resize 成相同大小以利後續辨識
            thresh = cv2.resize(thresh, (50, 50))
            imgarr.append(thresh)
        self.dicImg.update({"轉正": imgarr})

    #  將圖片顯示出來
    def showImg(self, img=None):

        if img is None:
            img = self.im

        cv2.imshow(self.imageName, img)
        cv2.namedWindow(self.imageName, cv2.WINDOW_NORMAL)
        #  調整視窗 讓標題列顯示出來
        cv2.resizeWindow(self.imageName, 250, 60)
        cv2.waitKey()


    #  將多個圖片顯示在一個figure
    def showImgEveryStep(self):
        diclength = len(self.dicImg)
        if diclength > 0:
            fig = plt.figure(figsize=(10, 10))
            gs = gridspec.GridSpec(diclength+1, 6)

            # 依序列出dict物件裡的圖片
            for index, key in enumerate(self.dicImg):
                #  如果不是list物件 就是圖片 可以呼叫imshow
                if not isinstance(self.dicImg[key], list):
                    ax = fig.add_subplot(gs[index, :6])
                    ax.imshow(self.dicImg[key], interpolation='nearest')
                    ax.set_title(key, fontproperties=self.font)
                else:
                    try:
                        for i, img in enumerate(self.dicImg[key]):
                            ax = fig.add_subplot(gs[index, i])
                            ax.imshow(img, interpolation='nearest')
                    except IndexError:
                        pass

            plt.tight_layout()
            plt.show()
        else:
            print '圖片數字陣列為空'
    #  存檔
    def SaveImg(self):

        cv2.imwrite("D:\\CaptchaRaw\\" + self.imageName + '.png', self.im)

# 目前步驟 1.色調分離 濾掉背景色 2.移除黑線
if __name__ == '__main__':
    for i in range(10):
        #  取得驗證碼資料夾裡 隨機一個驗證碼的路徑
        x = Image(r"D:\RailWayCapcha", random.choice(os.listdir(r"D:\RailWayCapcha")))
        x.posterization()
        x.mop_close()
        # x.SaveImg()
        x.removeBlackLines()
        # x.medianBlur()
        x.threshold()
        # x.horShadow()
        # x.removeNoise()
        x.splitImg()
        # x.positiveImg()
        x.showImgEveryStep()
