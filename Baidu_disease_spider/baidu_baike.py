#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/2/26 0026 上午 10:02
# @Author  : Juzphy

import requests
import lxml.html as HTML
import json
import pandas as pd
import re
import os
import glob

'''
    URL： https://baike.baidu.com/wikitag/taglist?tagId=75953
    任务描述：
        1、爬取该链接下所有百科内容(链接是XHR形式访问, 这里需要找到真正链接)
        2、将内容保存成txt和html文件
'''

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36 QQBrowser/3.9.3943.400",
    'X-Requested-With': 'XMLHttpRequest'}


def get_disase():
    # total：7250
    # totalPage：303
    url = 'https://baike.baidu.com/wikitag/api/getlemmas'
    count = 0
    with open('./data/disease_list.csv', 'w') as f:
        f.write('Id, Name, Url')
        f.write('\n')
        first_page_paras = {'contentLength': '40', 'filterTags': '[]', 'fromLemma': 'false', 'limit': '24',
                            'page': '0', 'tagId': '75953', 'timeout': 3000}
        first_res = requests.post(url, data=first_page_paras, headers=headers, allow_redirects=False)
        first_lemma = json.loads(first_res.text)
        total_page = first_lemma['totalPage']
        for i in range(total_page):
            paras = {'contentLength': '40', 'filterTags': '[]', 'fromLemma': 'false', 'limit': '24',
                     'page': '{}'.format(i), 'tagId': '75953', 'timeout': 3000}
            res = requests.post(url, data=paras, headers=headers, allow_redirects=False)
            lemma = json.loads(res.text)
            lemma_list = [(l['lemmaId'], l['lemmaTitle'], l['lemmaUrl']) for l in lemma['lemmaList']]
            for ll in lemma_list:
                f.write('{0}, {1}, {2}'.format(ll[0], ll[1], ll[2]))
                f.write('\n')
                count += 1
                print('Already writen the {0} record ==> {1}'.format(count, ll[1]))


def save2txt(path):
    df = pd.read_csv('./data/disease_list.csv', encoding='gbk')
    size = df.shape[0]
    for s in range(size):
        single = df.iloc[s, 1]
        if '/' in single:
            single = single.replace('/', '-')
        with open(path + '/{}.txt'.format(single), 'w', encoding='utf8') as file:
            res = requests.get(df.iloc[s, 2], headers=headers)
            content = res.text.encode(res.encoding).decode('utf8')
            pattern = re.compile('label-module="para-title">(.*?)<div class="anchor-list">', re.S)
            features = re.findall(pattern, content)
            length = len(features) + 1
            pattern1 = re.compile('<a name="{}" class="lemma-anchor para-title" ></a>(.*?)<div class="tashuo-bottom" id="tashuo_bottom">'.format(length),
                                  re.S)
            pattern2 = re.compile('<a name="{}" class="lemma-anchor para-title" ></a>(.*?)<div id="open-tag">'.format(length), re.S)
            temp = re.findall(pattern1, content)
            if temp:
                features.extend(temp)
            else:
                temp = re.findall(pattern2, content)
                features.extend(temp)
            txt = HTML.fromstring(content)
            des = txt.xpath("//div[@class='lemma-summary']")
            des_list = [d.xpath('string(.)') for d in des]
            description = ''.join(des_list).strip()
            file.write(description)
            file.write('\n')
            file.write('\n')
            headline = txt.xpath("//span[@class='headline-content']/text()")
            if headline:
                file.write(headline[0])
                file.write('\n')
            dt = txt.xpath("//div[@class='basic-info cmn-clearfix']/dl/dt/text()")
            dd = [x.strip() for x in txt.xpath("//div[@class='basic-info cmn-clearfix']/dl/dd/text()")]
            dt_dd = zip(dt, dd)
            for d in dt_dd:
                file.write(d[0] + ': ' + d[1])
                file.write('\n')
            file.write('\n')
            for fs in features:
                ft = HTML.fromstring(fs)
                feature = ft.xpath("//h2[@class='title-text']/text()[1]")
                if feature:
                    file.write(feature[0])
                    file.write('\n')
                else:
                    feature = ft.xpath('//h3[@class="title-text"]/text()[1]')
                    file.write(feature[0])
                    file.write('\n')
                para = ft.xpath("//div[@class='para']")
                # 有的网页会出现两个<div class="para" label-module="para">相邻情况
                content_list = [p.xpath('string(.)') for p in para if '\r\n' not in p.xpath('string(.)')
                                if p.xpath('string(.)')]
                for c in content_list:
                    file.write(c)
                    file.write('\n')
                file.write('\n')
        print('Already writen the txt file for {0}, order==>{1}'.format(single, s + 1))


def html_template(body, name):
    body_list = [b for b in body[0].split('\n') if b if 'img' not in b]
    final_body = '\n'.join(body_list)
    template = '''
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        <title>{0}</title>
        </head>
        <body>
            {1}
        </body>
        </html>
    '''.format(name, final_body)
    return template


def save2html(path):
    df = pd.read_csv('./data/disease_list.csv', encoding='gbk')
    size = df.shape[0]
    for s in range(size):
        single = df.iloc[s, 1]
        if '/' in single:
            single = single.replace('/', '-')
        with open(path + '/{}.html'.format(single), 'w', encoding='utf8') as hf:
            res = requests.get(df.iloc[s, 2], headers=headers)
            body_content = res.text.encode(res.encoding).decode('utf8')
            body_pattern1 = re.compile('<div class="lemma-summary" label-module="lemmaSummary">(.*?)<div class="tashuo-bottom" id="tashuo_bottom">'
                                       , re.S)
            body_pattern2 = re.compile('<div class="lemma-summary" label-module="lemmaSummary">(.*?)<div id="open-tag">'
                                       , re.S)
            body = re.findall(body_pattern1, body_content)
            if body:
                template = html_template(body, single)
                hf.write(template)
            else:
                body = re.findall(body_pattern2, body_content)
                template = html_template(body, single)
                hf.write(template)
        print('Already writen the html file for {0}, order==>{1}'.format(single, s+1))


def txt2html(txt_path, save_path):
    txt_list = glob.glob(os.path.join(txt_path, '*.txt'))
    for m, tl in enumerate(txt_list):
        name = tl.split('\\')[-1].strip()[:-4]
        with open(tl, encoding='utf8') as tf:
            content_list = ['<p>' + t + '<br>' + '</p>' for t in tf.read().split('\n') if t]
            content_str = ''.join(content_list)
            template = '''
                <!DOCTYPE html>
                <html>
                <head>
                <meta charset="utf-8">
                <title>{0}</title>
                </head>
                <body>
                    <p>{1}</p>
                </body>
                </html>
            '''.format(name, content_str)
            with open(save_path + './{}.html'.format(name), 'w', encoding='utf8') as h:
                h.write(template)
        print('Already writen the html file for {0}, order==>{1}'.format(name, m+1))


def main():
    # get_disase()
    # txt_path = './data/txt'
    html_path = './data/html'
    # save2txt(txt_path)
    save2html(html_path)
    # txt2html(txt_path, html_path)


if __name__ == '__main__':
    main()
