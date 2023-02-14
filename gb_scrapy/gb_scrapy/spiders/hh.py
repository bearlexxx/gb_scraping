import scrapy
from scrapy.http import HtmlResponse

from gb_scrapy.items import GbScrapyParseItem


class HhSpider(scrapy.Spider):
    name = 'hh'
    allowed_domains = ['hh.ru']
    start_urls = [
        'https://hh.ru/search/vacancy?text=Python+junior&from=suggest_post&salary=&area=1&ored_clusters=true&enable_snippets=truehttps://hh.ru/search/vacancy?no_magic=true&L_save_area=true&text=Python+junior&area=1&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=20']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa= 'pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        vacancies_links = response.xpath("//a[@class = 'serp-item__title']/@href").getall()
        for link in vacancies_links:
            yield response.follow(link, callback=self.parse_vacancy)
        # print(f'##################### {response.url} ####################')

    def parse_vacancy(self, response: HtmlResponse):
        vacancy_name = response.css('h1::text').get()
        vacancy_url = response.url
        vacancy_salary = response.xpath("//div[@data-qa= 'vacancy-salary']//text()").getall()
        currency, max_salary, min_salary = self.clean_salary(vacancy_salary)
        yield GbScrapyParseItem(
            name=vacancy_name,
            url=vacancy_url,
            salary=vacancy_salary,
            min_salary=min_salary,
            max_salary=max_salary,
            currency=currency,
        )

    @staticmethod
    def clean_salary(vacancy, min_salary=None, max_salary=None, currency=None):
        for i in range(len(vacancy) - 1):
            if vacancy[i] == "з/п не указана":
                return currency, max_salary, min_salary
            elif vacancy[i] == "от ":
                min_salary = int(vacancy[i + 1].replace('\xa0', ''))
            elif vacancy[i] == " до " or vacancy[i] == "до ":
                max_salary = int(vacancy[i + 1].replace('\xa0', ''))

        if len(vacancy) > 1:
            currency = vacancy[-3]

        return currency, max_salary, min_salary
