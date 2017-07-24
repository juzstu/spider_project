# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 16:07:50 2016

@author: Laresh
"""
import requests
import re
from bs4 import BeautifulSoup
import codecs
import csv
import sys  

'''
Sample spider for crawling douban Top250 and save as csv file.
'''

reload(sys)  
sys.setdefaultencoding('utf-8') 

douban_url = 'https://movie.douban.com/top250'

def get_page(url):
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    data = requests.get(url, headers=headers).content
    return data

def parse_html(html):
    soup = BeautifulSoup(html)
    movie_list_soup = soup.find('ol', attrs={'class':'grid_view'})
    movie_name_list = []
    comment_num = []
    score_list = []
    movie_dest = []    
    for i in movie_list_soup.find_all('li'):
        detail = i.find('div',attrs={'class':'hd'})
        movie_name = detail.find('span',attrs={'class':'title'}).getText()
        info = i.find('div',attrs={'class':'bd'})
        score = info.find('span', attrs={'class':'rating_num'}).getText()
        star = i.find('div',attrs={'class':'star'})
        num = star.find(text=re.compile(u'评价'))
        num = num[:-3]
        dest = info.find('span',attrs={'class':'inq'})
        if dest:
            movie_dest.append(dest.getText())
        else:
            movie_dest.append('无')
        score_list.append(score)
        comment_num.append(num)
        movie_name_list.append(movie_name)
    
    next_page = soup.find('span', attrs={'class':'next'}).find('a')
    if next_page:
        return movie_name_list, comment_num, score_list, movie_dest, douban_url + next_page['href']
    return movie_name_list, comment_num, score_list, movie_dest, None
        

def main():
    url = douban_url
    name = []
    num = []
    score = []
    info = []
    #循环结束 url=None
    while url:
        html = get_page(url)
        movie, peop, sc, inf, url = parse_html(html)
        name.extend(movie)
        num.extend(peop)
        score.extend(sc)
        info.extend(inf)
    final = zip(name,num,score,info)
    with codecs.open('top250.csv','wb',encoding='utf-8') as fp:
        writer = csv.writer(fp)
        writer.writerow(['电影','评价人数','评分','信息'])
        for f in final:
            writer.writerow(f)               

if __name__ == '__main__':
    main()
