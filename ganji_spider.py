# -*- coding: utf-8 -*-
# @Filename: new_ganji.py
# @Author: Studog
# @Date: 2017/5/24 9:27

import requests
import lxml.html as HTML
import csv
from xpinyin import Pinyin
import os
import concurrent.futures


class GanjiSpider(object):

    def __init__(self):
        self.city = input("请输入城市名:\n")
        p = Pinyin()
        city_name = p.get_initials(self.city, '').lower()
        self.url = 'http://{0}.ganji.com/v/zhaopinxinxi/p1/'.format(city_name)
        self.save_path = r'G:\data\ganji.csv'
        file_dir = os.path.split(self.save_path)[0]
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)
        if not os.path.exists(self.save_path):
            os.system(r'echo >  %s' % self.save_path)

    def get_job(self):
        flag = True
        with open(self.save_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['职位名称', '月薪', '最低学历', '工作经验', '年龄', '招聘人数','工作地点'])
        while flag:
            html = HTML.fromstring(requests.get(self.url).text)
            content = html.xpath("//li[@class='fieldulli']/a/@href")
            next_page = html.xpath("//li/a[@class='next']/@href")
            # os.cpu_count() or 1
            with concurrent.futures.ProcessPoolExecutor() as executor:
                executor.map(self.get_url, content)
            if next_page:
                self.url = next_page[0]
            else:
                flag = False

    def get_url(self, html_page):
        html = HTML.fromstring(requests.get(html_page).text)
        job_list = html.xpath("//dl[@class='job-list clearfix']/dt/a/@href")
        # (os.cpu_count() or 1) * 5
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.get_info, job_list)

    def get_info(self, job_url):
            html = HTML.fromstring(requests.get(job_url).text)
            name = html.xpath("//li[@class='fl']/em/a/text()")
            info = html.xpath("//li[@class='fl']/em/text()")[1:]
            address = html.xpath(("//li[@class='fl w-auto']/em//text()"))
            if name and len(info) == 5 and address:
                info[2] = info[2].strip()
                address[2] = address[2].strip()
                address = ''.join(address)
                info.append(address)
                name.extend(info)
                print(name)
                with open(self.save_path, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(name)

if __name__ == '__main__':
    gj = GanjiSpider()
    gj.get_job()
