# encoding:utf-8
import urllib, urllib.request, http.cookiejar, re
import urllib.parse
import requests
import re
import sys
from bs4 import BeautifulSoup
# import lxml
 
# Personal information
username = ''
password = ''
# cookie
cj = http.cookiejar.CookieJar()
cookie_hanler = urllib.request.HTTPCookieProcessor(cj)
 
# get once value
lgurl = 'http://v2ex.com/signin'
User_Agent = 'Mozilla/5.0'
headers = {'User-Agent':User_Agent}
req = urllib.request.Request(url = lgurl, headers = headers)
opener = urllib.request.build_opener(cookie_hanler)
urllib.request.install_opener(opener)
contents = opener.open(req)
contents = contents.read()
contents = contents.decode('utf-8')
print(contents)
# with urllib.request.urlopen(req) as response:

# match once value
reg = r'value="(.*)" name="once"'
pattern = re.compile(reg)
result = pattern.findall(contents)

# set login value
lgurl = 'http://v2ex.com/signin'
once = result[0]
data = {'u':username, 'p':password, 'once':once, 'next':'/'}
data = urllib.parse.urlencode(data).encode(encoding='utf-8')
hdr = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36', 'Referer':'http://v2ex.com/signin', 'Host':'v2ex.com'}
req = urllib.request.Request(url = lgurl, data = data, headers = hdr)
 
# login in
response = opener.open(req)
page = response.read()

# redirection
sign = urllib.request.urlopen('http://v2ex.com/mission/daily')
verify = re.compile(r"onclick=.* = '(.*)'")
last = re.findall(verify,sign.read().decode('utf-8'))
mission_url = 'http://v2ex.com' + last[0]
res = urllib.request.urlopen(mission_url)
mission_page = res.read()

if "Daily login reward has been claimed" in mission_page.decode('gbk','ignore'):
    print('Daily login reward has been claimed')
else:
	print("Claimed successfully")
	# print(mission_page)

