# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html


# 导入selenium的webdriver
from selenium import webdriver
import time
from scrapy.http.response.html import HtmlResponse
import random


class SeleniumDownloaderMiddleware(object):

    def __init__(self):
        # Selenium Webdriver是通过各种浏览器的驱动（web driver）来驱动浏览器的
        # 指定chrom的驱动（需要自己去下载chromedriver.exe）
        # Selenium到指定的路径将chromedriver程序运行起来，然后chromedriver就会去驱动chrome浏览器了
        # 默认是会到python环境里去找。因为我放到了环境变量那个路径下，所以也可以不指定路径
        # self.driver = webdriver.Chrome(r'C:\Users\Administrator\AppData\Local\Programs\Python\Python38\chromedriver.exe')
        self.driver = webdriver.Chrome()

    def process_request(self, request, spider):
        # 驱动打开请求页面
        self.driver.get(request.url)
        # 因为是异步请求，为避免未加载完成就获取的情况，等待1秒
        time.sleep(1)
        # 所属专题如果没有全部显示的话，需要模拟操作才能获取所有数据
        # 如果有“展示更多”按钮，点击，直到没有了，退出循环。如果一开始就没有该元素，会抛出异常，捕获异常。
        try:
            while True:
                # 定位元素
                show_more = self.driver.find_element_by_class_name("H7E3vT")
                # 点击该元素。因为直接show_more.click()失效了，所以通过执行js语句来点击
                self.driver.execute_script("arguments[0].click();", show_more)
                print('获取到并点击了该元素')
                time.sleep(0.5)
                if not show_more:
                    break
        except Exception as e:
            # 打印查看抛出的异常
            print(e)
        time.sleep(1)
        # 获取网页源代码
        source = self.driver.page_source
        # 将网页源代码封装成response返回给引擎。HtmlResponse需要传递的参数可以ctrl+B进入代码看。driver.current_url是当前页面url
        response = HtmlResponse(self.driver.current_url, body=source, request=request, encoding='utf-8')
        return response

# 随机user_agent中间件
class UseragentDownloaderMiddleware(object):
    USER_AGENTS = ['Mozilla/5.0 (compatible;U;ABrowse0.6;Syllable) AppleWebKit/420+ (KHTML, like Gecko)',
                   'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36',
                   'Mozilla/5.0 (Macintosh NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36']

    def process_request(self, request, spider):
        # 设置随机请求头用户代理
        user_agent = random.choice(self.USER_AGENTS)
        request.headers['User-Agent'] = user_agent


# ip代理池中间件
class IpprpxyDownloaderMiddleware(object):

    # PROXIES = ['200.73.129.213:8080', '157.230.241.171:44344', '132.145.93.114:3128', '132.145.93.114:3128']
    def process_request(self, request, spider):
        # 设置随机ip代理
        proxy = random.choice(self.PROXIES)
        request.meta['proxy'] = 'http://{}'.format(proxy)
