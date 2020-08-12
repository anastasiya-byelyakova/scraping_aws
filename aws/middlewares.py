# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy.http import HtmlResponse
from scrapy.utils.python import to_bytes
from scrapy import signals

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options


class SeleniumMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signals.spider_opened)
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
        return middleware

    def process_request(self, request, spider):
        # import requests
        #
        # headers = {
        #     "apikey": "7bbae810-dcc5-11ea-8d11-3b853f2dbb82"
        # }
        #
        # params = (
        #     ("url", request.url),
        # )
        #
        # response = requests.get('https://app.zenscrape.com/api/v1/get',
        #                         headers=headers,
        #                         params=params)
        request.meta['driver'] = self.driver  # to access driver from response
        self.driver.get(request.url)
        time.sleep(1)

        body = to_bytes(self.driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML"))  # body must be of type bytes

        return HtmlResponse(self.driver.current_url,
                            body=body,
                            encoding='utf-8',
                            request=request)

    def spider_opened(self, spider):
        options = Options()

        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

        self.driver = webdriver.Chrome(
            executable_path=ChromeDriverManager().install(),
            chrome_options=options
        )

    def spider_closed(self, spider):
        self.driver.close()