# -*- coding: utf-8 -*-
import scrapy

'''
    Item: 对应互动百科的某个词条
    title： 词条标题
    url： 词条链接
    image: 词条对应图片链接
    openTypeList: 词条对应开放分类列表
    detail： 详细信息
    baseInfoKeyList: 基本信息key列表
    baseInfoValueList: 基本信息value列表
'''


class HudongItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    image = scrapy.Field()
    openTypeList = scrapy.Field()
    detail = scrapy.Field()
    baseInfoKeyList = scrapy.Field()
    baseInfoValueList = scrapy.Field()
