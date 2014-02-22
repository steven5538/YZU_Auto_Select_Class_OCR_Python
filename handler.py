import urllib , urllib2 , cookielib

cookie_support = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
opener.addheaders = [
	('Host' , 'isdna1.yzu.edu.tw') ,
	('Accept' ,'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8') ,
	('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6') ,
	('Accept-Language' , 'zh-tw,zh;q=0.8,en-us;q=0.5,en;q=0.3') ,
	('Accept-Encoding' , 'gzip, deflate') ,
	('Connection' , 'keep-alive') ,
	('Cache-Control' , 'no-cache') ,
	('Content-Type' , 'application/x-www-form-urlencoded')
]