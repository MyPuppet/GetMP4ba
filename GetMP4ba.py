#!/usr/bin/env python
# -*- coding:utf-8 -*- 
import requests
import random
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class GetMP4ba:

    def __init__(self):
        # 构造 当前页第1页、总共爬取页数，写入HTML文件头
        self.current_page = 1
        self.count_page = self.get_count_page()
        self.output = open('result.html', 'w+')
        self.output.write('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>mp4ba爬取结果</title>
    <link href="https://cdn.bootcss.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <table class="table-responsive table-hover">
        <th>电影名</th>
        <th>磁力连接</th>''')

    def __del__(self):
        self.output.write('''
    </table>
</body>
</html>
''')
        self.output.close()

    # 获取总共页数
    def get_count_page(self):
        headers = self.get_headers()
        response = requests.get("http://www.mp4ba.net/", headers=headers)
        html = etree.HTML(response.text)
        result = html.xpath('//span[@id="fd_page_bottom"]//a[last()-1]')[0].text
        return int(result[4:])

    # 获取列表并写入文件
    def get_list(self, url):
        headers = self.get_headers()
        response = requests.get(url, headers=headers)
        html = etree.HTML(response.text)
        href = html.xpath('//a[@class="s xst"]/@href')
        list = html.xpath('//a[@class="s xst"]')
        list_count = len(list)
        for index in range(list_count):
            headers = self.get_headers()
            try:
                response = requests.get(href[index], headers=headers)
            except:
                response = requests.get(href[index], headers=headers)
            html = etree.HTML(response.text)
            current_url = html.xpath('//div[@id="top"]/p/a/@href')
            # 判断获取的磁力链接是否为空
            if current_url:
                self.output.write('''
        <tr><td>'''+ list[index].text +'''</td><td>'''+ current_url[-1] +'''</td></tr>''')

    # 获取随机User-Agent参数 此处不合理，应该只返回UA，对于这个脚本这样足以
    def get_headers(self):
        user_agent_list = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1',
            'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6',
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5',
            'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3',
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24'
        ]
        UA = random.choice(user_agent_list)
        headers = {'User-Agent': UA}
        return headers

    # 入口程序
    def run(self):
        print('Get started with a total of '+ str(self.count_page) +' pages')
        while self.current_page <= self.count_page:
            print('Get page %d ,a total of %d/%d' % (self.current_page, self.current_page, self.count_page))
            current_url = 'http://www.mp4ba.net/forum-mp4ba-' + str(self.current_page) + '.html'
            self.get_list(current_url)
            self.current_page += 1
        print('Get complete, get a total of %d pages' % self.count_page)

mp4ba = GetMP4ba()
print('''
Author: MyPuppet
loding....
''')
mp4ba.run()