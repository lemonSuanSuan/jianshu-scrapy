# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshu.items import JianshuItem


class JsSpider(CrawlSpider):
    name = 'js'
    allowed_domains = ['jianshu.com']
    # 从首页开始爬取
    start_urls = ['https://www.jianshu.com/']
    # 爬取整站的文章的方法：爬到首页推荐的文章链接，进入后继续提取每个页面出现的推荐文章详情页的链接（所以要follow=True）
    # 分析得出，每个详情页的链接为匹配规则为/p/和后面跟12个小写字母和数字的组合
    # 可以看到其实从页面上提取的并不是完整的链接，只是/p/xxxxxxxxxxxx这种形式,但是提取器会自动补全链接
    # 进入LinkExtractor代码可以看到它会拿response的base_url拼接
    # 就是提取到的链接会被自动拼接成https://www.jianshu.com/p/xxxxxxxxxxxx
    rules = (
        Rule(LinkExtractor(allow=r'/p/[0-9a-z]{12}'), callback='parse_detail', follow=True),
    )

    def parse_detail(self, response):
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
        # 字数和阅读量没有可供筛选的条件，并且他们前面有个span有些页面有有些页面没有，所以倒数着来取
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
