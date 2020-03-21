# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JianshuItem(scrapy.Item):
    # 文章id
    article_id = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 文章内容
    content = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 头像
    avatar = scrapy.Field()
    # 发布时间
    pub_time = scrapy.Field()
    # 原始url
    origin_url = scrapy.Field()
    # 字数
    word_count = scrapy.Field()
    # 阅读量
    read_count = scrapy.Field()
    # 评论数
    comment_count = scrapy.Field()
    # 点赞数
    like_count = scrapy.Field()
    # 所属专题
    subjects = scrapy.Field()



