"""
Написать приложение или функцию, которые собирают основные новости с сайта на выбор lenta.ru, yandex-новости.
Для парсинга использовать XPath.
Структура данных в виде словаря должна содержать:
- *название источника;
- наименование новости;
- ссылку на новость;
- дата публикации.
"""

from pprint import pprint

import requests
from lxml import html

URL = 'https://dzen.ru/news/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

params = {
    'issue_tld': 'ru',
    'sso_failed': ''
}


def get_content_dom_from_html_text(url, headers=None, params=None):
    response = requests.get(url, headers=headers, params=params)
    content_dom = html.fromstring(response.text)

    print(response.url)

    return content_dom


def dzen_parse(content_dom):
    news_tabs = content_dom.xpath('//div[contains(@class,"mg-card_type_")]')
    news_list = []

    for news in news_tabs:
        news_source = news.xpath('.//a[@class="mg-card__source-link"]/text()')[0]
        news_name = news.xpath('.//h2/a/text()')[0].replace('\xa0', ' ')
        news_url = news.xpath('.//h2/a/@href')[0]
        news_time = news.xpath('.//span[@class="mg-card-source__time"]/text()')[0]

        news_dict = {
            'name': news_name,
            'url': news_url,
            'news_time': news_time,
            'news_source': news_source
        }

        news_list.append(news_dict)
    return news_list


dom = get_content_dom_from_html_text(URL, headers=headers, params=params)

dzen_news = (dzen_parse(dom))

pprint(dzen_news)
