# encoding=gbk
'''
Created on 2017��8��15��

@author: Sophon
'''
import collections
import re
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import numpy as np

import plotly.plotly as py
import plotly.graph_objs as go

import os
from os import path
from scipy.misc import imread
from wordcloud import WordCloud
import jieba


# �����ı��ļ��������дʷ���list
def readInWords(file, wordslist):
    f = open(file, 'r')
    lines = f.readlines()
    for line in lines:
        print(line)
        wordslist.append(str(line).replace('\n', ''))
    print('%d words have been read' % len(wordslist))


def doWordsCounts(file, wordslist):
    counts = collections.Counter(wordslist)
    list = counts.most_common(30)
    x = []
    y = []
    with open(file, 'wb') as file:
        for kv in list:
            if re.findall(r'[�����20������������һǧ��һҹ]', kv[0]):
                continue
            x.append(kv[0])
            y.append(kv[1])
#             print('%s : %d' % (kv[0], kv[1]))
            line = kv[0] + " : " + str(kv[1]) + '\n'
            file.write(line.encode())
    return x, y
#     print(counts.most_common(50))


def draw_bar(data_x, data_y):
    data = [go.Bar(x=data_x, y=data_y)]
#     py.iplot(data, filename='basic-bar')

    trace1 = go.Bar(
        x=data_x,
        y=data_y,
        name='SF Zoo'
    )

    data = [trace1]
    layout = go.Layout(
        barmode='group'
    )

    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig, filename='grouped-bar')


def draw_wordcloud(file):
    # ����һ��txt�ļ�
    comment_text = open(file, 'rb').read()
    # ��ͷִʣ������ַ����������ͨ���ִʣ��޷�ֱ��������ȷ�����Ĵ���
    cut_text = " ".join(jieba.cut(comment_text))
    d = path.dirname(__file__)  # ��ǰ�ļ��ļ�������Ŀ¼
    color_mask = imread("c.jpg")  # ��ȡ����ͼƬ
    cloud = WordCloud(
        # �������壬��ָ���ͻ��������
        font_path="a.ttf",
        # font_path=path.join(d,'simsun.ttc'),
        # ���ñ���ɫ
        background_color='white',
        # ������״
        mask=color_mask,
        # �������ʻ�
        max_words=1000,
        # ��������
        max_font_size=40
    )
    word_cloud = cloud.generate(cut_text)  # ��������

    word_cloud.to_file(file.split('.')[0] + '.jpg')  # ����ͼƬ
    #  ��ʾ����ͼƬ
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.show()


def main():

    srcfile = '1001NightsTags.txt'
    savefile = '1001NightsTagCounts.txt'
#     draw_wordcloud(file)
    py.sign_in('xuantianqiang', 'dLaBV0bPxT6SbHfweDoC')
    wordslist = []
    readInWords(srcfile, wordslist)
    x, y = doWordsCounts(savefile, wordslist)
    print(x)
    print(y)
    draw_bar(x, y)


if __name__ == '__main__':
    main()
