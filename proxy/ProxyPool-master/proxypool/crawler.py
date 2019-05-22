import json
import re
from .utils import get_page
from pyquery import PyQuery as pq
from lxml import etree
from urllib.request import quote

class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies

    def freeProxyTwelve(self):
        for i in range(1,9):
            url = 'http://ip.jiangxianli.com/?page={}'.format(i)
            response = get_page(url)
            html_tree = etree.HTML(response.text)
            tr_list = html_tree.xpath("/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr")
            if len(tr_list) == 0:
                continue
            for tr in tr_list:
                yield tr.xpath("./td[2]/text()")[0] + ":" + tr.xpath("./td[3]/text()")[0]

    def ip_spider(self):
        city_list = ["安徽", "广东", "江苏", "北京", "浙江"]
        for x in city_list:
            city = quote('{}', encoding='utf-8').format(x)
            url = "http://31f.cn/region/{}/".format(city)
            response = get_page(url)
            # print(response)
            html = etree.HTML(response)
            tr_list = html.cssselect('.table tr')
            del tr_list[0]
            for tr in tr_list:
                ip = tr.xpath('td[2]/text()')[0]
                port = tr.xpath('td[3]/text()')[0]
                proxy = ip + ":" + port
                yield proxy

    def crawl_iphai(self):
        for s in range(1, 10):
            start_url = 'http://www.89ip.cn/index_{}.html'.format(s)
            html = get_page(start_url)
            if html:
                html_obj = etree.HTML(html)
                for s in range(0, 15):
                    find_ip = html_obj.xpath("//tbody/tr/td[1]")[s]
                    find_port = html_obj.xpath("//tbody/tr/td[2]")[s]
                    ip_2 = find_ip.text
                    # print(ip_2)
                    port_2 = find_port.text
                    remove_n = re.compile(r'\n')
                    ip = re.sub(remove_n, '', ip_2)
                    port_3 = re.sub(remove_n, '', port_2)
                    ip = ip.strip()
                    port = port_3.strip()
                    address_port = ip + ':' + port
                    # print(address_port)
                    yield address_port.replace(' ', '')

    def crawl_zhandaye(self):
        start_url = 'http://ip.seofangfa.com'
        html = get_page(start_url)
        if html:
            res = etree.HTML(html)
            tr_list = res.xpath('//tbody/tr')
            for tr in tr_list:
                ip = tr.xpath('td[1]/text()')[0]
                duankou = tr.xpath('td[2]/text()')[0]
                result = ip + ':' + duankou
                yield result.replace(' ', '')

    def crawl_xiladaili(self):
        for x in range(1, 21):
            start_url = "http://www.xiladaili.com/gaoni/{}/".format(x)
            response = get_page(start_url)
            html = etree.HTML(response)
            ip_list = html.xpath('//tbody/tr/td[1]/text()')
            for ip in ip_list:
                yield ip

    def F31(self):
        base_url = 'http://31f.cn/'
        html = get_page(base_url)
        if html:
            res = etree.HTML(html)
            tr_list = res.xpath('//table[@class="table table-striped"]/tbod/tr')
            del tr_list[0]
            for tr in tr_list:
                ip_find = tr.xpath('td[2]/text()')[0]
                ip_duankou = tr.xpath('td[3]/text()')[0]
                ip = ip_find + ':' + ip_duankou
                yield ip.replace(' ', '')


    def crawl_jisu(self):
        for x in range(1, 11):
            start_url = 'http://www.superfastip.com/welcome/freeip/{}'.format(x)
            # print('Crawling', start_url)
            html = get_page(start_url)
            if html:
                html_obj = etree.HTML(html)
                agent_ip_1 = html_obj.xpath('//tbody/tr/td[1]/text()')
                agent_ip_2 = html_obj.xpath('//tbody/tr/td[2]/text()')
                for a in range(len(agent_ip_1)):
                    ip = agent_ip_1[a]
                    port = agent_ip_2[a]
                    agent_ip = ip + ":" + port
                    yield agent_ip

    # def crawl_xroxy(self):
    #     for page in range(1, 14):
    #         # print('正在抓取{}页的ip'.format(page))
    #         url = "http://www.89ip.cn/index_{}.html".format(page)
    #         response = get_page(url)
    #         html = etree.HTML(response)
    #         tr_list = html.xpath('//div[@class="layui-form"]/table/tbody/tr')
    #         for tr in tr_list:
    #             address = tr.xpath('td[1]/text()')[0].replace('\n', '').replace('\t', '')
    #             port = tr.xpath('td[2]/text()')[0].replace('\n', '').replace('\t', '')
    #             final_ip = address + ":" + port
    #             # print(final_ip)
    #             yield final_ip

    # def crawl_daxiang(self):
    #     url = 'http://vtp.daxiangdaili.com/ip/?tid=559363191592228&num=50&filter=on'
    #     html = get_page(url)
    #     if html:
    #         urls = html.split('\n')
    #         for url in urls:
    #             yield url



    # def crawl_jisudaili(self):
    #     #     for x in range(1, 10):
    #     #         start_url = "http://www.superfastip.com/welcome/freeip/{}".format(x)
    #     #         html = get_page(start_url)
    #     #         ip_address = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
    #     #         # \s * 匹配空格，起到换行作用
    #     #         re_ip_address = ip_address.findall(html)
    #     #         for address, port in re_ip_address:
    #     #             result = address + ':' + port
    #     #             yield result.replace(' ', '')
          
    # def crawl_daili66(self, page_count=4):
    #     """
    #     获取代理66
    #     :param page_count: 页码
    #     :return: 代理
    #     """
    #     start_url = 'http://www.66ip.cn/{}.html'
    #     urls = [start_url.format(page) for page in range(1, page_count + 1)]
    #     for url in urls:
    #         print('Crawling', url)
    #         html = get_page(url)
    #         if html:
    #             doc = pq(html)
    #             trs = doc('.containerbox table tr:gt(0)').items()
    #             for tr in trs:
    #                 ip = tr.find('td:nth-child(1)').text()
    #                 port = tr.find('td:nth-child(2)').text()
    #                 yield ':'.join([ip, port])

    # def crawl_proxy360(self):
    #     """
    #     获取Proxy360
    #     :return: 代理
    #     """
    #     start_url = 'http://www.proxy360.cn/Region/China'
    #     print('Crawling', start_url)
    #     html = get_page(start_url)
    #     if html:
    #         doc = pq(html)
    #         lines = doc('div[name="list_proxy_ip"]').items()
    #         for line in lines:
    #             ip = line.find('.tbBottomLine:nth-child(1)').text()
    #             port = line.find('.tbBottomLine:nth-child(2)').text()
    #             yield ':'.join([ip, port])

    # def crawl_goubanjia(self):
    #     """
    #     获取Goubanjia
    #     :return: 代理
    #     """
    #     start_url = 'http://www.goubanjia.com/free/gngn/index.shtml'
    #     html = get_page(start_url)
    #     if html:
    #         doc = pq(html)
    #         tds = doc('td.ip').items()
    #         for td in tds:
    #             td.find('p').remove()
    #             yield td.text().replace(' ', '')

    # def crawl_ip181(self):
    #     start_url = 'http://www.ip181.com/'
    #     html = get_page(start_url)
    #     ip_address = re.compile('<tr.*?>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
    #     # \s* 匹配空格，起到换行作用
    #     re_ip_address = ip_address.findall(html)
    #     for address,port in re_ip_address:
    #         result = address + ':' + port
    #         yield result.replace(' ', '')


    # def crawl_ip3366(self):
    #     for page in range(1, 4):
    #         start_url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(page)
    #         html = get_page(start_url)
    #         ip_address = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
    #         # \s * 匹配空格，起到换行作用
    #         re_ip_address = ip_address.findall(html)
    #         for address, port in re_ip_address:
    #             result = address+':'+ port
    #             yield result.replace(' ', '')


    # def crawl_kxdaili(self):
    #     for i in range(1, 11):
    #         start_url = 'http://www.kxdaili.com/ipList/{}.html#ip'.format(i)
    #         html = get_page(start_url)
    #         ip_address = re.compile('<tr.*?>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
    #         # \s* 匹配空格，起到换行作用
    #         re_ip_address = ip_address.findall(html)
    #         for address, port in re_ip_address:
    #             result = address + ':' + port
    #             yield result.replace(' ', '')


    # def crawl_premproxy(self):
    #     for i in ['China-01','China-02','China-03','China-04','Taiwan-01']:
    #         start_url = 'https://premproxy.com/proxy-by-country/{}.htm'.format(i)
    #         html = get_page(start_url)
    #         if html:
    #             ip_address = re.compile('<td data-label="IP:port ">(.*?)</td>')
    #             re_ip_address = ip_address.findall(html)
    #             for address_port in re_ip_address:
    #                 yield address_port.replace(' ','')

    # def crawl_xroxy(self):
    #     for i in ['CN','TW']:
    #         start_url = 'http://www.xroxy.com/proxylist.php?country={}'.format(i)
    #         html = get_page(start_url)
    #         if html:
    #             ip_address1 = re.compile("title='View this Proxy details'>\s*(.*).*")
    #             re_ip_address1 = ip_address1.findall(html)
    #             ip_address2 = re.compile("title='Select proxies with port number .*'>(.*)</a>")
    #             re_ip_address2 = ip_address2.findall(html)
    #             for address,port in zip(re_ip_address1,re_ip_address2):
    #                 address_port = address+':'+port
    #                 yield address_port.replace(' ','')
    
    # def crawl_kuaidaili(self):
    #     for i in range(1, 4):
    #         start_url = 'http://www.kuaidaili.com/free/inha/{}/'.format(i)
    #         html = get_page(start_url)
    #         if html:
    #             ip_address = re.compile('<td data-title="IP">(.*?)</td>')
    #             re_ip_address = ip_address.findall(html)
    #             port = re.compile('<td data-title="PORT">(.*?)</td>')
    #             re_port = port.findall(html)
    #             for address,port in zip(re_ip_address, re_port):
    #                 address_port = address+':'+port
    #                 yield address_port.replace(' ','')

    # def crawl_xicidaili(self):
    #     for i in range(1, 3):
    #         start_url = 'http://www.xicidaili.com/nn/{}'.format(i)
    #         headers = {
    #             'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #             'Cookie':'_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWRjYzc5MmM1MTBiMDMzYTUzNTZjNzA4NjBhNWRjZjliBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUp6S2tXT3g5a0FCT01ndzlmWWZqRVJNek1WanRuUDBCbTJUN21GMTBKd3M9BjsARg%3D%3D--2a69429cb2115c6a0cc9a86e0ebe2800c0d471b3',
    #             'Host':'www.xicidaili.com',
    #             'Referer':'http://www.xicidaili.com/nn/3',
    #             'Upgrade-Insecure-Requests':'1',
    #         }
    #         html = get_page(start_url, options=headers)
    #         if html:
    #             find_trs = re.compile('<tr class.*?>(.*?)</tr>', re.S)
    #             trs = find_trs.findall(html)
    #             for tr in trs:
    #                 find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
    #                 re_ip_address = find_ip.findall(tr)
    #                 find_port = re.compile('<td>(\d+)</td>')
    #                 re_port = find_port.findall(tr)
    #                 for address,port in zip(re_ip_address, re_port):
    #                     address_port = address+':'+port
    #                     yield address_port.replace(' ','')
    #
    # def crawl_ip3366(self):
    #     #     for i in range(1, 4):
    #     #         start_url = 'http://www.ip3366.net/?stype=1&page={}'.format(i)
    #     #         html = get_page(start_url)
    #     #         if html:
    #     #             find_tr = re.compile('<tr>(.*?)</tr>', re.S)
    #     #             trs = find_tr.findall(html)
    #     #             for s in range(1, len(trs)):
    #     #                 find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
    #     #                 re_ip_address = find_ip.findall(trs[s])
    #     #                 find_port = re.compile('<td>(\d+)</td>')
    #     #                 re_port = find_port.findall(trs[s])
    #     #                 for address,port in zip(re_ip_address, re_port):
    #     #                     address_port = address+':'+port
    #     #                     yield address_port.replace(' ','')
    
    # def crawl_iphai(self):
    #     start_url = 'http://www.iphai.com/'
    #     html = get_page(start_url)
    #     if html:
    #         find_tr = re.compile('<tr>(.*?)</tr>', re.S)
    #         trs = find_tr.findall(html)
    #         for s in range(1, len(trs)):
    #             find_ip = re.compile('<td>\s+(\d+\.\d+\.\d+\.\d+)\s+</td>', re.S)
    #             re_ip_address = find_ip.findall(trs[s])
    #             find_port = re.compile('<td>\s+(\d+)\s+</td>', re.S)
    #             re_port = find_port.findall(trs[s])
    #             for address,port in zip(re_ip_address, re_port):
    #                 address_port = address+':'+port
    #                 yield address_port.replace(' ','')

    # def crawl_89ip(self):
    #     start_url = 'http://www.89ip.cn/apijk/?&tqsl=1000&sxa=&sxb=&tta=&ports=&ktip=&cf=1'
    #     html = get_page(start_url)
    #     if html:
    #         find_ips = re.compile('(\d+\.\d+\.\d+\.\d+:\d+)', re.S)
    #         ip_ports = find_ips.findall(html)
    #         for address_port in ip_ports:
    #             yield address_port

    # def crawl_data5u(self):
    #     start_url = 'http://www.data5u.com/free/gngn/index.shtml'
    #     headers = {
    #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #         'Accept-Encoding': 'gzip, deflate',
    #         'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    #         'Cache-Control': 'max-age=0',
    #         'Connection': 'keep-alive',
    #         'Cookie': 'JSESSIONID=47AA0C887112A2D83EE040405F837A86',
    #         'Host': 'www.data5u.com',
    #         'Referer': 'http://www.data5u.com/free/index.shtml',
    #         'Upgrade-Insecure-Requests': '1',
    #         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
    #     }
    #     html = get_page(start_url, options=headers)
    #     if html:
    #         ip_address = re.compile('<span><li>(\d+\.\d+\.\d+\.\d+)</li>.*?<li class=\"port.*?>(\d+)</li>', re.S)
    #         re_ip_address = ip_address.findall(html)
    #         for address, port in re_ip_address:
    #             result = address + ':' + port
    #             yield result.replace(' ', '')


            