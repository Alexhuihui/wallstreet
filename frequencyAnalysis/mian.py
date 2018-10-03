# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import re
import urllib.parse
from urllib import request
import ssl
import chardet
import sys
import requests
import wordcloud as wc
import matplotlib.pyplot as plt
import jieba
from jieba.analyse import extract_tags
from PIL import Image
from numpy import array
import numpy as npy
from numpy import arange
import matplotlib


class HtmlParser(object):
	def get_new_data(self, page_url, soup):
		res_data = []
		anodes = soup.find_all('p')
		for anode in anodes:
			res_data.append(anode.get_text())
		
		return res_data
	
	def parse(self, page_url, html_cont):
		if page_url is None or html_cont is None:
			return
		
		soup = BeautifulSoup(html_cont, 'html.parser')
		new_data = self.get_new_data(page_url, soup)
		
		return new_data


class HtmlDownloader(object):
	def download(self, url):
		if url is not None:
			
			try:
				ssl._create_default_https_context = ssl._create_unverified_context
				
				headers = {
					'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0)'
				}
				req = request.Request(url=url, headers=headers)
				
				response = request.urlopen(req, timeout=10)
				
				if response.getcode() == 200:
					
					return requests.get(url).text
				
				else:
					
					return None
			
			except Exception as e:
				
				print(str(e))
		
		else:
			
			return None
class UrlManager(object):
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()

    def add_new_url(self, url):
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def has_new_url(self):
        return len(self.new_urls) != 0

    def get_new_url(self):
        new_url = self.new_urls.pop()
        #self.old_urls.add(new_url)
        return new_url
class HtmlOutputer(object):
    def __init__(self):
        self.datas = []

    def collect_data(self,data):
        if data is None:
            return
        self.datas = data

    def output_html(self):
        fout = open('output.txt', 'w', encoding='utf-8')

        for data in self.datas:
            fout.write(data)

        fout.close()
class SpiderMain(object):
    def __init__(self):
        self.urls = UrlManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.outputer = HtmlOutputer()
        
    def frequency(self):
	    path = "output.txt"
	    # 从路径读取报告全文，存为data
	    data = open(path, "r", encoding="UTF-8").read()
	    # 使用jieba分词
	    cutdata = jieba.cut(data)
	    alldata = ""
	    for i in cutdata:
		    alldata = alldata + " " + str(i)
	
	    font = r"/System/Library/Fonts/STHeiti Medium.ttc"
	    # 读图片
	    pic = Image.open("/Users/alex/Downloads/frequency.jpg")
	    # 图片转数组
	    picarray = array(pic)
	    # collocations=False表示是否归并词，传入字体路径，图片数组，设置背景颜色为白色，用alldata生成词云
	    mywc = wc.WordCloud(collocations=False, font_path=font, mask=picarray, background_color="white").generate(
		    alldata)
	    # 画布大小
	    fig = plt.figure(figsize=(10, 10))
	    # 展示图片
	    plt.imshow(mywc)
	    # 去掉坐标轴
	    plt.axis('off')
	    plt.show()
	
	    # extract_tags提取词频前20的关键词存为列表tags中
	    tags = extract_tags(sentence=alldata, topK=20)
	    # 全切词，分别统计出这20个关键词出现次数，即词频，存为字典words_freq中
	    words = [word for word in jieba.cut(data, cut_all=True)]
	    words_freq = {}
	    for tag in tags:
		    freq = words.count(tag)
		    words_freq[tag] = freq
	    # 将该字典按词频排序
	    usedata = sorted(words_freq.items(), key=lambda d: d[1])
	    # 字典转为numpy数组并作矩阵转置，方便画图取用
	    tmp = npy.array(usedata).T
	    print(tmp)
	
	    # 画布大小
	    fig, ax = plt.subplots(figsize=(10, 10))
	    # 输出中文字体
	    myfont = matplotlib.font_manager.FontProperties(fname="/System/Library/Fonts/STHeiti Medium.ttc")
	    # 图表标题设置，想要标题居中可以去掉x，y的设置
	    plt.title(u'华尔街快讯词频统计', fontproperties=myfont, fontsize=20, x=0.001, y=1.02)
	    # 图表x轴设置
	    ax.set_xlabel(u'出现次数', fontproperties=myfont, fontsize=20, x=0.06, y=1.02, color="gray")
	    # 边框线设置，去除上方右方的框线，左下框线置灰融入背景
	    ax.spines['bottom'].set_color('grey')
	    ax.spines['left'].set_color('grey')
	    ax.spines['top'].set_color('white')
	    ax.spines['right'].set_color('white')
	    # 传入词语，y轴显示20个标记位置，设置字体大小，颜色为灰色
	    tick_positions = range(1, 21)
	    ax.set_yticks(tick_positions)
	    ax.set_yticklabels(tmp[0], fontproperties=myfont, fontsize=18, color="gray")
	    # 设置数据条的间隔
	    bar_positions = arange(20) + 0.75
	    # 导入数据并做图展示
	    ax.barh(bar_positions, tmp[1], 0.5, align="edge")
	    plt.show()
    
    def craw(self, root_url):
        count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:

                new_url = self.urls.get_new_url()
                self.urls.add_new_url(root_url)

                print('craw %d : %s' % (count, new_url))

                html_cont = self.downloader.download(new_url)
                new_data = self.parser.parse(new_url, html_cont)
                self.outputer.collect_data(new_data)

                if count == 1:
                    break

                count += 1

            except:
                print('craw failed')

        self.outputer.output_html()
		

if __name__ == '__main__':
    root_url = 'https://wallstreetcn.com/live/global'
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)
    obj_spider.frequency()