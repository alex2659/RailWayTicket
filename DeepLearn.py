from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD
from keras.datasets import mnist
import numpy

model = Sequential()
model.add(Dense(784, 500, init='glorot_uniform')) # 輸入層，28*28=784
model.add(Activation('tanh')) # 激活函數是tanh
model.add(Dropout(0.5)) # 採用50%的dropout

model.add(Dense(500, 500, init='glorot_uniform')) # 隱層節點500個
model.add(Activation('tanh'))
model.add(Dropout(0.5))

model.add(Dense(500, 10, init='glorot_uniform')) # 輸出結果是10個類別，所以維度是10
model.add(Activation('softmax')) # 最後一層用softmax

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True) # 設定學習率（lr）等參數
model.compile(loss='categorical_crossentropy', optimizer=sgd, class_mode='categorical') # 使用交叉熵作為loss函數

(X_train, y_train), (X_test, y_test) = mnist.load_data() # 使用Keras自帶的mnist工具讀取數據（第一次需要聯網）

X_train = X_train.reshape(X_train.shape[0], X_train.shape[1] * X_train.shape[2]) # 由於mist的輸入數據維度是(num, 28, 28)，這裡需要把後面的維度直接拼起來變成784維
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1] * X_test.shape[2])
Y_train = (numpy.arange(10) == y_train[:, None]).astype(int) # 參考上一篇文章，這裡需要把index轉換成一個one hot的矩陣
Y_test = (numpy.arange(10) == y_test[:, None]).astype(int)

# 開始訓練，這裡參數比較多。batch_size就是batch_size，nb_epoch就是最多迭代的次數， shuffle就是是否把數據隨機打亂之後再進行訓練
# verbose是屏顯模式，官方這麼說的：verbose: 0 for no logging to stdout, 1 for progress bar logging, 2 for one log line per epoch.
# 就是說0是不屏顯，1是顯示一個進度條，2是每個epoch都顯示一行數據
# show_accuracy就是顯示每次迭代後的正確率
# validation_split就是拿出百分之多少用來做交叉驗證
model.fit(X_train, Y_train, batch_size=200, nb_epoch=100, shuffle=True, verbose=1, show_accuracy=True, validation_split=0.3)
print('test set')
model.evaluate(X_test, Y_test, batch_size=200, show_accuracy=True, verbose=1)