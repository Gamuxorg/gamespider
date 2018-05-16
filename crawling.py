#!/usr/bin/env python3
from pyquery import PyQuery as pq
import urllib.parse
import urllib.request
import os,time

URLFIRST = "https://rutracker.org/forum/viewforum.php?f=1992"
currentpath = os.path.abspath('.')
listpagepath = os.path.join(currentpath, 'list')
outputpath = os.path.join(currentpath, 'rutracker-output')
outputfile = os.path.join(outputpath, 'output.txt')
gamelist = {}
if not os.path.exists(listpagepath):
    os.mkdir(listpagepath)


def CachePage(IndexPageNum=1):
    urldata = {}
    # 首页无此参数，第二页为50，第三页为100，依次类推
    urldata["start"] = IndexPageNum * 50
    urlvalue = urllib.parse.urlencode(urldata)
    if (IndexPageNum == 0):
        url = URLFIRST
    else:
        url = URLFIRST + "&" + urlvalue
    response = urllib.request.urlopen(url)
    htmlcontent = response.read().decode("Windows-1251")
    controledfile = open(os.path.join(listpagepath, str(IndexPageNum + 1) + ".html"), "w", encoding="utf-8")
    controledfile.write(htmlcontent)
    controledfile.close()
    response.close()
    print("第" + str(IndexPageNum + 1) + "页已获取完毕！")


def CacheMagnet():
    htmldom = pq(URLFIRST)
    indexnum = htmldom('a.pg').eq(-2).text()
    indexnum = int(indexnum)
    if not os.path.exists(outputpath):
        os.mkdir(outputpath)
    if not os.path.exists(outputfile):
        op = open(outputfile, 'w', encoding='utf-8')
        op.close()
    if (len([i for i in os.listdir(listpagepath) if os.path.isfile(os.path.join(listpagepath, i))]) != indexnum):
        for i in range(0, indexnum):
            CachePage(i)
    for i in os.listdir(listpagepath):
        if os.path.isfile(os.path.join(listpagepath, i)):
            htmlfile = open(os.path.join(listpagepath, i), 'r', encoding='utf-8', errors='ignore')
            htmldata = pq(htmlfile.read())
            gamelistnum = len(htmldata('a.tt-text'))
            for m in range(0, gamelistnum):
                innerhref = htmldata('a.tt-text').eq(m).attr('href')
                innerurl = 'https://rutracker.org/forum/' + innerhref
                innerdom = pq(url = innerurl)
                op = open(outputfile, 'a', encoding='utf-8')
                gamelist['size'] = htmldata('a.dl-stub').eq(m).text()
                gamelist['name'] = innerdom('div.post_body').children('span').eq(0).text()
                gamelist['magnet'] = innerdom('a.magnet-link').attr('href')
                op.write(str(gamelist))
                op.close
                time.sleep(2)
            htmlfile.close()


CacheMagnet()
