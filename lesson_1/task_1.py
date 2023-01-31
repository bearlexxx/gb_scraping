"""
 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
сохранить JSON-вывод в файле *.json.
"""

import requests
import json

ACC = 'bearlexxx'

responce = requests.get(f'https://api.github.com/users/{ACC}/repos')

if responce.ok:
    with open(f'{ACC}.json', 'w', encoding='utf-8') as f:
        print(f'Список репозиториев аккаунта {ACC}:')
        for repo in responce.json():
            print(repo['name'])

        json.dump(responce.json(), f, indent=4, ensure_ascii=False)

    print(f'JSON-вывод  записан в файл {ACC}.json')
else:
    print(f'Ошибка! Код ошибки {responce.status_code}')
