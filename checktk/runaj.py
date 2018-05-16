#!/usr/bin/python
import urllib.request, urllib.parse, urllib.error
import http.cookiejar
import sys

from bs4 import BeautifulSoup


def auto_login_hi():
    values = {
        'user_session_login': '201823380',
        'user_session_password': '5163'
    }
    postdata = urllib.parse.urlencode(values).encode('gbk')
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    headers = {'User-Agent': user_agent, 'Connection': 'keep-alive'}
    LOGIN_URL = "http://www.qgkzzx.com/default.do"
    #设置cookie
    request = urllib.request.Request(LOGIN_URL)
    request.add_header('User-agent', 'Mozilla/5.0')
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    request.add_header('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7')
    cookie_filename = 'cookie.txt'
    cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    response = urllib.request.urlopen(request, postdata)
    try:
        response = opener.open(request)
        page = response.read().decode('gbk')
    except urllib.error.URLError as e:
        print(e)
    cookie.save(ignore_discard=True, ignore_expires=True)
    for item in cookie:
        print('Name = ' + item.name)
        print('Value = ' + item.value)
    get_url = 'http://www.qgkzzx.com/u/personindex.do'  # 利用cookie请求访问另一个网址
    get_request = urllib.request.Request(get_url, headers=headers)
    get_response = opener.open(get_request)
    soup = BeautifulSoup(get_response.read().decode('gbk'), 'html.parser')

    ids = []
    #print(soup.prettify())
    for link in soup.find_all('a'):
        id = link.get('onclick').replace("openPaper('", '').replace(
            "','3')", "")
        print(id)
        ids.append(id)
    for id in ids[1:2]:
        get_url = "http://www.safetyme.cn//a/exam.shtml?method=showPaper&id=" + id
        print(get_url)
        get_request = urllib.request.Request(get_url, headers=headers)
        get_response = opener.open(get_request)
        soup = BeautifulSoup(get_response.read().decode('gbk'), 'html.parser')
        i = 0
        examtk = []
        for div in zip(
                soup.find_all("div", "exam-content"),
                soup.find_all("div", "for-wrong")):
            i = i + 1
            st = div[0]
            da = div[1]
            sttype = st.p.span.string
            print(sttype.replace("[", "").replace("]", ""))
            repstring = '<p><span style="color: green; font-weight: bold;">' + sttype + "</span>" + str(
                i) + "、"
            print(str(st.p).replace(repstring, "").replace("(1.0分)</p>", ""))
            print(da.contents[4].string.replace("正确答案：", "").strip())
            for li in st.ul:
                soup2 = BeautifulSoup(str(li), "html.parser")
                for inpt in zip(
                        soup2.find_all("input"), soup2.find_all("span")):
                    print(inpt[0]['value'])
                    print(inpt[1].string)
            tm = []
            tm.append(sttype.replace("[", "").replace("]", ""))
            tm.append(str(st.p).replace(repstring, "").replace(
                "(1.0分)</p>", ""))
            tm.append(da.contents[4].string.replace("正确答案：", "").strip())
            examtk.append(tm)

auto_login_hi()
