import scrapy
from scrapy import FormRequest


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['scrapethissite.com']
    start_urls = ['https://www.scrapethissite.com/pages/advanced/?gotcha=csrf']

    def parse(self, response):
        csrf_token = response.xpath('//input[@name="csrf"]/@value').get()
        yield FormRequest.from_response(
            response,
            formxpath='//form',
            formdata={
                'csrf': csrf_token,
                'user': 'scraping@gb.ru',
                'pass': 'password123'
            },
            callback=self.after_login
        )

    def after_login(self, response):
        quotes = response.xpath('//div[@class="col-md-4 col-md-offset-4"]').get()
        print(f'{quotes}')
