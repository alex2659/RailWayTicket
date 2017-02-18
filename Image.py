from PIL import Image, ImageEnhance
import cv2

class Image:
    #  傳入圖片所在目錄和檔名
    def __init__(self, Path,ImgName):
        #  儲存檔名
        self.imageName = ImgName
        #  用來儲放分割後的圖片
        self.arr = []
        #  將圖片做灰階
        self.im = cv2.imread(Path + "\\" + ImgName, flags=cv2.IMREAD_GRAYSCALE)

    #  濾背景色
    def threshold(self):
        # 115 是 threshold，越高濾掉越多
        # 255 是當你將 method 設為 THRESH_BINARY_INV 後，高於 threshold 要設定的顏色
        self.retval, self.im = cv2.threshold(self.im, 115, 255, cv2.THRESH_BINARY_INV)

    #  去除雜點
    def removeNoise(self):
        for i in range(len(self.im)):
            for j in range(len(self.im[i])):
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

    #  切割圖片
    def splitImg(self):
        _, contours, hierarchy = cv2.findContours(self.im.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
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
                        # cv2.imshow(self.imageName, self.im[y: y + h, x: x + w])
                        # cv2.waitKey()

            except IndexError:
                pass

    #  圖片轉正
    def positiveImg(self):
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

                for i in range(r):
                    for j in range(c):
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

            #  cv2.imwrite('tmp/' + str(index) + '.png', thresh)
            #  cv2.imshow(self.imageName, thresh)
            #  cv2.waitKey()

    #  將圖片顯示出來
    def showImg(self,img):

        if img is None:
            img = self.im

        cv2.imshow(self.imageName, img)
        cv2.namedWindow(self.imageName, cv2.WINDOW_NORMAL)
        #  調整視窗 讓標題列顯示出來
        cv2.resizeWindow(self.imageName, 250, 60)
        cv2.waitKey()
