# coding:utf-8
# Author:sudoinit0
import os
import time
import aircv as ac
from PIL import Image
import random
import sys

def openscreen():
	os.system('adb shell screencap -p /sdcard/1.png')
	os.system('adb pull /sdcard/1.png state.png')
	image = Image.open("state.png")
	print image.getcolors()
	
	for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
		if count >= 65535:
			if r==0 and g==0 and b==0 :
				print u'目前是黑屏状态'
				cmd = 'adb shell input keyevent 26'
				os.system(cmd)
				print u'开屏成功'
				break


def getpos():
	os.system('adb shell screencap -p /sdcard/1.png')
	os.system('adb pull /sdcard/1.png state.png')
	piclist=['5.jpg','4.jpg','3.jpg','2.jpg','1.jpg','success.jpg','bothok.jpg','black.jpg']
	i=0
	for pic in piclist :
		i+=1
		imsrc = ac.imread('state.png')
		imobj = ac.imread(pic)
		pos = ac.find_template(imsrc, imobj)
		print pos
		if pos !=None:
			if pos['confidence'] >0.92 :
				break
	if i>=len(piclist):
		return ""
	else:
		print(pic)
		return pic

def posandpress(img):
	os.system('adb shell screencap -p /sdcard/1.png')
	os.system('adb pull /sdcard/1.png state.png')
	imsrc = ac.imread('state.png')
	imobj = ac.imread(img)
	pos = ac.find_template(imsrc, imobj)
	cmd="adb shell input tap {} {}".format(pos['result'][0], pos['result'][1])
	print cmd
	os.system(cmd)
	
def backmain():
	os.system('adb shell input keyevent 4')
	print u"返回键"
	time.sleep(2)
	os.system('adb shell input keyevent 4')
	print u"返回键"
	time.sleep(2)
	os.system('adb shell input keyevent 4')
	print u"返回键"
	time.sleep(2)
	os.system('adb shell input keyevent 4')
	print u"返回键"
	time.sleep(2)
	os.system('adb shell input keyevent 4')
	print u"返回键"
	time.sleep(2)
	os.system('adb shell input keyevent 4')
	print u"返回键"
	time.sleep(2)
	os.system('adb shell input keyevent 3')
	print u"主页键"
	time.sleep(5)

def runsleep():
	waitminute=random.randint(1, 30)
	print u"等待时间",waitminute
	time.sleep(60*waitminute)


def checkplace():
	os.system('adb shell screencap -p /sdcard/1.png')
	os.system('adb pull /sdcard/1.png state.png')
	imsrc = ac.imread('state.png')
	imobj = ac.imread('jinru.jpg')
	pos = ac.find_template(imsrc, imobj)
	if pos !=None and pos['confidence'] >0.92 :
		print u"现在在打卡范围内"
		return True
	else:
		return False


def checktime():
	print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	dakaflag=-1
	hour=int(time.strftime("%H", time.localtime()))
	print u"当前小时为",hour
	if 7<=hour<=8:
		print u"现在是上班打卡"
		dakaflag=0
	elif 17<=hour<=19:
		print u"现在是下班打卡"
		dakaflag=1
	else:
		print u"现在不在打卡时间"
		dakaflag=-1
		quit()
	return dakaflag


reload(sys)
sys.setdefaultencoding('utf-8')
checktime()
runsleep()
openscreen()

trytime=0
while trytime<20:
	trytime+=1
	pic=getpos()
	if pic=='1.jpg' :
		print u'当前为待机界面'
		posandpress('1.jpg')
		print u'进入钉钉页面'
		time.sleep(5)
	elif pic=='2.jpg':
		print u'钉钉非公司首页'
		posandpress('2.jpg');
		print u'进入公司主页'
		time.sleep(5)  
	elif pic=='3.jpg':
		print u'公司首页'
		posandpress('3.jpg')
		print u'进入打卡页面'
		time.sleep(15)
	elif pic=='4.jpg':
		print u'上班打卡首页'  
		if checktime()==0:
			if checkplace()==True:
				print u'开始上班打卡'
				posandpress('4.jpg')
				time.sleep(5)
			else:
				print u"现在不在打卡范围，等待定位"
		else:
			os.system('adb shell input keyevent 4')
			time.sleep(5)
			os.system('adb shell input keyevent 4')
			time.sleep(5)
			os.system('adb shell input keyevent 4')
			quit()
	elif pic=='5.jpg':
		print u'下班打卡首页'  
		if checktime()==1:
			if checkplace()==True:
				print u'开始下班打卡'
				posandpress('5.jpg')
				time.sleep(5)
			else:
				print u'现在不在打卡范围，等待定位'
		else:
			os.system('adb shell input keyevent 4')
			time.sleep(5)
			os.system('adb shell input keyevent 4')
			time.sleep(5)
			os.system('adb shell input keyevent 4')
			quit()
	elif pic=='success.jpg':
		print u'打卡成功'
		posandpress('iknow.jpg')
		time.sleep(2)
		os.system('adb shell input keyevent 4')
		time.sleep(5)
		os.system('adb shell input keyevent 4')
		quit()
	elif pic=='bothok.jpg':
		print u'你今天已经完成打卡了'
		os.system('adb shell input keyevent 4')
		time.sleep(5)
		os.system('adb shell input keyevent 4')
		time.sleep(5)
		os.system('adb shell input keyevent 4')
		quit()
	else:
		print u'其他'
		openscreen()
		backmain()
print u"打卡失败"
	
