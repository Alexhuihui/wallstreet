# -*- coding:utf-8 -*-
import wordcloud as wc
import matplotlib.pyplot as plt
import jieba
from jieba.analyse import extract_tags
from PIL import Image
from numpy import array
import numpy as npy
from numpy import arange
import matplotlib

path = "/Users/alex/PycharmProjects/wallstreet/frequencyAnalysis/output.txt"
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
mywc = wc.WordCloud(collocations=False, font_path=font, mask=picarray, background_color="white").generate(alldata)
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
