# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
import requests
from selenium import webdriver
import re
from PIL import Image
from YDMHTTPDemo import yan_zheng
from selenium.webdriver.support.ui import WebDriverWait
from scrapy.http import HtmlResponse


class YxspiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class YxspiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class UserMiddleware(object):
    def __init__(self, random='random'):
        self.ua = UserAgent()
        self.type = random

    @classmethod
    def from_crawler(cls, crawler):
        return cls(random=crawler.settings.get('USER_AGENT'))

    def process_request(self, request, spider):
        request.headers['User-Agent'] = getattr(self.ua, self.type)
        return None


class ProxyMiddleware(object):
    def __init__(self, proxy):
        self.proxy = proxy

    @classmethod
    def from_crawler(cls, crawler):
        return cls(proxy=crawler.settings.get('PROXY'))

    def get_ip(self):
        try:
            response = requests.get(self.proxy)
            if response.status_code == 200:
                return response.text
        except Exception as e:
            print(e)
            return None

    def process_request(self, request, spider):
        if self.get_ip():
            url = 'http://' + self.get_ip()
            request.meta['proxy'] = url


class SeleniumMiddleware(object):
    def __init__(self):
        self.web = webdriver.Chrome()
        self.web.maximize_window()

    def process_response(self, request, response, spider):
        if response.status == 302:
            print('{}--出现验证码'.format(request.url))
            # 如果状态码是302 那么代表出现验证码，这时候可以调用selenium
            # 重新对象这个地址发起请求，那么使用selenium重新发起的请求可能
            # 将验证码规避，

            # selenium访问也会出现两种情况，
            # 第一种：不弹验证码，
            # 第二种：依旧弹验证码。

            self.web.get(request.url)
            res = re.compile(r'<title>(.*?)</title>', re.S)
            title = re.search(res, self.web.page_source).group(1)
            if title == '优信二手车-人机验证页':
                print('请输入验证码 ！！！！')
                print('使用selenium访问-{}-也出现验证码'.format(request.url))
                # 截取出现验证码的整个页面
                self.web.save_screenshot('captcha_html.png')
                captcha = self.web.find_element_by_css_selector('span.vcode>img')
                # 获取验证码图片的x坐标和y坐标，图片的高度和宽度
                x = captcha.location["x"]
                y = captcha.location["y"]
                width = captcha.location["x"] + captcha.size["width"]
                height = captcha.location["y"] + captcha.size["height"]
                # 从整个截取页面中定位到验证码图片，给验证码图片截取下来
                image = Image.open("captcha_html.png")
                captcha_img = image.crop((x, y, width, height))
                captcha_img.save("captcha.png")
                while True:
                    cid, result = yan_zheng('captcha.png')
                    # result = input('请输入你看的验证码：')
                    # result :验证码的识别结果。
                    # 定位到输入框中， 将识别结果传入到输入框，提交验证码
                    yzm_input = WebDriverWait(self.web, 20).until(lambda browser: self.web.find_element_by_css_selector("input.form-ipt")).send_keys(result)
                    WebDriverWait(self.web, 20).until(lambda browser: self.web.find_element_by_css_selector("span.sub-btn")).click()
                    # 判断验证码是不是成功。
                    error = WebDriverWait(self.web, 20).until(lambda browser: self.web.find_element_by_css_selector('p.error'))
                    if error.text == '图片验证码错误':

                        # 如果error的值对应的是图片验证码错误，说明验证码没有识别成功，那么将输入框的中的验证码清空，等待重新识别
                        yzm_input.clear()
                    else:
                        print('验证码识别成功。！')
                        break
            else:
                print('使用selenium访问-{}-没有出现验证码！'.format(request.url))
            # 不管使用selenium访问有没有出现验证码，最终都将selenium访问得到的response返回
            return HtmlResponse(url=request.url, body=self.web.page_source, request=request, encoding='utf-8')
        # 如果状态码不是 302 那么就直接返回出去。
        return response

