# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshu.items import JianshuItem


class JsSpider(CrawlSpider):
    name = 'test'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/p/8ef87ce8df0a', 'https://www.jianshu.com/p/c5dffe39c2f5']

    def parse(self, response):
        # 文章id,可从url获取
        article_id = response.url.split('/')[-1]
        # 标题
        title = response.xpath('//h1[@class="_1RuRku"]/text()').get()
        # 内容,这里把内容的标签也保存下来
        content = response.xpath('//article').get()
        # 作者
        author = response.xpath('//a[@class="_1OhGeD"]/text()').get()
        # 头像
        avatar = response.xpath('//img[@class="_13D2Eh"]/@src').get()
        # 发布时间
        pub_time = response.xpath('//div[@class="s-dsoj"]/time/text()').get()
        #字数和阅读量没有可供筛选的条件，并且他们前面有个span有些页面有有些页面没有，所以倒数着来取
        # 字数
        word_count = response.xpath('//div[@class="s-dsoj"]/span[last()-1]/text()').get()
        word_count = word_count.split()[-1]
        # 阅读量
        read_count = response.xpath('//div[@class="s-dsoj"]/span[last()]/text()').get()
        read_count = read_count.split()[-1]

        # 评论数,span中含有注释签<!---->，所以需要getall()才能获取到后面的数字
        comment_count = response.xpath('//div[@class="-pXE92"]/div[1]/span//text()').getall()[-1]
        # 点赞数,没有点赞数的话没有任何数字，所以自己判断一下给它赋0
        like_count = response.xpath('//div[@class="-pXE92"]/div[2]/span//text()').getall()
        if len(like_count) == 1:
            like_count = '0'
        else:
            like_count = like_count[-1]

        # 所属专题
        subjects = response.xpath('//div[contains(@class, "_2Nttfz")]/a/span/text()').getall()
        # getall()返回的是一个列表，将专题列表转换成以逗号分隔的字符串。
        subjects = ','.join(subjects)

        # url
        origin_url = response.url

        item = JianshuItem(
            article_id=article_id,
            title=title,
            content=content,
            author=author,
            avatar=avatar,
            pub_time=pub_time,
            word_count=word_count,
            read_count=read_count,
            comment_count=comment_count,
            like_count=like_count,
            subjects=subjects,
            origin_url=origin_url
        )

        yield item
