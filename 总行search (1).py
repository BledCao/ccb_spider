
# coding: utf-8

# In[ ]:

import requests
from lxml import etree
from selenium import webdriver
from urllib.request import urlretrieve
import time
import re
import sys


# In[ ]:

#初始化webdriver，并打开搜索页面
driver=webdriver.Chrome(r"E:/caobinqi2/Python/chromedriver.exe")
driver.get("http://eip.ccb.com")
driver.find_element_by_xpath('//*[@id="serchForm"]/input[2]').click()
driver.switch_to_window(driver.window_handles[1])


# In[ ]:

#输入搜索关键字
gjz=input("请输入要搜索的关键字：")
driver.find_element_by_xpath('//*[@id="1173116146534"]/table/tbody/tr/td/div/input[1]').clear()
driver.find_element_by_xpath('//*[@id="1173116146534"]/table/tbody/tr/td/div/input[1]').send_keys(gjz)
driver.find_element_by_xpath('//*[@id="1173116146534"]/table/tbody/tr/td/div/button').click()


# In[27]:

#构建搜索结果页的链接和页数
pageurls=[]
s=input("请输入要下载的页数（搜索页的页码数）：")
for num in range(1,int(s)+1):
    pageurls.append(driver.current_url[:-1]+str(num))
print(pageurls)


# In[ ]:

#解析搜索结果页，并将搜索结果链接纳入list
link_list=[]
for pageurl in pageurls:
    r=requests.get(pageurl)
    time.sleep(2)
    r_page=etree.HTML(r.text)
    for a in r_page.xpath('//script[@type="text/javascript"]/text()'):
        b=re.findall(r'hrefStrNoEbook="(.*)"',a)
        if len(b)>=1:
            c="http://eip.ccb.com:81"+b[0]
            link_list.append(c)
    print(link_list)


# In[ ]:

#遍历每个搜索结果链接，判断是否有附件并下载
titlelist=set()
for link in link_list:
    try:
        r=requests.get(link)
        time.sleep(2)
        r_page=etree.HTML(r.text)
        h=r_page.xpath('//*[@id="ccb_fujian"]/strong/a/@href') 
        if len(h)>=1: #文章中包含附件
            elements=r_page.xpath('//*[@id="ccb_fujian"]/strong/a')
            title=r_page.xpath('//*[@class="title" and @colspan="2"]/text()')
            textright=r_page.xpath('//*[@class="textright" and @width="56%"]/text()')[0]
            date=re.findall(r'发布时间:(.*)',textright)[0]
            print(h[0])
            try:
                #按照文章标题判断是否已下载，否则循环下载单个页面中的每个附件
                if title[0] not in titlelist:
                    for e in elements:
                        urlretrieve(e.xpath('@href')[0],"E:/caobinqi2/Python/eip_search_download/"+date+e.xpath('text()')[0])
                        print(title[0])
                        print(date)
                    titlelist.add(title[0])
                else:
                    print("已存在:"+title[0])
            except:
                print("下载错误", sys.exc_info()[0])
    except:
        print("获取页面错误"+sys.exc_info()[0])
print(titlelist)

