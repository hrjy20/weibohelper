import requests
import urllib2
import urllib
import md5
import re
def getAccounts():
	fp = open('config/accounts.txt','r')
	data = fp.read()
	resdata = []
	data = data.split('\r\n')
	for string in data:
		if string != '':
			resdata.append(string)
		else:
			continue
	return resdata

def getCookies():
	fp = open("config/cookies.database","r")
	data = fp.read()
	resdata = []
	data = data.split('\n')
	for cookie in data:
		if cookie != '':
			resdata.append(cookie)
		else:
			continue
	return resdata
def getFormData(url,text=''):
	mid = getMid(url)
	form_data = {
	"pic_src":"",
	"pic_id":"",
	"appkey":"",
	"mid":mid,
	"style_type":1,
	"mark":"",
	"reason":text,
	"location":"page_100605_home",
	"module":"",
	"page_module_id":"",
	"refer_sort":"",
	"is_comment_base":1,
	"rank":"",
	"rankid":"",
	"_t":0
	}
	form_data = urllib.urlencode(form_data)
	return form_data

def verifi():
	filedata = ""
	res = {}
	url = "http://login.sina.com.cn/cgi/pin.php"
	r = requests.get(url,stream=True)
	cookie = r.headers['Set-Cookie']
	p = re.compile('ULOGIN_IMG=\w+-\w+;')
	cookie = p.search(cookie).group(0)
	for chunk in r:
		filedata = filedata+chunk
	headers = {
	"Content-type":"multipart/form-data; boundary=-------------RK",
	"Accept-Encoding":"gzip, deflate", 
	"Accept-Language":"zh-cn", 
	"Accept":"*/*", 
	"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0"
	}
	# fp = open(filename,"r")
	# filedata = fp.read()
	boundary = "---------------RK"
	data = []
	data.append(boundary)
	data.append('Content-Disposition: form-data; name="username"\r\n')
	data.append('undefined')
	data.append(boundary)
	data.append('Content-Disposition: form-data; name="password"\r\n')
	data.append('hduisa111')
	data.append(boundary)
	data.append('Content-Disposition: form-data; name="typeid"\r\n')
	data.append('5000')
	data.append(boundary)
	data.append('Content-Disposition: form-data; name="timeout"\r\n')
	data.append('90')
	data.append(boundary)
	data.append('Content-Disposition: form-data; name="softid"\r\n')
	data.append('71614')
	data.append(boundary)
	data.append('Content-Disposition: form-data; name="softkey"\r\n')
	data.append('30be95da6c574797bc11ddbdf6a79793')
	data.append(boundary)
	data.append('Content-Disposition: form-data; name="image"; filename="1.png"')
	data.append('Content-Type: application/octet-stream\r\n')
	data.append(filedata)
	data.append(boundary+"--")
	# data.append('Content-Disposition: form-data; name="Submit"\r\n')
	# data.append('submit')
	# data.append(boundary)
	httpBody = '\r\n'.join(data)
	postDataUrl = 'http://api.ruokuai.com/create.json'
	response = urllib2.Request(postDataUrl,data=httpBody, headers=headers)
	response = urllib2.urlopen(response)
	response = response.read()
	#print response
	try:
		p = re.compile('Result\":\"(.*)\",')
		code = p.search(response).group(1)
		res['cookie'] = cookie
		res['code'] = code
		return res
	except:
		print "Failed to get vefiri code.Please check your result_money!"
		exit()

def getMid(url):
	headers = {
	"Cookie":"SUB=_2.;"
	}
	r = requests.get(url,headers = headers,allow_redirects =False)
	p = re.compile('mid=([0-9]+)&src')
	mid = p.search(r.text).group(1)
	return mid