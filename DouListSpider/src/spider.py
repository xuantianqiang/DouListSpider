# encoding=gbk
'''
Created on 2017��8��12��
��ȡ�����鵥��Ϣ���������������ӵ��ı�
��ȡÿ����ı�ǩ�����浽�ı�
������ǩ��������״ͼ����ͼ

@author: Sophon
'''

import time
import requests
from bs4 import BeautifulSoup

'''�Ȼ�ȡ���ܹ��ж���ҳ�棬ÿҳ��25����Ŀ'''


def getPageNums(url):
    firstPage = getHtmlText(url, None)
#     print(firstPage)
    soup = BeautifulSoup(firstPage, 'html.parser')
    p = soup.find('span', attrs={'class': 'thispage'})
    return p.attrs['data-total-page']


''''����ÿ�� ҳ�棬��ȡҳ���ı�����'''


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


'''�����ı�����ȡÿ��������Ƽ�����'''


def parserBookLists(booklist, html):

    soup = BeautifulSoup(html, 'html.parser')

    for div in soup.find_all('div', attrs={'class': 'bd doulist-subject'}):
        title = div.find('div', attrs={'class': 'title'})
        tag = title.find('a')
        dict = {'title': tag.string.strip(), 'url': tag.attrs['href']}
        booklist.append(dict)


'''�����鼮�ı�ǩ'''


def parserBookTags(book, taglist):
    soup = BeautifulSoup(book, 'html.parser')
    tags = soup.find_all('a', attrs={'class': 'tag'})
    for tag in tags:
        tagstr = tag.string.encode('utf-8')
        taglist.append(tagstr)


'''����ÿһ���鼮ҳ�棬��ȡ�鼮�ı�ǩ'''


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
        # �������м�ҳ
        nums = int(getPageNums(url))
        # ����ÿҳ���������鼮���ƺ�url
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
    # �����鼮��Ϣ�б���ȡ��ǩ
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
