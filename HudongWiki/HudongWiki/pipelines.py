# -*- coding: utf-8 -*-
import json
import time
from scrapy.exceptions import DropItem


class HudongPipeline(object):
    def __init__(self):
        self.count = 0
        self.file = open('./data/your_baike.json', 'w')
        self.start = time.time()
        
    def process_item(self, item, spider):
        # 'error'是百科中没有的页面赋予的title值（自己定义的）
        if item['title'] != 'error':
            line = ""
            if self.count > 0:
                line += ","
            line += json.dumps(dict(item), ensure_ascii=False) + '\n'
            self.file.write(line)
            self.count += 1
            cur = time.time()
            totalTime = int(cur-self.start)
            print("page count: " + str(self.count) + "      time:" + str(int(totalTime/3600)) + "h " +
                  str(int(totalTime/60) % 60) + "m " + str(totalTime % 60) + "s......")
            return item
        else:
            raise DropItem("百科中找不到对应页面！")
            
    def open_spider(self, spider):
        self.file.write("[\n")
        print("==================开启爬虫 \""+spider.name+"\" ==================")
        
    def close_spider(self, spider):
        self.file.write("\n]")
        print("==================关闭爬虫 \""+spider.name+"\" ==================")
