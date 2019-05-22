#-*- coding:utf-8 -*-
#程序员:Code.Zhang
#座右铭:将来的你一定会感激拼命的自己！
#时间:2018/12/5 16:39
#文件名称：test.py
#使用的IDE:PyCharm

import requests
import re
from lxml import etree
def crawl_iphai():
    for s in range(1, 13):
        start_url = 'http://www.89ip.cn/index_{}.html'.format(s)
        html = requests.get(start_url)
        if html:
            html_obj = etree.HTML(html.text)
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

if __name__ == '__main__':
   for x in crawl_iphai():
       print(x)

