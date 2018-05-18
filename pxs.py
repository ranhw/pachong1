# !/usr/bin/env python
# _*_ coding:utf-8 _*_

__author__='rhw'
import requests
import re
import os

def get_sort_list():
     response = requests.get('http://www.quanshuwang.com/list/1_1.html')
     response.encoding = 'gbk'
     #print(len(response.text))
     #print(response.text)
     html = response.text
     reg = r'<a target="_blank" title="(.*?)" href="(.*?)" class="clearfix stitle">'
     return re.findall(reg,html)
#get_sort_list()
def get_novel_list(url):
     response = requests.get(url)
     response.encoding = 'gbk'
     html = response.text
     reg = r'<a href="(.*?)" class="reader"'
     novel_url = re.findall(reg,html)[0]
     response = requests.get(novel_url)
     response.encoding = 'gbk'
     html = response.text
     reg = r'<li><a href="(.*?)" title=".*?">(.*?)</a><li>'
     chapter_url_list = re.findall(reg,html)
     return chapter_url_list

def get_chapter_content(url):
     response = requests.get(url)
     response.encoding = 'gbk'
     html = response.text
     reg = r'style5\(\);</script>(.*?)<script type="text/javascript">style6;'
     chapter_content = re.findall(reg, html, re.S)
     return chapter_content

for novel_name,novel_url in get_sort_list():
     #os.mkdir(os.path.join('novel',novel_name))
     path = os.path.join('novel',novel_name)
     if not os.path.exists(path):
         os.mkdir(path)
         print('创建文件夹成功')
     else:
         print('文件以存在，跳过')
         continue
         for chapter_url,chapter_name in get_novel_list(novel_url):
             chapter_content = get_chapter_content(chapter_url)
             with open(os.path.join(path,chapter_name + '.html'), 'w') as fn:
                 fn.write(chapter_content)
     break
