#!/usr/bin/python
# _*_ coding:utf-8 _*_
import urllib.request, urllib.parse, urllib.error
import http.cookiejar
import sys
import json
import csv, codecs
import re
import os
from bs4 import BeautifulSoup


def auto_login_hi():
    values = {'usercode': '201832245', 'userpws': '1966'}
    postdata = urllib.parse.urlencode(values).encode('utf-8')
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    headers = {'User-Agent': user_agent, 'Connection': 'keep-alive'}
    LOGIN_URL = "http://www.qgkzzx.com/user_login_check.do"
    #设置cookie
    request = urllib.request.Request(LOGIN_URL)
    request.add_header('User-agent', 'Mozilla/5.0')
    request.add_header('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7')
    cookie_filename = 'cookie.txt'
    cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    response = urllib.request.urlopen(request, postdata)
    try:
        response = opener.open(request)
        page = response.read().decode('utf-8')
        xmmc = json.loads(page)['xm_name']
    except urllib.error.URLError as e:
        print(e)
    cookie.save(ignore_discard=True, ignore_expires=True)
    for item in cookie:
        print('Name = ' + item.name)
        print('Value = ' + item.value)
    get_url = 'http://www.qgkzzx.com/u/personindex.do'  # 利用cookie请求访问另一个网址
    get_request = urllib.request.Request(get_url, headers=headers)
    get_response = opener.open(get_request)
    soup = BeautifulSoup(get_response.read().decode('utf-8'), 'html.parser')
    examtk = []
    stbh = 1
    for link in soup.find_all(name='a', attrs={"class": "grya"}):
        zsd = link.get('onclick').replace("goontmlx('", '').replace("')", '')
        get_url = 'http://www.qgkzzx.com/u/zsdtmlx.do?zsd_id=' + zsd
        get_request = urllib.request.Request(get_url, headers=headers)
        get_response = opener.open(get_request)
        soup = BeautifulSoup(get_response.read().decode('utf-8'),
                             'html.parser')
        istring = soup.find('i')
        stlx = soup.find('h4').text
        ts = str(istring.text.replace("1/", ''))
        for i in range(int(ts)):## 注意正式跑的时候要确认变量为ts
            tm = []
            get_url = 'http://www.qgkzzx.com/u/zsdtmlx.do?zsd_id=' + zsd + '&page=' + str(
                i + 1)
            print(get_url)
            get_request = urllib.request.Request(get_url, headers=headers)
            get_response = opener.open(get_request)
            soup = BeautifulSoup(get_response.read().decode('utf-8'),
                                 'html.parser')
            zsdmc = soup.find(name='a', attrs={"class": "menulittlein"}).text
            replaceStringBegin = '<p>' + '<i>' + str(i + 1) + '/' + str(
                ts) + '</i>'
            imgid = soup.find(name='img', attrs={"id": "check"})
            onclick = imgid.get('onclick')
            replaceStringEnd = '\r\n\t\t\t\t\t\t\t<img id="check" name="check" onclick="' + onclick + '" src="../images/no.gif" title="重点检查"/>\n</p>'
            replaceStringEnd2 = '<img id="check" name="check" onclick="' + onclick + '" src="../images/no.gif" title="重点检查"/>'
            replaceStringEnd3 = '</p>'
            stnr = str(soup.find('p')).replace(replaceStringBegin, '').replace(
                replaceStringEnd, '').replace(replaceStringEnd2, '').replace(
                    replaceStringEnd3, '')
            stxxs = []
            for label in soup.find_all('label'):
                stxxs.append(label.text)
            stda = str(soup.find('span')).replace(
                '<span id="ckda" style="display: none;"> 标准答案：', '').replace(
                    '</span>', '')
            tm.append(stbh)
            tm.append(stlx)
            tm.append(stnr)
            tm.append("##".join(stxxs))
            tm.append(stda)
            tm.append(xmmc)
            tm.append(zsdmc)
            examtk.append(tm)
            stbh = stbh + 1
    fname = os.path.abspath('.') + '\/file\/' + xmmc + '.csv'
    with open(
            fname, mode='w', encoding='gbk',
            newline='') as csvfile:  # 解决写入空行问题 使用wb不会再每一行后面插入空行
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(examtk)


auto_login_hi()