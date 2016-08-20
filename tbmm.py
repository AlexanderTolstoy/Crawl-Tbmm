# coding=utf-8
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.request import urlopen
import re
import os
import threading
def main():
    driver = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs")
    driver.get("https://mm.taobao.com/search_tstar_model.htm?")
    bsobj = BeautifulSoup(driver.page_source,'lxml')
    fp = open('mm.txt','r+')
    fp.write(driver.find_element_by_id('J_GirlsList').text)##获得主页上的姓名、所在城市、身高、体重等信息
    print("[*]OK GET MM's info")
    MMsinfoUrl = bsobj.findAll("a",{"href":re.compile("\/\/.*\.htm\?(userId=)\d*")})
#测试MMsinfoUrl的输出
# print (MMsinfoUrl)
# print (imagesUrl)
    fp.seek(0)#一定要让指针指回文件初始位置，否则会造成list index out of range的错误
    items = fp.readlines()
    content1 = [] # 存储个人信息
    n = 0
    m = 1
    while(n<14):
        content1.append([items[n].strip('\n'),items[m].strip('\n')])
        n += 3
        m += 3
# print (content1)
    content2 = [] # 存储个人主页网址
    for MMinfoUrl in MMsinfoUrl:
        content2.append(MMinfoUrl['href'])
# print (content2)
    contents = [[a,b] for a,b in zip (content1,content2)] #将个人的信息都集合在同一个容器中，方便查询操作
# print (contents)
    i=0
    while(i<5):  #为方便演示只取前5个姑凉的信息
        perMMpageUrl = "http:"+contents[i][1]
        path = "tbmm/"+contents[i][0][0]
        mkdir(path)
# print (path)
# print (perMMpageUrl)
        getperMMpageImg(perMMpageUrl,path)
        i += 1
    fp.flush()
    fp.close()
#得到姑凉主页的图片存储到对应文件夹
def getperMMpageImg(MMUrl,MMpath):
    owndriver = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs")
    owndriver.get(MMUrl)
    # print(MMpath)
    print("[*]Opening.....MM....................")
    ownobj = BeautifulSoup(owndriver.page_source,"lxml")
    perMMimgs = ownobj.find("div",class_="mm-aixiu-content").findAll("img",{"src":re.compile(".*\.jpg")})
    # print(perMMimgs)
    number = 1
    # print(number)
    for perMMimg in perMMimgs:
        imgPath = "https:"+str(perMMimg["src"])
        # print (imgPath)
        try:
            html = urlopen(imgPath)
            data = html.read()
            fileName = MMpath+'/'+str(number)+'.jpg'
            fpm = open(fileName,'wb')
            print("正在下载图片......")
            fpm.write(data)
            fpm.flush()
            fpm.close()
            number += 1
        except Exception:
            print ("下载失败了:(")
# 创建为姑凉对应文件夹
def mkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        print("建立:"+path+"文件夹")
        os.makedirs(path)
    else:
        print(path+"文件夹创建成功")
if __name__ == '__main__':
    main()
