# encoding: utf-8
from __future__ import print_function
import numpy as np
np.random.seed(1337)  # for reproducibility
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils
from keras import backend as K
from sklearn.preprocessing import LabelEncoder
import glob
import cv2
import re

nb_classes = 10 # 要分類的群組數 0~9共十個分類
kernel_size = (3,3) # 模型濾波器大小
input_shape = (50,50,3) # 輸入圖片大小
batch_size = 128 # 每一批有幾個圖
nb_epoch = 12 # 訓練次數

# 取得圖片和標籤
def GetData(path):
    # 取得所有圖片path
    allfile = glob.glob(path + '\*.png')
    length = len(allfile) # 圖片數量
    data = np.empty((length, 50,50,3), dtype="float32") # 用來存放圖片
    labels = [] #用來存放解答

    # 取得訓練圖片和訓練標籤(answer)
    for index, img_path in enumerate(allfile):
        image = cv2.imread(img_path)
        m = re.search(r'(\d)_\d*.png', img_path)
        label = m.group(1) # 從檔名取出圖片的解答
        arr = np.asarray(image, dtype="float32") / 255.0 #將黑白圖片轉成1,0陣列 原本是0,255
        data[index, :, :, :] = arr
        labels.append(label)
    # 將標籤轉成integers
    le = LabelEncoder()
    labels = le.fit_transform(labels)
    # 將標籤轉成獨熱編碼 one hot encoding
    labels = np_utils.to_categorical(labels, nb_classes)
    return data,labels

# 取得訓練資料
trainData,trainLabels = GetData('D:\CaptchaSingle')
# 取得測試資料
testData,testLabels = GetData('D:\CaptchaTest')

# 初始化模型
model = Sequential()
# 第一層卷積，filter大小3*3，數量32個，原始圖像大小50*50 輸出=48*48
model.add(Convolution2D(32, kernel_size[0], kernel_size[1],
                        border_mode='valid',
                        input_shape=input_shape))
model.add(Activation('relu'))
# 第二層卷積，filter大小3*3，數量32個，輸入圖像大小（50-3+1）*（50-3-1） = 48*48 輸出=46*46
model.add(Convolution2D(32, kernel_size[0], kernel_size[1]))
model.add(Activation('relu'))
# maxpooling，大小(2,2),輸入大小是46*46,stride默認是None，輸出大小是23*23
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))
# 第三層卷積，filter大小3*3，數量64個，輸入圖像大小23*23 輸出=21*21
model.add(Convolution2D(64, kernel_size[0], kernel_size[1]))
model.add(Activation('relu'))
# 第四層卷積，filter大小3*3，數量64個，輸入圖像大小21*21，輸出是18*18
model.add(Convolution2D(64, 4, 4))
model.add(Activation('relu'))
# maxpooling，大小(2,2),輸入大小是18*18,stride默認是None，輸出大小是9*9
model.add(MaxPooling2D(pool_size=(3,3)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(nb_classes))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='adadelta',
              metrics=['accuracy'])

model.fit(trainData, trainLabels, batch_size=batch_size, nb_epoch=nb_epoch,
          verbose=1
          , validation_data=(testData, testLabels)
          )
model.save_weights('model/model.h5')
score = model.evaluate(testData, testLabels, verbose=0)
print('Test score:', score[0])
print('Test accuracy:', score[1])

# ====================================================================================

#  網路抄來的預測集
# nb_class = 10
# model_path = './model/type2_model.d5'
#
# model = Sequential()
# model.add(Convolution2D(32, 1, 4, 4, border_mode='full', activation='relu'))
# model.add(Convolution2D(32, 32, 4, 4, activation='relu'))
# model.add(MaxPooling2D(poolsize=(3, 3)))
# model.add(Dropout(0.25))
# model.add(Convolution2D(64, 32, 4, 4, border_mode='full', activation='relu'))
# model.add(Convolution2D(64, 64, 4, 4, activation='relu'))
# model.add(MaxPooling2D(poolsize=(2, 2)))
# model.add(Dropout(0.25))
# model.add(Flatten())
# model.add(Dense(64 * 5 * 5, 512, activation='relu'))
# model.add(Dropout(0.5))
# model.add(Dense(512, nb_class, activation='softmax'))
# model.load_weights(model_path)
# model.compile(loss='categorical_crossentropy', optimizer='adagrad')
#
#
#
#============================================================

# mnist訓練集

# batch_size = 128
# nb_classes = 10
# nb_epoch = 12
#
# # input image dimensions
# img_rows, img_cols = 28, 28
# # number of convolutional filters to use
# nb_filters = 32
# # size of pooling area for max pooling
# pool_size = (2, 2)
# # convolution kernel size
# kernel_size = (3, 3)
#
# # the data, shuffled and split between train and test sets
# (X_train, y_train), (X_test, y_test) = mnist.load_data()
#
# if K.image_dim_ordering() == 'th':
#     X_train = X_train.reshape(X_train.shape[0], 1, img_rows, img_cols)
#     X_test = X_test.reshape(X_test.shape[0], 1, img_rows, img_cols)
#     input_shape = (1, img_rows, img_cols)
# else:
#     X_train = X_train.reshape(X_train.shape[0], img_rows, img_cols, 1)
#     X_test = X_test.reshape(X_test.shape[0], img_rows, img_cols, 1)
#     input_shape = (img_rows, img_cols, 1)
#
# X_train = X_train.astype('float32')
# X_test = X_test.astype('float32')
# X_train /= 255
# X_test /= 255
# print('X_train shape:', X_train.shape)
# print(X_train.shape[0], 'train samples')
# print(X_test.shape[0], 'test samples')
#
# # convert class vectors to binary class matrices
# print(y_train)
# Y_train = np_utils.to_categorical(y_train, nb_classes)
# Y_test = np_utils.to_categorical(y_test, nb_classes)
#
# model = Sequential()
#
# model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1],
#                         border_mode='valid',
#                         input_shape=input_shape))
# model.add(Activation('relu'))
# model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1]))
# model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=pool_size))
# model.add(Dropout(0.25))
#
# model.add(Flatten())
# model.add(Dense(128))
# model.add(Activation('relu'))
# model.add(Dropout(0.5))
# model.add(Dense(nb_classes))
# model.add(Activation('softmax'))
#
# model.compile(loss='categorical_crossentropy',
#               optimizer='adadelta',
#               metrics=['accuracy'])
#
# model.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=nb_epoch,
#           verbose=1, validation_data=(X_test, Y_test))
# score = model.evaluate(X_test, Y_test, verbose=0)
# print('Test score:', score[0])
# print('Test accuracy:', score[1])