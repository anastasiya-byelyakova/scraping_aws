from scrapy.spiders import CrawlSpider, Rule
from scrapy import Request
import pandas as pd

class SpiderSpider(CrawlSpider):
    name = 'aws'
    allowed_domains = ['amazon.com/']
    start_url = 'https://www.amazon.com/product-reviews/'

    def __init__(self, file='', **kwargs):


        self.AISN = set(pd.read_csv(file, header=None)[0])

        super().__init__(**kwargs)

    def start_requests(self):

        for i in self.AISN:
            link = self.start_url+i
            yield Request(link,
                          callback= self.parse_product)

    def parse_product(self, response):

        url = response.url
        product_name = response.xpath('//*[@id="cm_cr-product_info"]/div/div[2]/div/div/div[2]/div[1]/h1/a/text()').extract_first()
        average_rating = response.xpath('//*[@id="cm_cr-product_info"]/div/div[1]/div[2]/div/div/div[2]/div/span/text()').extract_first()
        total_ratings =  response.xpath('//*[@id="cm_cr-product_info"]/div/div[1]/div[3]/span/text()').extract_first()
        question_answered = response.xpath('//*[@id="a-page"]/div[2]/div[1]/div[1]/div/div[2]/div[1]/form/a/text()').extract_first()
        positive_reviews = response.xpath('//*[contains(text(),"positive reviews")]/text()').extract_first()
        negative_reviews = response.xpath('//*[contains(text(),"critical reviews")]/text()').extract_first()
        total_reviews = response.xpath('//*[@id="filter-info-section"]/span/text()').extract_first()

        yield {
            'URL': url,
            'AISN':url.split('/')[-1],
            'Title':product_name,
            'Average rating':average_rating,
            'Total ratings':total_ratings,
            'Questions answered':question_answered,
            'Positive reviews':positive_reviews,
            'Critical reviews':negative_reviews,
            'Total reviews':total_reviews
        }
