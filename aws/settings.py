# -*- coding: utf-8 -*-

# Scrapy settings for people project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'people'

SPIDER_MODULES = ['aws.spiders']
NEWSPIDER_MODULE = 'aws.spiders'
ROBOTSTXT_OBEY = False
COOKIES_ENABLED = True
ITEM_PIPELINES = {
   'aws.pipelines.PeoplePipeline': 300,
}

USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36"

LOG_LEVEL='ERROR'
DATABASE_USER='root'
DATABASE_PASSWORD='123456789'
DATABASE_IP='localhost'
DATABASE_NAME='aws_aisn'
DOWNLOAD_DELAY=30
CONCURRENT_REQUESTS=1
# DOWNLOADER_MIDDLEWARES = {
#     'aws.middlewares.SeleniumMiddleware': 200
# }