# -*- coding: utf8 -*-

from PIL import Image , ImageEnhance
import urllib , urllib2 , cookielib
from urllib2 import urlopen, URLError, HTTPError
import cv2 , tesseract
import numpy as np


def downloadImage(opener):
	try:
		f = opener.open('https://isdna1.yzu.edu.tw/Cnstdsel/SelRandomImage.aspx')
		urllib2.install_opener(opener)

		with open('tmp.png' , 'wb') as local_file:
			local_file.write(f.read())

	except HTTPError , e:
		print "HTTPError: " , e.code
	except URLError , e:
		print "URLError: " , e.reason

def imageOpening():
	img = cv2.imread('tmp.png' , 0)
	kernel = np.ones((2 , 2) , np.uint8)
	opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

	cv2.imwrite('tmp_.png' , opening)

def imageFilter(im):
	enhancer = ImageEnhance.Contrast(im)
	im = enhancer.enhance(3.0)
	enhancer = ImageEnhance.Brightness(im)
	im = enhancer.enhance(10.0)

	pix = im.load()
	w , h = im.size

	for x in xrange(w):
		for y in xrange(h):
			if pix[x , y][2] == 255 and pix[x , y][3] == 255 and pix[x , y][1] != 255:
				pix[x , y] = (0 , 0 , 0 , 255)
			else:
				pix[x , y] = (255 , 255 , 255 , 255)

	im.save('tmp.png')

def OCR():
	api = tesseract.TessBaseAPI()
	api.Init('.' , 'eng' , tesseract.OEM_DEFAULT)
	api.SetVariable('tessedit_char_whitelist' , '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
	api.SetPageSegMode(tesseract.PSM_AUTO)

	mBuffer=open('tmp_.png' , 'rb').read()
	result = tesseract.ProcessPagesBuffer(mBuffer , len(mBuffer) , api)

	if result != None:
		return result.strip()
	else:
		return None

def checkCaptha(captha):
	if captha == None or len(captha) != 4:
		return False
	return True

def get(opener):
	while True:
		print 'Predicting OCR..'
		downloadImage(opener)
		im = Image.open('tmp.png')
		imageFilter(im)
		imageOpening()
		captha = OCR()

		if checkCaptha(captha) == True:
			print 'Captha: ' + captha
			return captha

