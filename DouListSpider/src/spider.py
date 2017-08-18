# encoding=gbk
'''
Created on 2017年8月12日
爬取豆瓣书单信息，保存书名跟连接到文本
爬取每本书的标签，保存到文本
分析标签，画出柱状图跟云图

@author: Sophon
'''

import time
import requests
from bs4 import BeautifulSoup

'''先获取下总共有多少页面，每页是25个条目'''


def getPageNums(url):
    firstPage = getHtmlText(url, None)
#     print(firstPage)
    soup = BeautifulSoup(firstPage, 'html.parser')
    p = soup.find('span', attrs={'class': 'thispage'})
    return p.attrs['data-total-page']


''''访问每个 页面，获取页面文本内容'''


def getHtmlText(url, param):
    try:
        if param == None:
            r = requests.get(url)
        else:
            r = requests.get(url, params=param)
        r.encoding = ('utf-8')
        return r.text
    except:
        print('Error: %s' % url)
        return ""


'''解析文本，获取每本书的名称及连接'''


def parserBookLists(booklist, html):

    soup = BeautifulSoup(html, 'html.parser')

    for div in soup.find_all('div', attrs={'class': 'bd doulist-subject'}):
        title = div.find('div', attrs={'class': 'title'})
        tag = title.find('a')
        dict = {'title': tag.string.strip(), 'url': tag.attrs['href']}
        booklist.append(dict)


'''解析书籍的标签'''


def parserBookTags(book, taglist):
    soup = BeautifulSoup(book, 'html.parser')
    tags = soup.find_all('a', attrs={'class': 'tag'})
    for tag in tags:
        tagstr = tag.string.encode('utf-8')
        taglist.append(tagstr)


'''遍历每一本书籍页面，获取书籍的标签'''


def getTags(booklist, tags):
    print('Find %d books:' % len(booklist))
    cnt = 1
    for book in booklist:
        print('Getting %d-th book tags' % cnt)
        bookurl = book['url']
        text = getHtmlText(bookurl, None)
        if text == "":
            continue
        parserBookTags(text, tags)
        cnt += 1
        time.sleep(3)


def printContents(booklist):
    print('getting tags from %d books:' % len(booklist))
    cnt = 1
    for book in booklist:
        print('%d-th book:' % cnt)
        print(book['title'].encode('utf-8'))
        print(book['url'])
        cnt += 1


def writeInfoToFile(books, file):
    print('  Writing book infos to file=========')
    with open(file, 'ab') as f:
        for book in books:
            info = book['title'] + '  :  ' + book['url'] + '\n'
            f.write(info.encode())


def writeTagToFile(tags, file):
    print('Writing tags to file=========')
    with open(file, 'ab') as f:
        for tag in tags:
            f.write(tag)
            f.write('\n'.encode())


def test():
    bookurl = 'https://book.douban.com/subject/26646201/'
    text = getHtmlText(bookurl, None)
    print(text)
    tags = []
    parserBookTags(text, tags)


def crawDouList(urlbase, idlist, bookInfoFile, bookTagFile):
    booklist = []
    for id in idlist:
        url = urlbase + id + '/'
        # 解析下有几页
        nums = int(getPageNums(url))
        # 遍历每页，解析到书籍名称和url
        for i in range(nums):
            start = i * 25
            kv = {'start': start}
            text = getHtmlText(url, kv)
            if text == "":
                continue
            parserBookLists(booklist, text)
            print('Writing %d-th page info to file:' % i)
            writeInfoToFile(booklist, bookInfoFile)
            time.sleep(1)
    # 遍历书籍信息列表，获取标签
    tags = []
    getTags(booklist, tags)
    writeTagToFile(tags, bookTagFile)
    print(tags)


def main():
    urlbase = 'https://www.douban.com/doulist/'

    id_1001nights = ['40243926']
    id_all = ['3574376', '37743651', '43837485', '3569759']
    id_logicMind = ['3574376']

#     bookInfoFile = '1001Nights.txt'
#     bookTagFile = '1001NightsTags.txt'
#     crawDouList(urlbase, id_1001nights, bookInfoFile, bookTagFile)

    bookInfoFile = 'LogicMind.txt'
    bookTagFile = 'LogicMindTags.txt'
    crawDouList(urlbase, id_logicMind, bookInfoFile, bookTagFile)


if __name__ == '__main__':
    main()
