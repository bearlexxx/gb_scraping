"""
1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
    которая будет добавлять только новые вакансии/продукты в вашу базу.
2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой
    больше введённой суммы (необходимо анализировать оба поля зарплаты).
"""

import requests
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
from pprint import pprint

URL = 'https://hh.ru/search/vacancy'
AREA = 1844
text = 'python'
items_on_page = 20

params = {
    'area': AREA,
    'text': text,
    'items_on_page': items_on_page,
    'page': 0,
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

client = MongoClient('mongodb://127.0.0.1:27017/')
# print(client.list_database_names())
db = client.parse_hh_db
db_vacancies = db.vacancies


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


def add_vacancy(vacancies, vacancies_db):
    new_vacancy_count = 0
    for vacancy in vacancies:
        if vacancies_db.count_documents({'vacancy_link': vacancy['vacancy_link']}, limit=1) == 0:
            vacancies_db.insert_one(vacancy)
            print(f'Новая вакансия "{vacancy["vacancy_name"]}" добавлена')
            new_vacancy_count += 1
    vacancies_in_db = vacancies_db.find()
    pprint(f'Добавлено {new_vacancy_count} записей. Количество вакансий {len(list(vacancies_in_db))}')


def search_vacancy_by_salary(vacancies_db):
    while True:
        try:
            salary_needed = int(input('Введите размер зарплаты: '))
            break
        except ValueError:
            print('Ошибка! Значение должно быть числом!')
    searched_vacancies = vacancies_db.find(
        {'$or': [{'min_salary': {'$gte': salary_needed}}, {'max_salary': {'$gte': salary_needed}}]})

    return searched_vacancies


if __name__ == "__main__":
    add_vacancy(vacancies=hh_bs_parser(url=URL, params=params, headers=headers), vacancies_db=db_vacancies)
