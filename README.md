

如何安裝
-----------------------------
step 1.
下載安裝OpenVPN 選擇Installer, Windows Vista and later
https://openvpn.net/index.php/open-source/downloads.html

並且到OpenVPN的安裝目錄   舉例 E:\OpenVPN\bin
右鍵點擊openvpn.exe ->內容 ->相容性頁籤 ->將"以系統管理員的身份執行此程式"勾選

Step2.
安裝Anaconda3  python3.x版本

Step3.

windows 下安裝 opencv
從 opencv 3.x 開始，opencv 其實就已經可以支持 python 3 了，但是官方給出的編譯版本還只支持 python 2.7 ，
所以如果想要給 python 3 安裝 opencv 模塊，我們就得自己編譯源碼，
但是這個過程相對繁瑣，還容易出錯。這裡提供一個非官方的下載地址：

http://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv

該網站提供了眾多在 windows 平台下的第三方已編譯 python 包擴展下載。
進入網頁，選擇一個合適自己的版本 opencv_python-xxx.whl 下載。
比如，我使用 python 3.5 ，所以選擇下載 ：
opencv_python-3.1.0+contrib_opencl-cp35-cp35m-win_amd64.whl
amd64 適用所有 64-bit 的操作系統。
下載好之後，使用 CMD 進入 .whl 文件所在目錄，執行（以 opencv_python-3.1.0+contrib_opencl-cp35-cp35m-win_amd64.whl 為例）：
pip install opencv_python-3.1.0+contrib_opencl-cp35-cp35m-win_amd64.whl 進行安裝。
如果你想要自己編譯安裝，可以參考這篇：
http://docs.opencv.org/3.1.0/d5/de5/tutorial_py_setup_in_windows.html

Step4.
安裝Keras

