# encoding: utf-8
from PIL import Image, ImageEnhance
import cv2
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.font_manager import FontProperties
import collections
import os, random, sys
import numpy as np

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
        self.im = cv2.imread(Path + "\\" + ImgName, cv2.IMREAD_GRAYSCALE)
        self.dicImg.update({"轉灰階": self.im.copy()})


    #  閾值化
    def threshold(self):
        # 115 是 threshold，越高濾掉越多
        # 255 是當你將 method 設為 THRESH_BINARY_INV 後，高於 threshold 要設定的顏色
        self.retval, self.im = cv2.threshold(self.im, 50, 255, cv2.THRESH_BINARY_INV)
        self.dicImg.update({"閾值化": self.im.copy()})

    #  去噪
    def removeNoise(self):
        for i in xrange(len(self.im)):
            for j in xrange(len(self.im[i])):
                if self.im[i][j] == 255:
                    count = 0
                    for k in range(-2, 3):
                        for l in range(-2, 3):
                            try:
                                if self.im[i + k][j + l] == 255:
                                    count += 1
                            except IndexError:
                                pass
                    # 這裡 threshold 設 4，當週遭小於 4 個點的話視為雜點
                    if count <= 4:
                        self.im[i][j] = 0

        self.im = cv2.dilate(self.im, (2, 2), iterations=1)
        self.dicImg.update({"去噪": self.im.copy()})

    #  色調分離
    def posterization(self):
        n = 4  # Number of levels of quantization

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

    #  干擾線檢測
    def lineDetect(self):
        laplacian = cv2.Laplacian(self.im, cv2.CV_8UC1)  # Laplacian Edge Detection
        minLineLength = 1
        maxLineGap = 1
        lines = cv2.HoughLinesP(laplacian, 1, np.pi / 180, 1, minLineLength, maxLineGap)
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(self.im, (x1, y1), (x2, y2), (255,255,255))
        self.dicImg.update({"干擾線檢測": self.im.copy()})

                #  切割圖片
    def splitImg(self):
        contours, hierarchy = cv2.findContours(self.im.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #  按照X軸位置對圖片進行排序 確保我們從左到右讀取數字
        cnts = sorted([(c, cv2.boundingRect(c)[0]) for c in contours], key=lambda x: x[1])

        for index, (c, _) in enumerate(cnts):
            (x, y, w, h) = cv2.boundingRect(c)

            try:
                # 只將寬高大於 8 視為數字留存
                if w > 8 and h > 8:
                    add = True
                    for i in range(0, len(self.arr)):
                        # 這邊是要防止如 0、9 等，可能會偵測出兩個點，當兩點過於接近需忽略
                        if abs(cnts[index][1] - self.arr[i][0]) <= 3:
                            add = False
                            break
                    if add:
                        self.arr.append((x, y, w, h))

            except IndexError:
                pass
        Imgarr = [self.im[y: y + h, x: x + w] for x, y, w, h in self.arr]
        self.dicImg.update({"分割圖片": Imgarr})
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
            # 第一列 原始驗證碼的圖片
            ax1 = fig.add_subplot(gs[0, :6])
            originImg = cv2.imread(self.Path + "\\" + self.imageName)
            ax1.imshow(originImg, interpolation='nearest')
            ax1.set_title('原始驗證碼', fontproperties=self.font)

            # 依序列出dict物件裡的圖片
            for index, key in enumerate(self.dicImg):
                #  如果不是list物件 就是圖片 可以呼叫imshow
                if not isinstance(self.dicImg[key], list):
                    ax = fig.add_subplot(gs[index+1, :6])
                    ax.imshow(self.dicImg[key], interpolation='nearest')
                    ax.set_title(key, fontproperties=self.font)
                else:
                    for i, img in enumerate(self.dicImg[key]):
                        ax = fig.add_subplot(gs[index+1, i])
                        ax.imshow(img, interpolation='nearest')

            plt.tight_layout()
            plt.show()
        else:
            print '圖片數字陣列為空'


if __name__ == '__main__':
    for i in range(10):
        #  取得驗證碼資料夾裡 隨機一個驗證碼的路徑
        x = Image(r"D:\RailWayCapcha", random.choice(os.listdir(r"D:\RailWayCapcha")))
        x.posterization()
        # x.lineDetect()
        x.removeNoise()
        # x.threshold()
        # x.splitImg()
        # x.positiveImg()
        x.showImgEveryStep()
