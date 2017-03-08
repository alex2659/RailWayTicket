# encoding: utf-8
from Image import Image
import requests
import kerasInitModel
import numpy as np

letters = list('0123456789')

model = kerasInitModel.LoadModel()
model.load_weights("model/model.h5")
for i in range(10):
    req = requests.get('http://railway.hinet.net/ImageOut.jsp')
    x = Image(req.content)
    imgs = x.StartProcess()

    data = np.empty((len(imgs), 50,50,3), dtype="float32")
    for index,img in enumerate(imgs):
        arr = np.asarray(img, dtype="float32") / 255.0  # 將黑白圖片轉成1,0陣列 原本是0,255
        data[index, :, :, :] = arr

    classes = model.predict_classes(data)
    result = []
    for c in classes:
        result.append(letters[c])
    print(''.join(result).upper())

