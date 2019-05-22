# -*- coding: utf-8 -*-
"""
优信二手车访问二手车列表页的时候是不会弹出验证码的，访问汽车详情页的如果速度过快的时候会弹出验证码。
1. 降低爬虫的爬取速度。缺点：影响效率。
2. 设置随机请求头和代理ip。缺点：设置请求头和代理ip并一定能够避免验证码的出现。
3. 识别验证码。
"""
import scrapy


class YxSpider(scrapy.Spider):
    name = 'yx'
    allowed_domains = ['www.youxin.com']
    # start_urls = ['http://www.xin.com/']
    car_list = ['baoshijie', 'wey', 'luhu']
    city_list = ['beijing', 'shanghai', 'zhengzhou']

    def start_requests(self):
        for city in self.city_list:
            for car in self.car_list:
                url = 'https://www.xin.com/{}/{}/'.format(city, car)
                yield scrapy.Request(url=url, dont_filter=True, meta={'car': car, 'city': city})

    def parse(self, response):
        href_list = response.css('ul>li>div>a::attr(href)').extract()
        for href in href_list:
            every_car_url = 'https:' + href
            yield scrapy.Request(url=every_car_url, callback=self.parse_info, meta=response.meta, dont_filter=True)
        next_href = response.xpath('//a[text()="下一页"]/@href').extract_first('')

        print()
        if next_href:
            next_url = 'http://www.xin.com' + next_href
            yield scrapy.Request(url=next_url, callback=self.parse, meta=response.meta, dont_filter=True)
        else:
            print('没有下一页')

    def parse_info(self, response):
        """
        解析汽车详细信息的函数。
        :param response:
        :return:
        """
        # 汽车品牌
        car = response.meta['car']
        # 汽车所在城市
        city = response.meta['city']
        # 汽车的地址。
        car_url = response.url
        # 汽车的名称
        car_name = response.xpath('//div[@class="cd_m_h cd_m_h_zjf"]/span/text()').extract_first().strip()

        # 汽车价格
        car_price = response.css('.cd_m_info_jg>b::text').extract_first('')
        # 汽车的上牌日期
        car_time = response.css('li:nth-child(1)>span:nth-child(2)::text').extract_first('')
        # 使用里程。
        use_km = response.css('.cd_m_info_desc>li:nth-child(2)>a::text').extract_first('').strip()
        # 国标
        car_gb = response.css('.cd_m_info_desc>li:nth-child(3)>span:nth-child(1)::text').extract_first('')
        # 排量
        car_pl = response.css('.cd_m_info_desc>li:nth-child(4)>span:nth-child(1)::text').extract_first('')
        # 提车日期
        car_get_time = response.css('.cd_m_info_desc>li:nth-child(5)>span:nth-child(1)::text').extract_first('')
        print(car_name)

