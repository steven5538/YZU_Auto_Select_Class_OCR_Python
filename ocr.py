# -*- coding: utf8 -*-

from PIL import Image
import urllib , urllib2 , cookielib
import sys
from urllib2 import urlopen, URLError, HTTPError
import handler


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

def numpoint(im):
	width , height = im.size
	data = list(im.getdata())
	mumpoint = 0

	for x in range(width):
		for y in range(height):
			if data[y * width + x] != 255:
				mumpoint += 1

	return mumpoint

def pointmidu(im):
    width , height = im.size

    for y in range(0 , height , 5):
        for x in range(0 , width , 5):
            box = (x , y , x + 5 , y + 5)
            im1 = im.crop(box)
            a = numpoint(im1)

            if a < 11:
                for i in range(x , x + 5):
                    for j in range(y , y + 5):
                        im.putpixel((i , j) , 255)
    return im

def imageFilter(im):
	im = im.convert('RGBA')
	im = im.rotate(1)
	im = im.crop((1 , 4 , im.size[0]-1 , im.size[1]-1))
	pix = im.load()

	width , height = im.size

	for y in xrange(height):
		for x in xrange(width):  
			if pix[x, y][1] != 0 and (pix[(x + 1) % width , y][1] != 0 and pix[x , (y + 1) % height][1] != 0) :
				pix[x, y] = (255, 255, 255, 255)
			else:
				pix[x, y] = (0, 0, 0, 255)

	
	dx=[-1 , -1 , -1 , 0 , 0 , 0 , 1 , 1 , 1]
	dy=[-1 , 0 , 1 , -1 , 0 , 1 , -1 , 0 , 1]

	for y in xrange(1 , height):
		for x in xrange(1 , width):  
			num = 0

			for i in range(len(dx)):
				if x > 0 and x < width - 1 and y > 0 and y < height - 1:
					if(pix[(x + dx[i]) , (y + dy[i])][0] == 0):
						num += 1

			if pix[x,y] == (255,255,255) and num >= 3:
				pix[x, y] = (0, 0, 0, 0)

	im = pointmidu(im)

	im.save('tmp_.png')

def OCR():
	import tesseract

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
		captha = OCR()

		if checkCaptha(captha) == True:
			print 'Captha: ' + captha
			return captha

