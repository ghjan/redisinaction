#!/usr/bin/python
# -*- coding:utf-8 -*-
# urllib2_test.py
# author: wklken
# 2012-03-17 wklken@yeah.net

import urllib, urllib2, cookielib, socket
import testurllib2

url = "http://www.baidu.com"  # change yourself
'''
Python网页抓取urllib,urllib2,httplib[3]
    http://blog.csdn.net/wklken/article/details/7364390
在python的urllib2中使用socks代理
    http://panweizeng.com/python-urllib2-socks-proxy.html
'''


# 最简单方式
def use_urllib2():
    try:
        f = urllib2.urlopen(url, timeout=15).read()
    except urllib2.URLError, e:
        print e.reason
    print "length of content of (url:%s) : %d" % (url, len(f))


# 使用Request
def get_request():
    # 可以设置超时
    socket.setdefaulttimeout(25)
    # 可以加入参数  [无参数，使用get，以下这种方式，使用post]
    params = {"wd": "a", "b": "2"}
    # 可以加入请求头信息，以便识别
    i_headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",
                 "Accept": "text/plain"}
    # use post,have some params post to server,if not support ,will throw exception
    # req = urllib2.Request(url, data=urllib.urlencode(params), headers=i_headers)
    req = urllib2.Request(url, headers=i_headers)

    # 创建request后，还可以进行其他添加,若是key重复，后者生效
    # request.add_header('Accept','application/json')
    # 可以指定提交方式
    # request.get_method = lambda: 'PUT'
    try:
        page = urllib2.urlopen(req)
        print 'page length:', len(page.read())
        # like get
        # url_params = urllib.urlencode({"a":"1", "b":"2"})
        # final_url = url + "?" + url_params
        # print final_url
        # data = urllib2.urlopen(final_url).read()
        # print "Method:get ", len(data)
    except urllib2.HTTPError, e:
        print "Error Code:", e.code
    except urllib2.URLError, e:
        print "Error Reason:", e.reason


def getCharsetFromHeader(header):
    if not header:
        return None
    result = {}
    charset = None
    for item in header:
        result.update({item[0]: item[1]})
    content_type = result.get('content-type')
    import re
    ss = re.split("; ", content_type)
    for s in ss:
        lstTemp = s.split('=')
        lstTemp = [item.strip().lower() for item in lstTemp if item and item.strip() != '']
        if lstTemp and len(lstTemp) == 2:
            if lstTemp[0] == 'charset':
                charset = lstTemp[1] and lstTemp[1].replace('"', '')
                break
    return charset


def getStream_withsocks(url_google="https://www.youtube.com/"):
    import socks
    import socket
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "localhost", 1080)
    socket.socket = socks.socksocket
    socket.setdefaulttimeout(100)
    import urllib2
    return urllib2.urlopen(url_google, timeout=200)


def use_socks(url_google="https://www.youtube.com/"):
    stream = getStream_withsocks(url_google)
    print stream.read()


def use_proxy(myurl=url, enable_proxy=False):
    proxy_handler = urllib2.ProxyHandler({"http": "http://localhost:1080"})
    null_proxy_handler = urllib2.ProxyHandler({})
    if enable_proxy:
        opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
    else:
        opener = urllib2.build_opener(null_proxy_handler, urllib2.HTTPHandler)
    # 此句设置urllib2的全局opener
    urllib2.install_opener(opener)
    content = urllib2.urlopen(myurl).read()
    print "proxy len:", len(content)


class NoExceptionCookieProcesser(urllib2.HTTPCookieProcessor):
    @staticmethod
    def http_error_403(self, req, fp, code, msg, hdrs):
        return fp

    @staticmethod
    def http_error_400(self, req, fp, code, msg, hdrs):
        return fp

    @staticmethod
    def http_error_500(self, req, fp, code, msg, hdrs):
        return fp


def hand_cookie():
    cookie = cookielib.CookieJar()
    # cookie_handler = urllib2.HTTPCookieProcessor(cookie)
    # after add error exception handler
    cookie_handler = NoExceptionCookieProcesser(cookie)
    opener = urllib2.build_opener(cookie_handler, urllib2.HTTPHandler)
    url_login = "http://138.128.194.6:8080/discuz/forum.php"
    params = {"username": "admin", "password": "myserverbbs1"}
    opener.open(url_login, urllib.urlencode(params))
    for item in cookie:
        print item.name, item.value
        # urllib2.install_opener(opener)
        # content = urllib2.urlopen(url).read()
        # print len(content)


# 得到重定向 N 次以后最后页面URL
def get_request_direct(url_google='http://www.google.com'):
    import httplib
    httplib.HTTPConnection.debuglevel = 1
    request = urllib2.Request("http://www.google.com")
    request.add_header("Accept", "text/html,*/*")
    request.add_header("Connection", "Keep-Alive")
    opener = urllib2.build_opener()
    f = opener.open(request)
    print f.url
    print f.headers.dict
    print len(f.read())


if __name__ == "__main__":
    use_urllib2()
    get_request()

    url_google = 'http://www.youtube.com'
    try:
        get_request_direct(url_google)
    except Exception, e:
        print e
    print "use proxy-null proxy-------------"
    use_proxy()
    print "use proxy-socket proxy-------------"
    use_socks(url_google)
    print "run hand_cookie-------------"
    hand_cookie()
