"""
Собрать информацию о вакансиях на вводимую должность с сайтов hh.ru и/или Superjob и/или работа.ру.
 Приложение должно анализировать несколько страниц сайта. Получившийся список должен содержать в себе минимум:
Наименование вакансии.
Предлагаемую зарплату (дополнительно: разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к
цифрам).
Ссылку на саму вакансию.
Сайт, откуда собрана вакансия.
По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
Структура должна быть одинаковая для вакансий с всех сайтов. Общий результат можно вывести с помощью dataFrame
через pandas, сохранить в json, либо csv.
"""
from pprint import pprint

import requests
from bs4 import BeautifulSoup as bs

URL = 'https://hh.ru/search/vacancy'

params = {
    'area': 1844,
    'text': 'python',
    'items_on_page': 20,
    'page': 0,
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}


def hh_bs_parser(url, params, headers):
    vacancies_list = []
    response = requests.get(url=url, params=params, headers=headers)
    # pprint(response.status_code)
    while response.ok:
        response = requests.get(url=url, params=params, headers=headers)
        soup = bs(response.content, 'html.parser')
        vacancies = soup.find_all('div', {'class': "serp-item"})
        if not vacancies:
            # print(len(vacancies_list))
            return vacancies_list
        for vacancy in vacancies:
            vacancy_name = vacancy.find('a', {'class': 'serp-item__title'}).getText()
            vacancy_link = vacancy.find('a', {'class': 'serp-item__title'}).get('href')
            vacancy_employer = vacancy.find('a', {'class': 'bloko-link bloko-link_kind-tertiary'}).getText().replace(
                '\xa0', ' ')
            vacancy_salary = vacancy.find('span', {'class': 'bloko-header-section-3'})
            min_salary = None
            max_salary = None
            currency = None
            if vacancy_salary:
                vacancy_salary = vacancy_salary.getText().replace('\u202f', "")
                vacancy_salary_split = vacancy_salary.split(' ')
                if len(vacancy_salary_split) == 3 and vacancy_salary_split[0] == 'от':
                    min_salary = int(vacancy_salary_split[1])
                    max_salary = None
                    currency = vacancy_salary_split[2]
                if len(vacancy_salary_split) == 3 and vacancy_salary_split[0] == 'до':
                    min_salary = None
                    max_salary = int(vacancy_salary_split[1])
                    currency = vacancy_salary_split[2]
                if len(vacancy_salary_split) == 4:
                    min_salary = int(vacancy_salary_split[0])
                    max_salary = int(vacancy_salary_split[2])
                    currency = vacancy_salary_split[3]

            vacancies_dict = {
                'vacancy_name': vacancy_name,
                'vacancy_link': vacancy_link,
                'vacancy_employer': vacancy_employer,
                'salary': vacancy_salary,
                'min_salary': min_salary,
                'max_salary': max_salary,
                'currency': currency,
            }
            vacancies_list.append(vacancies_dict)

        params['page'] += 1

    return vacancies_list


vacancies_list = hh_bs_parser(URL, params=params, headers=headers)
pprint(vacancies_list)
