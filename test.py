#-*-coding:utf-8 -*-
import re
#
#
# html = """
# <p><font class="orange02"><strong>去程結果:您的車票已訂到</strong></font></p>
#
# 	<p class="gray01"><span class="hd1">身分證字號：</span> <span id="spanPid" class="hv1 blue01 bold01">R124190739</span></p>
# 	<p class="gray01">
# 		<span class="hd1">電腦代碼：</span> <span id="spanOrderCode" class="hv1 red02 text_14p bold01">747218</span>
# 		<span class="blue01 bold01">
#
# 		</span>
# 	</p>
# 	<p class="gray01">
# 		<span class="hd1">車次：</span> <span class="hv1 blue01 bold01">302  </span>
# 		<span class="hd1">車種：</span> <span class="hv1 blue01 bold01">
# 		自強號
# 		</span>
# 	</p>
# 	<p class="gray01"><span class="hd1">乘車時刻：</span> <span class="hv1 blue01 bold01">2017/03/13 06:10</span></p>
# 	<p class="gray01">
# 		<span class="hd1">起站：</span> <span class="hv1 blue01 bold01">台東  </span>
# 		<span class="hd1">到站：</span> <span class="hv1 blue01 bold01">新左營</span>
# 		<span class="hd1">張數：</span> <span class="hv1 blue01 bold01">1</span>
# 	</p>
# """
# # 找出html裡的文字 並存在group裡 id:身份證字號 code:電腦代碼 trainNumber:車次 kind:車種
# regex = r"<span id=\"spanOrderCode\" [^>]*>(?P<code>\d*)[^車次]*車次：</span> <span[^>]*>(?P<trainNumber>\d*)[^車]*車種：</span> <span[^>]*>\s*(?P<kind>[自強|莒光|復興]*)"
# # p = re.compile(regex)
# m = re.search(regex.decode('utf-8'),html.decode('utf-8'),re.MULTILINE)
# print(m.groups())
# result = str.format("電腦代碼:{} 車次:{} 車種:{}",m.group('code'),m.group('trainNumber'),m.group('kind').encode('big5'))
# print(result)



def checkDateType(date):
    p = re.compile(r'\d{4}/\d{2}/\d{2}-(\d*)')
    m = p.match(date)
    if m.group(1).isdigit():
        if int(m.group(1)) > 11:
            return 'ctkind'
        else:
            return 'order_kind'
    else:
        return '非數字'

a= checkDateType('2017/03/12-12')
print(a)