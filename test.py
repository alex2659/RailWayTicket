#-*-coding:utf-8 -*-
import re


html = """
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
	<title>車種訂票結果</title>
	<meta http-equiv="Content-Type" content="text/html; charset=big5">
	<meta http-equiv="Pragma" content="no-cache">
	<meta http-equiv="Cache-Control" content="no-cache">
	<link href="./CssStyle/master.css" rel="stylesheet" type="text/css">
	<style type="text/css">
		input, select {font-family:Arial;}
		span.hd1 {width:100px;}
		span.hv1 {width:150px;}
	</style>
</head>
<body>
<div><a href="#" accesskey="C" title="中間主要內容區，此區塊呈現網頁的網頁內容">:::</a></div>
<table width='750' border='0'><tr><td background='./Images/title_bg.jpg' style='text-align:left'><img src='./Images/title_04.jpg' alt='車種訂來回票'></td></tr></table><br><p><font class='orange02'><strong>去程結果 : </strong></font></p>
<p><font class='orange02'><strong>您的車票已訂到</strong></font></p><p class='gray01'><span class='hd1'>身分證字號：</span> <span id='spanPid' class='hv1 blue01 bold01'>R124190739</span></p><p class='gray01'><span class='hd1'>電腦代碼：</span> <span id='spanOrderCode' class='hv1 red02 text_14p bold01'>957023</span></p><p class='gray01'><span class='hd1'>車次：</span> <span class='hv1 blue01 bold01'>51</span><span class='hd1'>車種：</span> <span class='hv1 blue01 bold01'>莒光</span></p><p class='gray01'><span class='hd1'>乘車時刻：</span> <span class='hv1 blue01 bold01'>2017/03/10 06:12</span></p><p class='gray01'><span class='hd1'>起站：</span> <span class='hv1 blue01 bold01'>&#21488;&#21271;    </span><span class='hd1'>到站：</span> <span class='hv1 blue01 bold01'>&#26032;&#24038;&#29151;  </span><span class='hd1'>張數：</span> <span class='hv1 blue01 bold01'>01</span></p><p class='gray01'>取票或網路付款截止時間：<br/>車站、郵局請於	<span class='blue01 bold01'>2017/02/28</span> 營業時間內完成取票<br/>超商請於		<span class='blue01 bold01'>2017/02/28 24:00</span> 前完成付款取票<br/>網路付款請於	<span class='blue01 bold01'>2017/02/28 24:00</span> 前完成付款<br/>郵局及超商須另支付每張8元取票服務費<br/><b>若您3個月內逾期未取票累計3次，系統將停止受理訂票6個月</b><p>郵輪式列車車票不開放網路付款系統、對號列車自動售票機取票</p></p><script language='javascript' src='./pay.js'></script><noscript></noscript><form id='goPayForm' onsubmit='return goPay();' action='https://ticket.ctbcbank.com/railway/index.php' method='post' target='_blank' style='float:left;'><input type='hidden' name='howgo'/><input type='hidden' name='na'   /><input type='hidden' name='id1'  /><input type='hidden' name='go1sn'/><input type='hidden' name='id2'  /><input type='hidden' name='go2sn'/><input type='hidden' name='id3'  /><input type='hidden' name='go3sn'/><button type='submit' style='border:0;background:white;width:150px;'><img src='./Images/pay02_a.jpg' alt='網路付款(另開視窗)' onmouseover="this.src='./Images/pay02_b.jpg'" onmouseout="this.src='./Images/pay02_a.jpg'" onfocus="this.src='./Images/pay02_b.jpg'"  onblur="this.src='./Images/pay02_a.jpg'"></button></form><form name='form1' method='post' action='ccancel.jsp' style='margin-left:100px;'><input type='hidden' name='personId'  value='R124190739'><input type='hidden' name='orderCode' value='957023'><button type='submit' style='border:0;background:white;width:150px;'><img src='./Images/delete02_a.jpg' alt='取消此車次訂票' onmouseover="this.src='./Images/delete02_b.jpg'" onmouseout="this.src='./Images/delete02_a.jpg'" onfocus="this.src='./Images/delete02_b.jpg'" onblur="this.src='./Images/delete02_a.jpg'"></button></form>

</body>
</html>
"""
# 找出html裡的文字 並存在group裡 id:身份證字號 code:電腦代碼 trainNumber:車次 kind:車種
regex = r"<span id='spanPid' [^>]*>(?P<id>\w*).*<span id='spanOrderCode'[^>]*>(?P<code>\d*).*車次：</span> <span class='hv1 blue01 bold01'>(?P<trainNumber>\d*).*車種：</span> <span class='hv1 blue01 bold01'>(?P<kind>[自強|莒光|復興]*)"
# p = re.compile(regex)
m = re.search(regex.decode('utf-8'),html.decode('utf-8'))
result = str.format("身份證字號:{} 電腦代碼:{} 車次:{} 車種:{}",m.group('id').encode('utf-8'),m.group('code').encode('utf-8'),m.group('trainNumber').encode('utf-8'),m.group('kind').encode('utf-8'))
print(result)