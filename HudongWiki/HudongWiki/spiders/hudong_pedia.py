import scrapy
from HudongWiki.items import HudongItem
import urllib
'''
爬虫启动：
cd ~\HudongWiki\HudongWiki
scrapy crawl Hudong

file_object: 你要爬取提条的文本
内容格式:
朱自清
橘子
月台
'''

# 定义分隔符
split_sign = '##'

class HudongSpider(scrapy.Spider):
	name = "Hudong"
	# 声明地址域
	allowed_domains = ["http://www.baike.com"]
	file_object = open('./data/word_list.txt','r', encoding='utf8').read()
	wordList = file_object.split()
	start_urls = []
	count = 0

	# 本处是用于构造原始json
	for i in wordList:
		cur = "http://www.baike.com/wiki/"
		cur = cur + str(i)
		start_urls.append(cur)

	def parse(self, response):
		# div限定范围
		main_div = response.xpath('//div[@class="w-990"]')

		title = response.url.split('/')[-1]  #  通过截取url获取title
		title = urllib.parse.unquote(title)
		if title.find('isFrom=intoDoc') != -1:
			title = 'error'

		url = response.url
		url = urllib.parse.unquote(url)

		img = ""
		for p in main_div.xpath('.//div[@class="r w-300"]/div[@class="doc-img"]/a/img/@src'):
			img = p.extract().strip()

		openTypeList = ""
		# flag用于分隔符处理（第一个词前面不插入分隔符）
		flag = 0
		for p in main_div.xpath('.//div[@class="l w-640"]/div[@class="place"]/p[@id="openCatp"]/a/@title'):
			if flag == 1 :
				openTypeList += split_sign
			openTypeList += p.extract().strip()
			flag = 1

		detail = ""
		detail_xpath = main_div.xpath('.//div[@class="l w-640"]/div[@class="information"]/div[@class="summary"]/p')
		if len(detail_xpath) > 0 :
			detail = detail_xpath.xpath('string(.)').extract()[0].strip()
		# 可能为空
		if detail == "":
			detail_xpath = main_div.xpath('.//div[@class="l w-640"]/div[@id="content"]')
			if len(detail_xpath) > 0 :
				detail = detail_xpath.xpath('string(.)').extract()[0].strip()

		flag = 0
		baseInfoKeyList = ""
		for p in main_div.xpath('.//div[@class="l w-640"]/div[@name="datamodule"]/div[@class="module zoom"]/table//strong/text()'):
			if flag == 1 :
				baseInfoKeyList += split_sign
			baseInfoKeyList += p.extract().strip()
			flag = 1

		flag = 0
		baseInfoValueList = ""
		base_xpath = main_div.xpath('.//div[@class="l w-640"]/div[@name="datamodule"]/div[@class="module zoom"]/table')
		for p in base_xpath.xpath('.//span'):
			if flag == 1 :
				baseInfoValueList += split_sign
			all_text = p.xpath('string(.)').extract()[0].strip()
			baseInfoValueList += all_text
			flag = 1

		item = HudongItem()
		item['title'] = title
		item['url'] = url
		item['image'] = img
		item['openTypeList'] = openTypeList
		item['detail'] = detail
		item['baseInfoKeyList'] = baseInfoKeyList
		item['baseInfoValueList'] = baseInfoValueList

		yield item