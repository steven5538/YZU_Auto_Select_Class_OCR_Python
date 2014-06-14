# -*- coding: utf8 -*-

import urllib , urllib2 , cookielib
from urllib2 import urlopen, URLError, HTTPError
from urllib import urlencode
from bs4 import BeautifulSoup
import time , sys

import ocr
import handler
import config

opener = handler.opener

def login():
	while True:
		global opener
		login_url = 'https://isdna1.yzu.edu.tw/CnStdSel/Index.aspx'

		try:
			login_info = urllib2.urlopen(login_url).read()
			info = BeautifulSoup(str(login_info))
		except:
			print 'server error.'
		
		login_data = config.loginInfo
		login_data['__VIEWSTATE'] = info.find('input' , {'id' : '__VIEWSTATE'})['value']
		login_data['__EVENTVALIDATION'] = info.find('input' , {'id' : '__EVENTVALIDATION'})['value']
		login_data['Txt_CheckCode'] = ocr.get(opener)

		login_data = urlencode(login_data)

		try:
			login_info = opener.open(login_url , login_data).read()
			info = str(login_info)
		except:
			print 'server error'

		if info.find('驗證碼錯誤') == -1:
			break
		else:
			print 'OCR error, still trying...'


	print 'Login SUCCESS!'

def getClass():
	while True:
		for classInfo in config.classInfo:
			global opener
			get_url = 'https://isdna1.yzu.edu.tw/CnStdSel/SelCurr/CurrMainTrans.aspx?mSelType=SelCos&mUrl=' + urllib.quote(classInfo)
			
			print classInfo

			try:
				get_info = opener.open(get_url).read()
				info = str(get_info)

				if info.find('逾時') != -1 or info.find('logged off') != -1 or info.find('異常') != -1:
					print 'been logout, relogin.'
					return False

				if info.find('加選訊息') != -1 or info.find('選過') != -1:
					print 'you get the class ,' + classInfo + ', check it.'
					return True

				if info.find('已達上限') != -1:
					print 'reach upper limit, still running...'

			except:
				print 'something wrong.'
				return True


			time.sleep(2.2)

if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding('utf-8')

	while True:
		login()
		if getClass() == True:
			break
